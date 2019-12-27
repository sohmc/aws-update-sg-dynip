#!/bin/bash -u
TEMP_FILE=./aws_sg_ddns.conf

cd .travis/

if [[ -f ${TEMP_FILE} ]]; then
    rm ${TEMP_FILE}
fi

echo "Creating copy of the template..."
cp ./aws_sg_ddns-template.conf ${TEMP_FILE}

if [[ -z "${SG}" ]]; then
    echo "SG not set.  Exiting..."
    exit 1;
else
    echo "Adding Security Group..."
    sed -i "s/\$SG/${SG}/" ${TEMP_FILE}
fi;

