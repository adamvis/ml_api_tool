#!/bin/bash

payload=$1
output_file=$2
content=${3:-text/csv}

curl --data-binary @${payload} -H "Content-Type: ${content}" -v http://localhost:8080/invocations &> ${output_file}
