# pip install chembl_webresource_client # install once in console

import pandas as pd
from datetime import datetime
from chembl_webresource_client.new_client import new_client

print("ChEMBL client is ready!")


# Define flattener function - unnest nested data
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Init client
molecule_client = new_client.molecule

# Open CSV in append mode
output_file = "chembl_molecules.csv"
batch_size = 1000
offset = 0
max_entries = 1000000                 # Adjust depending on system capacities

written_header = False

while offset < max_entries:         # Generate batches of 1000 molecules to not overload system
    batch = molecule_client.filter(
        molecule_type="Small molecule",
        molecule_properties__alogp__isnull=False,
        molecule_properties__hba__isnull=False,
        molecule_properties__hbd__isnull=False,
        molecule_properties__psa__isnull=False
    )[offset:offset+batch_size]     # Slice the DB "DB Entries + batch size"

    if not batch:
        break  # no more data

    # Flatten and convert
    flat_batch = [flatten_dict(mol) for mol in batch]
    df = pd.DataFrame(flat_batch)

    keep_cols = [                   # Define relevant columns for the EDA
        'molecule_chembl_id',
        'molecule_type',
        'pref_name',
        'max_phase',
        'molecule_properties.alogp',
        'molecule_properties.cx_logp',
        'molecule_properties.full_mwt',
        'molecule_properties.hba',
        'molecule_properties.hba_lipinski',
        'molecule_properties.hbd',
        'molecule_properties.hbd_lipinski',
        'molecule_properties.num_lipinski_ro5_violations',
        'molecule_properties.num_ro5_violations',
        'molecule_properties.psa',
        'molecule_properties.qed_weighted',
        'molecule_properties.ro3_pass',
        'molecule_structures.canonical_smiles',
        'molecule_structures.standard_inchi',
        'molecule_structures.standard_inchi_key'
    ]

    # Trim the DataFrame
    df = df[[col for col in keep_cols if col in df.columns]]

    # Add a timestamp column to the DataFrame
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['timestamp'] = timestamp  # Add the timestamp as a new column

    # Write to CSV
    df.to_csv(output_file, mode='a', index=False, header=not written_header)
    written_header = True

    # Print progress
    print(f"Processed batch {offset // batch_size + 1}")

    offset += batch_size