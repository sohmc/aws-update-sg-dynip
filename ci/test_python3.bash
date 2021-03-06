#!/bin/bash

set -ev

PYTHON=python

if [[ $OS_NAME != "windows" ]]; then
    PYTHON=python3
fi

echo "Building template..."
bash ci/create_template.bash

echo "aws secret sauce: ${AWS_SECRET_SAUCE}"

echo "Running script..."
${PYTHON} update_aws_sg.py -f -c ci/aws_sg_ddns.conf
