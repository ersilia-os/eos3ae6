import pandas as pd
from rdkit import Chem
from rdkit.Chem.rdmolfiles import SDWriter

df = pd.read_csv("data/osm_clf.csv")
mols = [Chem.MolFromSmiles(x) for x in list(df["smiles"])]

with SDWriter('data/all_s4.sdf') as w:
    for m in mols:
        w.write(m)
