FROM ubuntu:22.04



RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

WORKDIR app

COPY . /app

RUN pip --no-cache-dir install pymongo
RUN pip --no-cache-dir install pandas
RUN pip --no-cache-dir install numpy
RUN pip --no-cache-dir install flask

CMD ["python3", "src/app.py"]