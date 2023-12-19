# flask_e2e_project


Patients’ Information Display Flask App

## Steps to use the app:

1. Login with a google account
2. Arrive at dashboard containing user profile, links to webpages and a logout link 3
3. Select Patients Information page link or Patient Conditions page link
4. Patients Information page displays 3 tables: patients, conditions, patient_conditions.
5. Patient Conditions page displays a pie chart showing the percentage of patients with certain conditions. There is an option to select a specific condition to see a cutout slice of the pie.

## To run the app locally without Docker:
1. Use google cloud shell terminal
2. Download code from github with git clone
3. cd into correct folder and run python app.py
4. a link to view website locally would be provided (http://127.0.0.1:5000)
5. Go to link to access app


## To run the app with Docker:
1. Ensure there is a dockerfile
2. In cloudshell terminal enter the following code:
3. Build docker image with `docker build -t <name of image> . `
4. Run image with `docker run -d -p 5001:5000 <name of image>`

## Docker Commands
1. To build docker image: docker build -t <name of image> . name of image: flaskapp1
2. To list the images: docker images
3. To run image: docker run -d -p 5001:5000 <name of image> (docker run -p <host-port>:<container-port> <image-name>)
4. To get container ID and to see the containers that are running: docker ps
5. To stop the container: docker stop <container id from list displayed by docker ps command>
6. To remove a container: docker rm <container-id>
7. To delete all containers: docker system prune -a -f 


