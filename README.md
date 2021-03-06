# docker-solubility
Docker for reproducing machine learning solubility models.

## Install Docker
To run model please [install docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

### Install from Docker
```
docker run --rm -v /PATH/TO_FILE/YOU_WANT_TO_WORK_ON/:/data rodrigozepeda/docker-solubility
```
where:

* ``/PATH/TO_FILE/YOU_WANT_TO_WORK_ON/`` is substituted by path to the csv file conaining the Smiles you want to predict (see [To_predict.csv on Github](https://github.com/RodrigoZepeda/docker-solubility-v1/blob/master/predict_files/To_predict.csv) for an example).
* Included models can be specified as:
  + ``GraphConv``
  + ``Weave``
  + ``MPNN``
  + ``DAG``
  + ``RandomForest`` [Random forest model](https://github.com/RodrigoZepeda/docker-solubility/blob/master/data_analysis/model_data_sheets/RandomForest.md). 
  + ``KRR``
  + ``XGBoost``
  + ``TextCNN``   **WORKS BUT THROWS ERROR**

As an example, assuming the files to predict are included in ``~/Dropbox/predict_files`` and you want the Graph Convolution model you can:
```
sudo docker run --rm -v ~/Dropbox/predict_files:/data docker-solubility GraphConv
```

See [manual for further instructions](https://github.com/RodrigoZepeda/docker-solubility-v1/blob/master/Manual.md)  
