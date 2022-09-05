# use the golang:alpine base image
FROM golang:alpine

# set the working directory to /go/src/app
WORKDIR /go/src/app

# copy all the files from the current directory to the container working directory (e.g. `/go/src/app`)
ADD main.go .

# import dependencies using `go mod init` and build the application using `go build -o helloworld` command, where `-o helloworld` will create the binary of the application with the name `helloworld`
RUN go mod init && go build -o helloworld

# expose the port 6111
EXPOSE 6111

# start the container by invoking the binary created earlier, which is  `./helloworld`
CMD ["./helloworld"]
