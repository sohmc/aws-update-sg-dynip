#!/bin/bash
BIN_NAME=./dist/${BIN_NAME}

echo "Testing ${BIN_NAME}"

set -ev

# echo "Getting binary from S3..."
# curl -v $S3_URI -o $BIN_NAME

echo "Building template..."
bash ci/create_template.bash

echo "Running script..."
${BIN_NAME} -f -c ci/aws_sg_ddns.conf
