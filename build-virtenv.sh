#!/usr/bin/env bash

VENV=virtenv

if [ ! -d "${VENV}" ]; then
  echo "Creating Python3 virtual environment at ${VENV} ..."
  python3 -m venv "${VENV}"
else
  echo "Python3 virtual environment ${VENV} already exists. Skipping its creation."
fi

source "${VENV}/bin/activate"
pip install -r saw-script/deps/cryptol/cryptol-remote-api/python/requirements.txt
pip install -e saw-script/deps/cryptol/cryptol-remote-api/python/
pip install -r saw-script/saw-remote-api/python/requirements.txt
pip install -e saw-script/saw-remote-api/python/
