# Latency-Testing
CloudLab TCP Latency Testing


## To Install
```shell script
conda env create -f environment.yaml
conda activate Latency-Testing
pip install -e .
```

## To Test
```shell script
pytest -vvv -s -k test_setup 
```