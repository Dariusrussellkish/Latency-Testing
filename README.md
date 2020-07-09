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

## To Run a Latency Test
- Make sure you set the message size correctly, it defaults to 1024 bytes
    - This is in `latencytesting/parameters.py`
- Make sure you set the server IPs correctly in `tests/test_server_clinet.py`
- On each CloudLab server, set up your environment
    - Install Conda and this repo
    - Install the environment
    - Switch to the Latency-Testing environment
    - Install this module into the Latency-Testing environment
- Use `pytest -vvv -s -k test_production` on each server and wait for all clients to connect