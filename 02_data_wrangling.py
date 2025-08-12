max_entries: int = 1000000                # Amount of molecules downloaded from the script "01_Data_Download"

import pandas as pd

# Read in data
chembl_data = pd.read_csv("chembl_molecules.csv")

#Check data
chembl_data.info()

# Remove repeated column names (originated due to nested data)
chembl_data.columns = [col.replace("molecule_properties.", "").replace("molecule_structures.", "") for col in chembl_data]

# How much churn was in the import?
print(f"\n\tOut of {max_entries} just {len(chembl_data["molecule_chembl_id"])} had sufficient data for this data analysis.")

# How many actual drug are in the data set?
is_drug =chembl_data[chembl_data['max_phase'] == 4]
# print(is_drug)
print(f"Out of {max_entries} {len(is_drug)} are approved drugs.")

# Assign 'is drug' label
chembl_data['is_drug'] = chembl_data['max_phase'] == 4

# Assign Lipinski rules for oral availability of drug molecules
# Any drug that is oral available shouldnt violate then 2 rules

# chembl_data.info()
# Filter 1 - Molecular weight <= 500 Da
chembl_data['Rule_mwt'] = chembl_data['full_mwt'] <= 500

# Filter 2 - Number of hydrogen bond acceptors (HBA) <= 10
chembl_data['Rule_hba'] = chembl_data['hba'] <= 10

# Filter 3- Number of hydrogen bond donors <= 5
chembl_data['Rule_hbd'] = chembl_data['hbd'] <= 5

# Filter 4 - clop P <= 5
chembl_data['Rule_alogp'] = chembl_data['alogp'] <= 5

# Save tidy data
chembl_data.to_csv('chembl_data_tidy.csv', index = False)