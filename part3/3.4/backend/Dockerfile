FROM golang:1.16
EXPOSE 8080

WORKDIR /usr/src/app
COPY . .

RUN go build && go test ./... && \
    useradd -m appuser && chown appuser .

ENV REQUEST_ORIGIN="http://localhost:5000"

USER appuser

CMD ["./server"]
