FROM ubuntu
RUN apt-get update
RUN apt-get install python3 -y
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install pysqlite3
COPY . /opt/source-code/
COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt
COPY . /tmp/
CMD [ "exec python3 application.py" ]
