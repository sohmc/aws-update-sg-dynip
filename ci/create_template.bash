#!/bin/bash -u
TEMP_FILE=./aws_sg_ddns.conf
SED_OPTIONS='-i'

cd ci/

if [[ -f ${TEMP_FILE} ]]; then
    rm ${TEMP_FILE}
fi

if [[ ${OS_NAME} == "macos-latest" ]]; then
    echo "Setting sed options for osx"
    SED_OPTIONS='-i "" -e '
fi

echo "Creating copy of the template..."
cp ./aws_sg_ddns-template.conf ${TEMP_FILE}

if [[ -z "${SG}" ]]; then
    echo "SG not set.  Exiting..."
    exit 1;
else
    echo "Adding Security Group..."
    sed ${SED_OPTIONS} "s/\$SG/${SG}/" ${TEMP_FILE}
fi;

