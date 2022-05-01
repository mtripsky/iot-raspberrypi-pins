#!/bin/bash
VERSION="0.1.16"
ARCH="arm32v7"
APP="iot-raspberrypi-pins"
docker buildx build -f ./Dockerfile-$APP-$ARCH -t $APP:$VERSION . --load
docker tag $APP:$VERSION mtripsky/$APP:$VERSION
docker push mtripsky/$APP:$VERSION