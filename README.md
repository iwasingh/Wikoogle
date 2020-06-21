# Wikoogle

Wikoogle is a information retrieval system (search engine) to retrieve relevant wikipedia articles.

## Installation
Alongside of other dependencies used to build the project explained below, you must need:
* [Wikipedia dumps](https://dumps.wikimedia.org/enwiki/latest/). You should pick few dumps and only ones that have `pages-articles-multistream` as a name.
  Download them and put in the `dumps` directory on the root of the project


### Windows/Unix
#### Requirements
* python (>= 3.8)
* pipenv

After checking the requirements 
```
python --version
pipenv --version
```

follow these steps from the root of the project:
#### Installing dependencies
```bash
pipenv install
pipenv run  python -m nltk.downloader 'popular'
```
#### Run
1. Specify the entrypoint
    ```bash
    export FLASK_APP=main.py 
    ```
    or in Window Powershell (`Window-key + X` -> Window Powershell)
    ```bash
    $env:FLASK_APP = "main.py"
    ```
1. Run
    ```
    cd src
    pipenv run python -m flask run --host 0.0.0.0 --port PORT --no-reload
    ```
    remember to set the PORT (e.g 8888)

### Docker
As alternative to the first installation, you can install and run the project within a linux container. Be sure to have docker installed: https://docs.docker.com/get-docker/
1. Build the image `information_retrieval` (you can change the tag)
    ```bash 
    docker image build -t information_retrieval -f Dockerfile.dev .
    ```
   
   The image is based on the `python:latest` image. If the process fails due to missing image, download it with
   `docker pull python` and retry.
1. Create the container with the name `ir_container` (you can change it)
    ```bash
    docker container create -p 8888:8888 -v ${PWD}:/app -it --name ir_container information_retrieval
    ```
   
   You can change the ports mapping(8888 is the only exposed port of the image, so don't change the destination container port but only the origin host port) and the name of the container.
   
1. Run
   ```bash
   docker -ia ir_container # or the name you specified before
   cd src
   export FLASK_APP=main.py
   python -m flask run --host 0.0.0.0 --port 8888 --no-reload
   ```
   

### 
## Usage



## License
[MIT](https://choosealicense.com/licenses/mit/)
