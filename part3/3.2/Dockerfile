FROM ubuntu

RUN apt-get update -qq && apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    curl \
    git \
    lxc \
    iptables
    
RUN curl -sSL https://get.docker.com/ | sh

COPY doit.sh .
CMD bash doit.sh
