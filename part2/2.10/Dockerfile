FROM ubuntu:16.04 
EXPOSE 5000

RUN apt-get update && apt-get install -y curl 
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash
RUN apt install -y nodejs

WORKDIR /usr/src/app 
COPY . .

RUN npm install
RUN npm run build
RUN npm install -g serve

CMD ["serve", "-s", "-l", "5000", "build"]
