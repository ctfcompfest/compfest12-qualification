FROM ubuntu:18.04
RUN apt-get update && apt-get -y install python3 socat
COPY prob.py ./
COPY flag.txt ./
COPY words.txt ./
EXPOSE 2000
CMD socat TCP-LISTEN:2000,reuseaddr,fork EXEC:"python3 prob.py"
