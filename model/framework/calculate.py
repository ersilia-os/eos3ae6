from whales.ChemTools import prepare_mol_from_sdf
from whales import do_whales
import whales.ChemTools as tools

import os, sys
import pandas as pd
from rdkit.Chem import PandasTools
import numpy as np
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))

SDF_FILE = "act.sdf"

data_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

df = pd.read_csv(data_file)

tmp_folder = tempfile.mkdtemp()
sdf_file = os.path.join(tmp_folder, SDF_FILE)

PandasTools.AddMoleculeColumnToFrame(df,'smiles','molecule')
PandasTools.WriteSDF(df, sdf_file, molColName='molecule', properties=list(df.columns))

mols = prepare_mol_from_sdf(sdf_file) # computes 3D geometry from a specified sdf file

whales_library = []
for mol in mols:
    whales_temp, lab = do_whales.whales_from_mol(mol)
    whales_library.append(whales_temp)

df_whales_library = pd.DataFrame(whales_library,columns=lab)

df_whales_library.to_csv(output_file, index=False)
