#!/usr/bin/env bash

if [ ! -d LICENSE ]; then
  echo "Sorry, you need to run that from where your LICENSE is."
  exit 1
fi

echo "find true tests to perform"
