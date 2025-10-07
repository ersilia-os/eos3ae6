from whales.ChemTools import prepare_mol_from_sdf
from whales import do_whales
import whales.ChemTools as tools

import csv
import os, sys
import json
import struct
import pandas as pd
from rdkit.Chem import PandasTools
import numpy as np
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))

SDF_FILE = "act.sdf"

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

# functions to read and write .csv and .bin files
def read_smiles_csv(in_file): # read SMILES from .csv file, assuming one column with header
  with open(in_file, "r") as f:
    reader = csv.reader(f)
    cols = next(reader)
    data = [r[0] for r in reader]
    return cols, data

def read_smiles_bin(in_file):
  with open(in_file, "rb") as f:
    data = f.read()

  mv = memoryview(data)
  nl = mv.tobytes().find(b"\n")
  meta = json.loads(mv[:nl].tobytes().decode("utf-8"))
  cols = meta.get("columns", [])
  count = meta.get("count", 0)
  smiles_list = [None] * count
  offset = nl + 1
  for i in range(count):
    (length,) = struct.unpack_from(">I", mv, offset)
    offset += 4
    smiles_list[i] = mv[offset : offset + length].tobytes().decode("utf-8")
    offset += length
  return cols, smiles_list

def read_smiles(in_file):
  if in_file.endswith(".bin"):
    return read_smiles_bin(in_file)
  return read_smiles_csv(in_file)

def write_out_csv(results, header, file):
  with open(file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for r in results:
      writer.writerow(r)

def write_out_bin(results, header, file):
  arr = np.asarray(results, dtype=np.float32)
  meta = {"columns": header, "shape": arr.shape, "dtype": "float32"}
  meta_bytes = (json.dumps(meta) + "\n").encode("utf-8")
  with open(file, "wb") as f:
    f.write(meta_bytes)
    f.truncate(len(meta_bytes) + arr.nbytes)
  m = np.memmap(
    file, dtype=arr.dtype, mode="r+", offset=len(meta_bytes), shape=arr.shape
  )
  m[:] = arr
  m.flush()

def write_out(results, header, file):
  if file.endswith(".bin"):
    write_out_bin(results, header, file)
  elif file.endswith(".csv"):
    write_out_csv(results, header, file)
  else:
    raise ValueError(f"Unsupported extension for {file!r}")

# read input
_, smiles_list = read_smiles(input_file)

df = pd.DataFrame({"smiles":smiles_list})


tmp_folder = tempfile.mkdtemp()
sdf_file = os.path.join(tmp_folder, SDF_FILE)
if "smiles" in df.columns:
    PandasTools.AddMoleculeColumnToFrame(df,'smiles','molecule')
PandasTools.WriteSDF(df, sdf_file, molColName='molecule', properties=list(df.columns))

mols = prepare_mol_from_sdf(sdf_file) # computes 3D geometry from a specified sdf file


with open(os.path.join(ROOT, "labels.csv"), "r") as f:
    lab = []
    for l in f:
        lab += [l.rstrip()]

whales_library = []
for mol in mols:
    try:
        whales_temp, _ = do_whales.whales_from_mol(mol)
    except:
        whales_temp = None
    whales_library.append(whales_temp)

R = []
for r in whales_library:
    if r is None:
        r = [""]*len(lab)
    R += [r]

# write output in a .csv file
write_out(R, lab, output_file)
