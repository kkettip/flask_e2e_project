FROM python:3.10-slim-buster
#base image obtained from Docker Hub that will be updated. This base image has Linux operating system underneath.
WORKDIR /app
#create new folder call app
COPY . /app/
#takes app.py, requirements.txt and docker file and put them in an application folder in the virtual operating system.
RUN pip install -r requirements.txt
#installing required packages included in requirements.txt
EXPOSE 5000
#running on port 5000
CMD ["python", "app.py"]
#applications that we want Docker to run

#change web preview port to the required port in google terminal to preview the app
#images need to be rebuild everytime changes are made

#Docker Commands
# To build docker image: docker build -t <name of image> . name of image: flaskapp1
# To list the images: docker images
# To run image: docker run -d -p 5001:5000 <name of image> (docker run -p <host-port>:<container-port> <image-name>)
# To get container ID and to see the containers that are running: docker ps
# To stop the container: docker stop <container id from list displayed by docker ps command>
# To remove a container: docker rm <container-id>
# To delete all containers: docker system prune -a -f 
 