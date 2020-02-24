#!/bin/sh

image=$1
PWD=$2
echo $PWD

mkdir test_dir
mkdir -p test_dir/model
mkdir -p test_dir/output

rm test_dir/model/*
rm test_dir/output/*

docker run -v ${PWD}/test_dir:/opt/ml --rm ${image} train
