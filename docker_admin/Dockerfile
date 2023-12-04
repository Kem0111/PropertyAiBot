FROM python:3.11


ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/"


WORKDIR /code


RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction

ENTRYPOINT ["sh", "entrypoint.sh"]

CMD ["make", "start"]