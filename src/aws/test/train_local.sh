#!/bin/sh

image=$1
PWD=$2
container_name=$3

docker run -v ${PWD}/local_test/test_dir:/opt/ml --name ${container_name} ${image} train

docker logs ${container_name} >> ${PWD}/local_test/test_dir/output/train_logs.txt

docker container rm ${container_name}