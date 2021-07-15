FROM alpine

ENV REACT_APP_BACKEND_URL=http://localhost:8080
EXPOSE 5000

RUN apk add --no-cache curl npm && \
    curl -sL https://deb.nodesource.com/setup_14.x && \
    apk add nodejs && \
    apk del curl && \ 
    rm -rf /var/lib/apt/lists/*     

WORKDIR /usr/src/app 
COPY . .

RUN npm install && npm run build && npm install -g serve && \
    adduser --disabled-password appuser && chown appuser .
USER appuser

CMD ["serve", "-s", "-l", "5000", "build"]
