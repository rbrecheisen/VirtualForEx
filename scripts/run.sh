#!/bin/bash

VERSION=$(cat virtualforex/src/virtualforex/resources/VERSION)

if [ "${1}" == "" ]; then

    cd virtualforex
    briefcase dev

elif [ "${1}" == "--test" ]; then

    cd virtualforex
    briefcase dev --test

elif [ "${1}" == "--exe" ]; then

    cd virtualforex
    briefcase run

elif [ "${1}" == "--build" ]; then

    rm -rf virtualforex/build
    python scripts/python/updatetomlversion.py ${VERSION}
    python scripts/python/updatetomlrequirements.py
    cd virtualforex
    briefcase create
    briefcase build

elif [ "${1}" == "--package" ]; then

    cd virtualforex
    briefcase package --adhoc-sign
fi