FROM alpine

ENV REQUEST_ORIGIN="http://localhost:5000"
EXPOSE 8080

WORKDIR /usr/src/app
COPY . .

RUN apk add --no-cache go gcc libc-dev && go build && go test ./... && \
    adduser --disabled-password appuser && chown appuser . && \
    apk del go gcc libc-dev

USER appuser

CMD ["./server"]
