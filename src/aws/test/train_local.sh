#!/bin/sh

image=$1
PWD=$2
echo $PWD

docker run -v ${PWD}/local_test/test_dir:/opt/ml --rm ${image} train
