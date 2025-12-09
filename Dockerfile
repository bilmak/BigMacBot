FROM python:3.13.11
WORKDIR /src
RUN curl -sSL https://install.python-poetry.org | python3 - 
ENV PATH="/root/.local/bin:${PATH}"
COPY . /src/
RUN poetry install
RUN apt update && apt install rlwrap -y
CMD ["rlwrap", "poetry", "run", "python3", "-m", "app.main"]