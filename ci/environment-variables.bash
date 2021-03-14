#!/bin/bash

set -ev

echo "github.event_name: ${GITHUB_EVEN_NAME}"
echo "matrix.os: ${OS_NAME}"
echo "matrix.arch: ${CPU_ARCH}"
