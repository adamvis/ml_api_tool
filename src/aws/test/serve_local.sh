#!/bin/sh

image=$1
PWD=$2
model_name=$3

docker run -d -v ${PWD}/local_test/test_dir:/opt/ml -p 8080:8080 --name ${model_name} --rm ${image} serve
