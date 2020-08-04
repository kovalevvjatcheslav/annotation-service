![service pipeline](https://github.com/kovalevvjatcheslav/annotation-service/workflows/service%20pipeline/badge.svg)

Run project (docker required to run the project):  
`echo <GITHUB_TOKEN> | docker login docker.pkg.github.com -u <LOGIN> --password-stdin`  
`docker-compose -f docker/docker-compose.yml up`  

The swagger specification:
https://app.swaggerhub.com/apis/kovalevvjatcheslav/annotation-service/1.0.0-oas3