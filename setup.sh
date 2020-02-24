#!/bin/bash -i
pip3 install -r requirements.txt

workdir=$(pwd)
alias ml_api_tool="python3 $workdir/ml_api_tool.py"

