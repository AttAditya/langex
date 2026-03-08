#!/bin/bash

set +e
dir=""

while [ true ]; do
  dir=$dir/*
  ls .$dir/__pycache__
  
  if [ $? -ne 0 ]; then
    echo "No __pycache__ directories found."
    exit 0
  fi
  
  rm -rf .$dir/__pycache__
done

