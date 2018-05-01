docker build -t godmc-api .
docker rm -f godmc-api
docker run -d --name godmc-api -p 8081:80 godmc-api

