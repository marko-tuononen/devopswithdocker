FROM ubuntu:18.04
WORKDIR /usr/src/app
COPY curler.sh .
RUN apt update && apt install --yes curl
CMD ./curler.sh
