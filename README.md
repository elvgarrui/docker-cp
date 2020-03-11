# DOCKER-CP

## Install instructions:

 ```$ pip install -r requirements.txt```

 ```$ pip install .```

## Usage:
  
  ```$ docker run -d --name test fedora:25 /usr/bin/sleep ```

  ```$ docker-cp --buffer-length=4 test:/etc/fedora-release .```
  
  ```$ docker-cp --buffer-length=4  READNE.md test:/home/```