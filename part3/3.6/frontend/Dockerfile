FROM alpine as build-stage

RUN apk add --no-cache npm nodejs

WORKDIR /usr/src/app 
COPY . .

RUN npm install && npm run build


FROM alpine

ENV REACT_APP_BACKEND_URL=http://localhost:8080
EXPOSE 5000

COPY --from=build-stage /usr/src/app/build /usr/src/app/build

RUN apk add --no-cache npm && npm install -g serve && \
    adduser --disabled-password appuser && chown appuser .
    
USER appuser

WORKDIR /usr/src/app 
CMD ["serve", "-s", "-l", "5000", "build"]
