#!/bin/bash

set -ev

PYTHON=python

if [[ $OS_NAME != "windows" ]]; then
    PYTHON=python3
fi

echo "Building template..."
bash ci/create_template.bash

echo "Running script..."
${PYTHON} cloudflare-ddns.py -f -c ci/aws_sg_ddns.conf
