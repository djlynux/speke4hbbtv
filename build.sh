#!/bin/bash

# Script to build the entire package

# Change the BUCKETNAME and TEMPLATENAME variables with your
BUCKETNAME="subinh-pkgbuild"
TEMPLATENAME="speke4hbbtv-build.template"

# Build commands
chalice package --merge-template templates/setup.template build/
aws cloudformation package --template-file build/sam.json --s3-bucket $BUCKETNAME --output-template-file build/$TEMPLATENAME