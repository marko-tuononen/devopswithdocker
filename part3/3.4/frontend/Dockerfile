FROM ubuntu:16.04 
EXPOSE 5000

RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash && \
    apt install -y nodejs && \
    apt-get purge -y --auto-remove curl && \ 
    rm -rf /var/lib/apt/lists/*     

WORKDIR /usr/src/app 
COPY . .

ENV REACT_APP_BACKEND_URL=http://localhost:8080
RUN npm install && npm run build && npm install -g serve && \
    useradd -m appuser && chown appuser .
USER appuser

CMD ["serve", "-s", "-l", "5000", "build"]
