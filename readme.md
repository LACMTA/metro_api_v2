# Metro API v2
Metro API v2 is an API for Metro's GTFS-RT data.

## Getting started

### Prerequistes

- Docker installed

### Local Deployment

Below is the shell script that can run to get started with the repository locally.

``` shell
# clone the repository
git clone https://github.com/LACMTA/metro_api_v2.git

#change to the directory
cd docker-fastapi-projects-nginx

# creates image in current folder with tag nginx
docker build . -t nginx

# runs nginx image
docker run --rm -it  -p 80:80/tcp nginx:latest
```
