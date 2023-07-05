#!/bin/bash

# Directory containing the test files
test_directory="other-tests"
executable="projP42223base/bimaru.py"

# Loop through all test files with .txt extension
for test_file in $test_directory/*.txt; do
  # Get the base name of the test file (without extension)
  base_name=$(basename "${test_file%.*}")

  echo "Test $base_name"
  time -p (python3 "$executable" < "$test_file") >/dev/null;
  echo ""
  echo ""
  
done
