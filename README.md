# docker-solubility-v1
Docker for reproducing our solubility model.

## Install Docker
To run model please [install docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

### Install from Docker
```
docker pull rodrigozepeda/docker-solubility-v1
```

### Install from Github

To install from Github either clone or manually download project
```
 git clone https://github.com/RodrigoZepeda/docker-solubility-v1
```

Go to project directory:
```
cd docker-solubility-v1
```

Then run Docker build command
```
docker build -t docker-solubility-v1 .
```
## Run

To run interactive session:
```
docker run -it -v /PATH/TO_FILE/YOU_WANT_TO_WORK_ON/:/data docker-solubility-v1
```

where ``/PATH/TO_FILE/YOU_WANT_TO_WORK_ON/`` is substituted by path to the csv file conaining the Smiles you want to predict.
As an example, assuming the files to predict are included in ``~/Dropbox/Quimica/Docker/docker-solubility-v2/predict_files`` you can:
```
sudo docker run -it --rm -v ~/Dropbox/Quimica/Docker/docker-solubility-v2/predict_files:/data docker-solubility-v1
```

See **MANUAL**  