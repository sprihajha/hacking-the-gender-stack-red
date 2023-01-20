import rdkit  # chemical power
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from typing import List
import pandas as pd  # data analysis
import numpy as np  # math
from rdkit import Chem
from rdkit.Chem import (
    AllChem,
    MACCSkeys,
    Descriptors,
    DataStructs,
)  # fingerprint and lipinsky functionality


def generate_image(mol_smi: str, width: int = 400, height: int = 400) -> str:
    """
    Generates an image of an rdkit mol represented by the given smiles.

    *THIS WILL BE GIVEN TO PARTICIPANTS*

    :param mol_smi: SMILES of mol to display
    :param width: width of the image
    :param height: height of the image
    :return: generated image as an SVG string
    """
    mol = Chem.MolFromSmiles(mol_smi)
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText().encode()


import os


def get_all_fingerprints():
    # dictionary for library of molecules with associated fingerprints
    wd = f"{os.getcwd()}/science/science/"
    # smiles
    datatable = pd.read_csv(wd + "modified2.csv")
    datatable.columns = ["SMILES", "h"]
    datatable_smiles = datatable.SMILES
    datatable_smiles_l = datatable_smiles.tolist()
    datatable_smiles_clean = [x for x in datatable_smiles_l if str(x) != "nan"]
    # or mols = [Chem.MolFromSmiles(s) for s in datatable_smiles_l]

    mols = []
    badsmiles = []
    for smiles in datatable_smiles_clean:
        if "." not in smiles:
            try:
                mol = Chem.MolFromSmiles(str(smiles))
                mols.append(mol)
            except:
                print(s)
        # take away

    cleaned_mols = [x for x in mols if str(x) != "nan"]

    # morgan (= ecfp4) fingerprints
    # maybe replace r = 2 with different numbers
    all_fps = []
    for mol in cleaned_mols:
        try:
            all_fps_ind = AllChem.GetMorganFingerprintAsBitVect(
                mol, 2, nBits=2048, useChirality=True
            )
            all_fps.append(all_fps_ind)
        except:
            print("bad mol found")
    array = [np.array(x) for x in all_fps]

    # make a new dataframe with smiles and fingerprint
    # remake the smiles since some got lost

    new_smiles = [Chem.MolToSmiles(m) for m in cleaned_mols]
    data = pd.DataFrame()
    data["SMILES"] = new_smiles
    data["FP"] = all_fps
    data["FP array"] = array

    # make it a dictionary

    datadict = data.to_dict()
    table = pd.DataFrame()
    for i, mol in enumerate(cleaned_mols):
        Chem.SanitizeMol(mol)
        table.loc[i, "MolWt"] = Descriptors.MolWt(mol)
        table.loc[i, "LogP"] = Descriptors.MolLogP(mol)
        table.loc[i, "TPSA"] = Descriptors.TPSA(mol)

    frames = [table, data]
    data_fp_and_properties = pd.concat(frames, axis=1, join="inner")
    return data_fp_and_properties, all_fps


data_fp_and_properties, all_fps = get_all_fingerprints()
# print(DATA_FP)

# this function calculates a fingerprint
def fp_generator(smi):

    mol = Chem.MolFromSmiles(smi)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048, useChirality=True)
    molecule_array = np.array(fp)
    return fp


# this function calculates similarity
def similarity_searcher(smiles_test, similarity_degree):
    scores = DataStructs.BulkTanimotoSimilarity(fp_generator(smiles_test), all_fps)
    data_fp_and_properties["SCORES"] = scores
    candidates = data_fp_and_properties[
        data_fp_and_properties["SCORES"] > similarity_degree
    ]
    return (
        candidates.groupby("SMILES")
        .apply(lambda dfg: dfg.to_dict(orient="list"))
        .to_dict()
    )

    # return candidates["SMILES"] and pass that to image-generator????


a = similarity_searcher("C=C(C)C(=O)OCCCC(=O)OCC(COC)OC", 0.4)
print(a)
ATOM_PROP_ATOM_LABEL = "atomLabel"


def generate_image(mol_smi: str, width: int = 400, height: int = 400) -> str:
    """
    Generates an image of an rdkit mol represented by the given smiles.

    *THIS WILL BE GIVEN TO PARTICIPANTS*

    :param mol_smi: SMILES of mol to display
    :param width: width of the image
    :param height: height of the image
    :return: generated image as an SVG string
    """
    mol = Chem.MolFromSmiles(mol_smi)
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText().encode()
