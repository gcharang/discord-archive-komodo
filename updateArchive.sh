#!/bin/bash

until ./main.py
do
    echo "..."
    sleep 1
done
