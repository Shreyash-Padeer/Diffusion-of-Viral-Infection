#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <input_file> <output_file> <k> <num_instances>"
  exit 1
fi
# Check if the input file exists
pip install -r requirements.txt
INPUT_FILE=$1
OUTPUT_FILE=$2
K=$3
NUM_INSTANCES=$4

python3 src/pagerank.py "$INPUT_FILE" "$OUTPUT_FILE" "$K"