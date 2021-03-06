# -*- coding: utf-8 -*-
"""
Functions for predicting expected solubility
Rodrigo Zepeda

Adapted from:
https://github.com/PatWalters/solubility/blob/master/solubility_comparison.py
"""

import pandas as pd
import sys
import warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Hide tensorflow warnings

#Importing deepchem throws a numpy warning
sys.stderr = None            # suppress deprecation warning
import deepchem as dc
sys.stderr = sys.__stderr__  # restore stderr

from deepchem.utils.save import load_from_disk
from rdkit import Chem

def load_model(modelname, model_file, modeltype = "tensorflow"):
    #Read model file
    try:
        if modeltype == "tensorflow":
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore",category=Warning)
                model = modelname.load_from_dir(model_file)
            return model
        elif modeltype == "sklearn" or modeltype == "xgboost":
            modelname.reload()
            return modelname
        else:
            sys.exit("Invalid model type")
    except:
        sys.exit('Unable to find' + modelname + ' at ' + model_file)

def load_data(dataset_file, smiles_column = "Smiles"):
    #Read dataset to predict
    try:
        newsmiles = pd.read_csv(dataset_file)
    except:
        sys.exit('Unable to read ' + dataset_file + 'from "/data" directory')

    #Search for smiles column
    try:
        mols = [Chem.MolFromSmiles(s) for s in newsmiles.loc[:,smiles_column]]
    except:
        sys.exit('Unable to read ' + smiles_column + ' column from ' + dataset_file)

    return newsmiles, mols

def predict_from_mols(featurizer, transformers, mols, model, molnames, dirpath, isdag = False, istextcnn = False):

    #Featurize data
    ftdata = featurizer.featurize(mols)

    #Predict data
    #FIXME fiz hacks
    if isdag:
        #HACK for predicting the DAG model
        ftdata = dc.data.datasets.NumpyDataset(ftdata)
        ftdata = transformers.transform(ftdata)
        predicted_solubility = model.predict(ftdata)

    elif istextcnn:

        #HACK for predicting the  textcnn model
        import numpy as np

        newsmiles = [Chem.MolToSmiles(s) for s in mols]
        mydata = pd.DataFrame({'smiles': newsmiles, 'tasks': np.ones((1,len(newsmiles))).flatten()  })
        mydata.to_csv(dirpath + "temp.csv",index=False)
        loader = dc.data.CSVLoader(
              tasks=["tasks"],
              smiles_field="smiles",
              featurizer=featurizer)
        dataset = loader.featurize(dirpath + "temp.csv")

        # Initialize transformers
        transformers = [
              dc.trans.NormalizationTransformer(
                  transform_y=True, dataset=dataset)
        ]

        for transformer in transformers:
           dataset = transformer.transform(dataset)

        predicted_solubility = model.predict(dataset)
        #os.remove("temp.csv")

    else:
        predicted_solubility = model.predict_on_batch(ftdata)

    #Convert to dataframe
    mydf = pd.concat([molnames, pd.DataFrame(predicted_solubility)], axis = 1)
    mydf.columns = ["Smile","Predicted Solubility"]

    return mydf

def write_to_csv(fname, parentdir, mydf, newdir):

    dirpath = parentdir + newdir
    #Create new directory
    #https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    #Write dataset
    try:
        mydf.to_csv(dirpath + "/" + fname, index=False)
        print('     Model saved as "' + fname + '" on\n         "' +
            dirpath +  '" directory', flush = True)
    except:
        sys.exit('Unable to save "' + fname + '" on "'+ dirpath +  '" directory')

    return 0

def predict_csv_from_model(featurizer, transformers, modelname, model_file,
    dataset_file, fname, smiles_column = 'Smiles', parentdir = '/data/',
    newdir = "predictions", modeltype = "tensorflow", isdag = False, istextcnn = False):

    #Load model
    model = load_model(modelname, model_file, modeltype)

    #Load data
    newsmiles, mols = load_data(dataset_file, smiles_column)

    #Predict dataset
    predict_df = predict_from_mols(featurizer, transformers, mols, model, newsmiles, dataset_file, isdag, istextcnn)

    #Write to csv
    write_to_csv(fname, parentdir, predict_df, newdir)

    return 0
