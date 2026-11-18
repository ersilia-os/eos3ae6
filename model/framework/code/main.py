from whales.ChemTools import prepare_mol_from_sdf
from whales import do_whales
import whales.ChemTools as tools
from ersilia_pack_utils.core import read_smiles, write_out
import os, sys
import pandas as pd
from rdkit.Chem import PandasTools
import numpy as np
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))

SDF_FILE = "act.sdf"

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

# read input
_, smiles_list = read_smiles(input_file)

df = pd.DataFrame({"smiles":smiles_list})


tmp_folder = tempfile.mkdtemp()
sdf_file = os.path.join(tmp_folder, SDF_FILE)
if "smiles" in df.columns:
    PandasTools.AddMoleculeColumnToFrame(df,'smiles','molecule')

# Molecules RDKit cannot parse are None; writing them to the SDF made the whole
# batch fail. Only valid molecules go to the SDF; invalid ones get an empty row.
valid_idx = [i for i, m in enumerate(df["molecule"]) if m is not None]
df_valid = df.iloc[valid_idx]

if len(df_valid) > 0:
    PandasTools.WriteSDF(df_valid, sdf_file, molColName='molecule', properties=list(df_valid.columns))
    mols = prepare_mol_from_sdf(sdf_file) # computes 3D geometry from a specified sdf file
else:
    mols = []


with open(os.path.join(ROOT, "labels.csv"), "r") as f:
    lab = []
    for l in f:
        lab += [l.rstrip()]

whales_valid = []
for mol in mols:
    try:
        whales_temp, _ = do_whales.whales_from_mol(mol)
    except:
        whales_temp = None
    whales_valid.append(whales_temp)

whales_library = [None] * len(df)
for i, w in zip(valid_idx, whales_valid):
    whales_library[i] = w

R = []
for r in whales_library:
    if r is None:
        r = [""]*len(lab)
    R += [r]

# write output in a .csv file
write_out(R, lab, output_file, np.float32)
