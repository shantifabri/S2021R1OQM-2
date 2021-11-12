FROM ubuntu
RUN apt-get update
RUN apt-get install python3 -y
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install pysqlite3
COPY . /opt/sourcecode/
WORKDIR /opt/sourcecode
RUN pip3 install --requirement /opt/sourcecode/requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD [ "./application.py"]
