# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUMBUFFERED 1

# Install dependencies
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

# Set work directory
WORKDIR /code

# Copy project code
COPY pyproject.toml poetry.lock /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy entrypoint.sh
COPY entrypoint.sh /code/
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

# Creating folders, and files for a project:
COPY . /code
