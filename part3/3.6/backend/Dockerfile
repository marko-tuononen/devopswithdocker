FROM alpine as build-stage

WORKDIR /usr/src/app
COPY . .

RUN apk add --no-cache go gcc libc-dev && go build && go test ./... && \
    apk del go gcc libc-dev


FROM alpine

ENV REQUEST_ORIGIN="http://localhost:5000"
EXPOSE 8080

WORKDIR /usr/src/app
COPY --from=build-stage /usr/src/app/server /usr/src/app/server

RUN adduser --disabled-password appuser && chown appuser .

USER appuser
CMD ["./server"]
