import json

notebook_path = '/Users/vikingo/Documents/UDG/Machine Learning/Matematicas_Aplicadas_DS_Examen2_Alan_Solano.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Helper to find cell index by a snippet
def find_cell_index_by_source(nb, snippet):
    for i, cell in enumerate(nb.get('cells', [])):
        if 'source' in cell:
            source_text = "".join(cell['source'])
            if snippet in source_text:
                return i
    return -1

# Fix SARIMA fitting line
sarima_idx = find_cell_index_by_source(nb, "sarima_model.fit")
if sarima_idx != -1:
    cell = nb['cells'][sarima_idx]
    new_source = []
    for line in cell.get('source', []):
        if 'sarima_model.fit' in line:
            new_source.append(line.replace('sarima_model', 'model_sarima'))
        else:
            new_source.append(line)
    cell['source'] = new_source
    nb['cells'][sarima_idx] = cell
    print('SARIMA fitting line corrected.')
else:
    print('SARIMA fitting cell not found.')

# Save notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('Notebook Part 3 modified successfully.')
