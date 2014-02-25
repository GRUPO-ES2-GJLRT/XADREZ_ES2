#!/bin/bash
set -e

cd "$(dirname "$0")"

virtualenv --python=python2.7 --no-site-packages --distribute .
source ./bin/activate
pip install --upgrade distribute
pip install -r bootstrap/requirements.txt
