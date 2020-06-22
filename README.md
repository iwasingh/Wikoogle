<br />
<p align="center">
  <a href="https://github.com/iwasingh/Wikoogle">
    <img src="https://i.imgur.com/k4ZcWB3.png" alt="Logo" width="425px">
  </a>

  <h3 align="center">Wikoogle</h3>

  <p align="center">
    The wikipedia search engine!
    <br />
    <a href="http://212.237.42.43:8080/"><strong>Demo »</strong></a>
    <br />
    <br />
  </p>
</p>

Wikoogle is a wikipedia information retrieval system (search engine)

## Installation
Alongside of other dependencies used to build the project explained below, you must need:
* [Wikipedia dumps](https://dumps.wikimedia.org/enwiki/latest/). You should pick few dumps and only ones that have `pages-articles-multistream` as a name.
  Download them and put in the `dumps` directory on the root of the project
* You will need enough RAM memory that depends on the number of dumps you want to index, you can easily run out of memory during the index or running phase.
 For example, if you have >= 3 dumps (> 3 GB decompressed) you will need at least 4 GB of ram free. On the other hand if you index a single tiny dump (from 600MB to 1.3GB decompressed), 2 GB free should be enough


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
   Be sure to give ENOUGH RAM to the container(read installation instruction at the beginning), otherwise the next step might fail
1. Run
   ```bash
   docker -ia ir_container # or the name you specified before
   cd src
   export FLASK_APP=main.py
   python -m flask run --host 0.0.0.0 --port 8888 --no-reload
   ```
   


## Usage
The usage is straightforward, you can checkout the demo online here: http://212.237.42.43:8080/ or hit the browser after you
ran the application on your computer at: [localhost:PORT](http://localhost:PORT) where `PORT` is the port you specified in the previous steps.


Wikoogle, resembles google(at least, we try): the query language is almost the same and you can configure search parameters of the models (e.g page rank, query expansion) from the ui-friendly menu

### Browser support
All major modern browser are supported:
* Chrome (>=57)
* Edge (>=16)
* Firefox (>=52)

## Screenshots
<p align="center">
  <a href="https://github.com/iwasingh/Wikoogle" target="_blank">
    <img src="https://i.imgur.com/Rgv2DQD.png" align="center" width="888px"/>
  </a>
</p>

<p align="center">
  <a href="https://github.com/iwasingh/Wikoogle" target="_blank">
    <img src="https://i.imgur.com/U0GkYuE.png" align="center" width="888px"/>
  </a>
</p>
<p align="center">
  <a href="https://github.com/iwasingh/Wikoogle" target="_blank">
    <img src="https://i.imgur.com/G4JHW77.png" align="center" width="888px"/>
  </a>
</p>


## License
[MIT](https://choosealicense.com/licenses/mit/)
