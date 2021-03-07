#!/bin/bash
BIN_NAME=update_aws_sg-${OS_NAME}-${CPU_ARCH}.bin
DIST_FILE=update_aws_sg

mkdir -p ~/.cache/pip/wheels

set -ev


echo "Installing pyinstaller"
pip install pyinstaller

echo chowning pip wheels directory
chown -Rv $USER:$GROUP ~/.cache/pip/wheels

pyinstaller --log-level=DEBUG --onefile ./update_aws_sg.py

if [[ $OS_NAME == "windows-latest" ]]; then
    DIST_FILE=update_aws_sg.exe
    BIN_NAME=update_aws_sg-${OS_NAME}-${CPU_ARCH}.exe
fi

if [[ -f ./dist/${DIST_FILE} ]]; then
    cp ./dist/${DIST_FILE} ./dist/${BIN_NAME}
fi

echo Binary copied: 
ls -l ./dist/${BIN_NAME}

echo "::set-output name=BIN_NAME::${BIN_NAME}"
