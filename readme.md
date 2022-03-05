# Metro API v2
Metro API v2 is an API for Metro's GTFS-RT data.

## Versioning

Metro API v2 uses a modified version of [Semantic Versioning](https://semver.org/), with major (`X`), minor(`x`), and hotfix(`*`) releases for the numbers respectively: `X.x.*`.

More versioning information can be found in [versioning.md](versioning.md)
## Getting started

### Prerequistes

- Docker installed

### Local Deployment

Below is the shell script that can run to get started with the repository locally.

``` shell
# clone the repository
git clone https://github.com/LACMTA/metro_api_v2.git

#change to the directory
cd metro_api_v2
```

Run these commands in order to build the docker container and then run it.

``` shell
# creates image in current folder with tag nginx
docker build . -t metro-api-v2:metro-api-v2

# runs metro-api-v2 image
docker run --rm -it  -p 80:80/tcp metro-api-v2:metro-api-v2
```

docker-compose stop -t 1

Use this command to run locally.

``` shell
# install the required libraries
pip3 install -r requirements.txt

# run uvicorn to serve the API
uvicorn app.main:app --reload --port 1212


```

Use this command to run uvicorn from Windows.  You may need to use Python 3.

``` bash
python -m uvicorn app.main:app --reload 
```

### Misc Commands

```
docker build -t metro-api-v2:metro-api-v2 .
docker compose up

docker tag metro-api-v2:metro-api-v2 albertkun/

metro-api-v2

docker push albertkun/metro-api-v2
```