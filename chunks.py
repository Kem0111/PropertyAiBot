import json
import os

# Define the maximum allowed tokens per file
max_tokens_per_file = 2000000

# Define max files
max_files = 20

# Your input file
input_file="properties.json"

# Load the original JSON file
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Split the data into chunks based on the maximum allowed tokens
chunks = []
current_chunk = []
current_tokens = 0

for item in data:
    item_tokens = len(json.dumps(item))

    if current_tokens + item_tokens > max_tokens_per_file:
        chunks.append(current_chunk)
        current_chunk = []
        current_tokens = 0

    current_chunk.append(item)
    current_tokens += item_tokens

# Add the last chunk
if current_chunk:
    chunks.append(current_chunk)

# max_files = len(chunks)

# Save each chunk as a separate JSON file
output_directory = 'property'
os.makedirs(output_directory, exist_ok=True)

for i, chunk in enumerate(chunks):
    if (i < max_files):
        output_file_path = os.path.join(output_directory, f'property{i + 1}.json')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(chunk, output_file, ensure_ascii=False, indent=2)
    else:
        break

print(f'{i} files created in the {output_directory} directory.')