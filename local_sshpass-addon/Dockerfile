FROM alpine:3.15

# Installiere sshpass, openssh-client, Python3 und pip
RUN apk update && apk add --no-cache sshpass openssh-client python3 py3-pip

# Installiere paho-mqtt über pip
RUN pip3 install paho-mqtt

# Kopiere das Start-Skript und das Trigger-Script ins Image
COPY run.sh /run.sh
COPY trigger.py /trigger.py

# Stelle sicher, dass beide Skripte ausführbar sind
RUN chmod +x /run.sh /trigger.py

# Beim Containerstart wird das Run-Skript ausgeführt
CMD [ "/run.sh" ]
