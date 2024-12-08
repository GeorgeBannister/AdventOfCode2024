#!/usr/bin/env bash

set -eux

mkdir $1

cp template.py $1/main.py
touch $1/inp.txt
