FROM alpine:3.15

# Installiere sshpass und openssh-client
RUN apk update && apk add --no-cache sshpass openssh-client

# Kopiere das Start-Skript ins Image
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
