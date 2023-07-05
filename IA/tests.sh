#!/bin/bash

# Directory containing the test files
test_directory="instances-students"
executable="projP42223base/bimaru.py"

# Color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m'

# Loop through all test files with .txt extension
for test_file in $test_directory/*.txt; do
  # Get the base name of the test file (without extension)
  base_name=$(basename "${test_file%.*}")
  
  # Construct the corresponding output file name
  output_file="$test_directory/$base_name.out"

  # Execute the Python script and capture the output
  output=$(python3 "$executable" < "$test_file")

  # Compare the output with the expected output file
  if diff -q <(echo "$output") "$output_file" >/dev/null; then
    echo -e "${GREEN}"
    echo "Test $base_name passed"
    time -p (python3 "$executable" < "$test_file") >/dev/null;
    echo -e "${RESET}"
  else
    echo -e "${RED}"
    echo "Test $base_name failed"
    echo "Expected output:"
    cat "$output_file"
    echo ""
    echo "Actual output:"
    echo "$output"
    echo ""
    echo "diff:"
    diff <(echo "$output") "$output_file"
    echo -e "${RESET}"  
  fi
done
