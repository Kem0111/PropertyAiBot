import asyncio
import json
from .thread_manager import ThreadManager
from .assistant_manager import AssistantManager
from .db_manager import db_manager


class ChatSession:

    TOOL_TO_DB_FUNC = {
        "add_notification": db_manager.add_notification,
        "collect_user_info_for_order": db_manager.client_proccess,
        # "provide_property_ids": db_manager.add_user_request_pr
    }

    TOOL_CALL_OUTPUT = {
        "add_notification": 'result taken into account',
        "collect_user_info_for_order": 'result taken into account',
    }

    def __init__(self,
                 thread_manager: ThreadManager,
                 assistant_manager: AssistantManager,
                 user_id: int,
                 assistant_id: str = None,
                 thread_id: str = None,
                 ):

        self.thread_manager = thread_manager
        self.assistant_manager = assistant_manager
        self.user_id = user_id
        self.assistant_id = assistant_id
        self.thread_id = thread_id

    async def chat_loop(self, user_input):

        response = await self.get_latest_response(user_input)
        return response

    async def get_latest_response(self, user_input):
        # Send the user message
        await self.send_message(user_input)

        # Create a new run for the assistant to respond
        await self.create_run()

        # Wait for the assistant's response
        await self.wait_for_assistant()

        # Retrieve the latest response
        return await self.retrieve_latest_response()

    async def send_message(self, content):
        return await self.thread_manager.send_message(self.thread_id, content)

    async def create_run(self):
        return await self.thread_manager.create_run(self.thread_id, self.assistant_id)

    async def wait_for_assistant(self):
        while True:
            runs = await self.thread_manager.list_runs(self.thread_id)
            latest_run = runs.data[0]
            if latest_run.status in ["completed", "failed"]:
                break

            if latest_run.status == "requires_action":

                tool_outputs = []

                for tool_call in latest_run.required_action.submit_tool_outputs.tool_calls:
                    method = self.TOOL_TO_DB_FUNC.get(tool_call.function.name)
                    if method:
                        print(tool_call.function.arguments)
                        try:
                            results = await method(
                                self.user_id, **json.loads(tool_call.function.arguments)
                            )
                            output = self.TOOL_CALL_OUTPUT[tool_call.function.name].format(results)
                        except json.JSONDecodeError as e:
                            output = f"Ошибка при разборе JSON: {e}, Исходная строка JSON: {tool_call.function.arguments}"
                        except Exception as e:
                            output = f"Произошла ошибка: {e}"
                        tool_outputs.append(
                                {
                                    "tool_call_id": tool_call.id,
                                    "output": output
                                },
                            )

                if tool_outputs:
                    await self.thread_manager.submit_tool_outputs(
                        thread_id=self.thread_id,
                        run_id=latest_run.id,
                        tool_outputs=tool_outputs
                    )
            await asyncio.sleep(4)  # Wait for 4 seconds before checking again

    async def retrieve_latest_response(self):
        response = await self.thread_manager.list_messages(self.thread_id)
        for message in response.data:
            if message.role == "assistant":
                return message.content[0].text.value
        return None
