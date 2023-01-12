#!/bin/bash
# Read the template file
TEMPLATE=$(<"configtemplate.json")
# Substitute the variables in the template with the provided values
OUTPUT="$TEMPLATE"
for VAR in $(grep -o "\${[^}]*}" "configtemplate.json" | sed 's/[${}]//g'); do
  read -p "Enter value for $VAR: " VALUE
  OUTPUT="${OUTPUT//\$\{$VAR\}/$VALUE}"
done
# Write the output to the specified file
echo "$OUTPUT" > "config.json"
