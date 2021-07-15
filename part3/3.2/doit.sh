#!/bin/bash
git clone https://github.com/marko-tuononen/docker-hy.github.io
docker build -t markotuononen/devops-with-docker-task3.2:latest docker-hy.github.io
docker login
docker push markotuononen/devops-with-docker-task3.2:latest
