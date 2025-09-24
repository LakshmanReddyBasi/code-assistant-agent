import nbformat
import json

# Replace 'input.json' with your file path
input_file = 'input.json'
# Replace 'output.ipynb' with your desired output file path
output_file = 'output.ipynb'

# Read the JSON data with UTF-8 encoding
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        json_content = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from '{input_file}': {e}")
    exit()

# Create a new notebook object
notebook = nbformat.v4.new_notebook()

# A list to store the properly formatted cell objects
cells_to_add = []

# Logic to handle different JSON structures
if isinstance(json_content, list):
    # Case: The JSON is a list. Assume each item is content for a code cell.
    print("Detected JSON as a list. Treating each item as a code cell source.")
    for item in json_content:
        # Check if the item is a dictionary with a 'source' key
        if isinstance(item, dict) and 'source' in item:
            # If the item is already a cell-like dictionary, use its source
            cell_source = item['source']
        else:
            # Otherwise, assume the item is the source content itself
            cell_source = item
        cells_to_add.append(nbformat.v4.new_code_cell(str(cell_source)))
elif isinstance(json_content, dict) and "cells" in json_content:
    # Case: The JSON file is already a valid notebook structure.
    print("Detected JSON as a notebook structure with 'cells' key.")
    cells_to_add = json_content['cells']
else:
    print("Unsupported JSON format. Assuming the content is for a single code cell.")
    cells_to_add.append(nbformat.v4.new_code_cell(json.dumps(json_content, indent=2)))

# Assign the processed cells to the notebook
notebook['cells'] = cells_to_add

# Write the notebook to an .ipynb file
with open(output_file, 'w', encoding='utf-8') as f:
    nbformat.write(notebook, f)

print(f"\nSuccessfully converted '{input_file}' to '{output_file}'")