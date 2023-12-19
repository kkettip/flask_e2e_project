# flask_e2e_project


Patients’ Information Display Flask App

## Tools Used:
1. Github (Version Control)
2. Flask (Python; Frotend & Backend)
3. MySQL (Database via GCP)
4. SQLAlchemy (ORM)
5. .ENV (Environment Variables)
6. Tailwind (Frontend Styling)
7. Authorization (Google OAuth)
8. API Service (Flask Backend)
9. Logger (Debugging & Logging)
10. Docker (Containerization)
11. GCP (Deployment)


## Description and Steps to use the app:
faker is used to generate fake patients' data
(see readme and images in Docs folder)

1. Login with a google account
2. Arrive at dashboard containing user profile, links to webpages and a logout link 3
3. Select Patients Information page link or Patient Conditions page link
4. Patients Information page displays 3 tables: patients, conditions, patient_conditions.
5. Patient Conditions page displays a pie chart showing the percentage of patients with certain conditions.
6. There is an option to select a specific condition to see a cutout slice of the pie.
7. Log out

   
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


## Steps to deploy app to the cloud:

Used GCP App Engine for Web Deployment

First add app.yaml then:

In terminal input :
1. gcloud config set project <project ID>
2. gcloud auth login
3. go to browser link
4. allow cloud SDK to access google account
5. copy authorization code
6. enter authorization code
7. gcloud app deploy app.yaml
8. Web link will be provided

## MySQL GCP Instance Setup and Configuration

MySQL instance is used to store data for retrieval 

1. Log into GCP account
2. Select SQL
3. Select Create an instance
4. Select MySQL
5. Provide information for Instance
6. Adjust settings
7. In Cloud SQL Edition Section: Select Enterprise and Select Sandbox
8. In Machine configuration Select Shared core
9. In Connections select Public IP and add network 0.0.0.0/0
10. Select Create the instance


## .ENV format 

To store secret information like passwords without exposing it for others to see in code.

## MySQL DB
1. DB_HOST = os.getenv("DB_HOST") =>IP address
2. DB_DATABASE = os.getenv("DB_DATABASE") => Name of Database
3. DB_USERNAME = os.getenv("DB_USERNAME") => root (for GCP)
4. DB_PASSWORD = os.getenv("DB_PASSWORD") => PW (for root user)
5. DB_PORT = int(os.getenv("DB_PORT", 3306))
6. DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

## Oauth

For user authentication when signing in to webapps

1. GOOGLE_CLIENT_ID= ********
2. GOOGLE_CLIENT_SECRET= *********






