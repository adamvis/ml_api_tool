#!/bin/bash -i

# python3 -m pip install --user --upgrade setuptools wheel twine
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# rm -i dist
# rm -i ml_api_tool.egg-info

# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps ml_api_tool

workdir=$(pwd)

pip3 install -r $workdir/requirements.txt
alias ml_api_tool="python3 $workdir/ml_api_tool.py"

