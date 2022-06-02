FROM ubuntu:20.04
RUN apt update
# RUN apt install -y ffmpeg
RUN apt install -y python3.9
RUN apt install -y python3-pip
RUN apt install -y libglib2.0-0
RUN apt install -y libgl1-mesa-dev
RUN pip install --user poetry
ENV PATH $PATH:/root/.local/bin/
WORKDIR /app
COPY poetry.lock /app/
COPY poetry.toml /app/
COPY pyproject.toml /app/
COPY main.py /app/
COPY model /app/model
RUN poetry install
