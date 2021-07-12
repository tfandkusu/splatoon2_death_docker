FROM ubuntu:20.04
RUN apt update
RUN apt install -y ffmpeg
RUN apt install -y python3.9
RUN apt install -y python3-pip
RUN pip install --user opencv-python==4.5.3.56
RUN pip install --user tensorflow==2.5.0
RUN pip install --user tqdm==4.61.2
WORKDIR /app
COPY main.py /app/main.py
COPY model /app/model
