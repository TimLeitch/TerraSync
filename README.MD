## Docker commands
### Build image
docker run --name mongodb-test -d -p 27017:27017 mongo
docker build -t node-mongo .    