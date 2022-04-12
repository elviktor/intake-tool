# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUMBUFFERED 1

ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install poetry==1.2.0

RUN git clone https://github.com/python-poetry/poetry /poetry

# Set work directory
WORKDIR /code

ENV VIRTUAL_ENV=/poetry-env \
    PATH="/poetry-env/bin:$POETRY_HOME/bin:$PATH"

# Copy project code
COPY pyproject.toml poetry.lock /code/

RUN python3 -m venv $VIRTUAL_ENV && \
    poetry install

# Copy entrypoint.sh
COPY entrypoint.sh /code/
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

CMD "pytest"
# Creating folders, and files for a project:
COPY . /code
