from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg') # required for local development and g-shell
import matplotlib.pyplot as plt
import io
import base64

from datetime import datetime

import warnings
warnings.simplefilter("ignore", UserWarning)

from pandas import read_sql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
import sqlalchemy


from flask import Flask, render_template, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from dotenv import load_dotenv
import os
from db_functions import update_or_create_user


import logging

logging.basicConfig(
    level=logging.ERROR,
    filename="/home/kettip_kriangchaivech/flask_e2e_project/logs/logger_output.logs",
    filemode="w",
    format='%(levelname)s - %(name)s - %(message)s'
)


load_dotenv()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')


#app = Flask(__name__)

load_dotenv()  # Load environment variables from .env file

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)

# Create a database engine
db_engine = create_engine(conn_string, echo=False)





app = Flask(__name__)
app.secret_key = os.urandom(12)
oauth = OAuth(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google/')
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    ###note, if running locally on a non-google shell, do not need to override redirect_uri
    ### and can just use url_for as below
    redirect_uri = url_for('google_auth', _external=True)
    print('REDIRECT URL: ', redirect_uri)
    session['nonce'] = generate_token()
    ##, note: if running in google shell, need to override redirect_uri 
    ## to the external web address of the shell, e.g.,
    #redirect_uri = 'https://5000-cs-531176737229-default.cs-us-east1-pkhd.cloudshell.dev/google/auth/'
    redirect_uri = 'https://5000-cs-531176737229-default.cs-us-east1-vpcf.cloudshell.dev/google/auth/'
    
    
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    update_or_create_user(user)
    print(" Google User ", user)
    return redirect('/dashboard')

@app.route('/dashboard/')
def dashboard():
    user = session.get('user')
    if user:
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')





# Load the dataset
url = 'https://raw.githubusercontent.com/kkettip/datasci_4_web_viz/main/Datasets/PLACES__Local_Data_for_Better_Health__County_Data_2023_release%20%20CT.csv'
df = pd.read_csv(url)
df_obesity = df[(df['MeasureId'] == 'OBESITY') & (df['Data_Value_Type'] == 'Age-adjusted prevalence')]

@app.route('/obesity', methods=['GET', 'POST'])
def obesity():
    counties = sorted(df_obesity['LocationName'].unique())
    selected_county = request.form.get('county') or counties[0]
    
    img = create_plot(selected_county)

    today = datetime.today().strftime('%Y-%m-%d')
    
    return render_template("obesity.html", counties=counties, selected_county=selected_county, img=img, today=today)



    

def create_plot(county):
    overall_avg = df_obesity['Data_Value'].mean()
    selected_county_avg = df_obesity[df_obesity['LocationName'] == county]['Data_Value'].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(['Selected County', 'Overall Average'], [selected_county_avg, overall_avg], color=['lightcoral', 'dodgerblue'])
    ax.axhline(selected_county_avg, color='gray', linestyle='dashed', alpha=0.7)
    ax.set_ylabel('Data Value (Age-adjusted prevalence) - Percent')
    ax.set_ylim(0, 50)
    ax.set_title('Obesity Age-adjusted Prevalence Comparison')
    
    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return base64.b64encode(img.getvalue()).decode()

#if __name__ == '__main__':
    #app.run(debug=True)




@app.route('/patients_information')
def patients_information():
    query_patients = "SELECT * FROM patients limit 10"
    df_patients = read_sql(query_patients, db_engine)
    patients = df_patients.to_dict(orient='records')
   

    query_conditions = "SELECT * FROM conditions limit 10"
    df_conditions = read_sql(query_conditions, db_engine)
    conditions = df_conditions.to_dict(orient='records')

    query_patient_conditions = "SELECT * FROM patient_conditions limit 10"
    df_patient_conditions= read_sql(query_patient_conditions, db_engine)
    patient_conditions = df_patient_conditions.to_dict(orient='records')
    

    return render_template('patients_information.html', patients=patients, conditions=conditions, patient_conditions=patient_conditions)


@app.route('/conditions', methods=['GET', 'POST'])
def conditions():
    if not session.get('user'): 
        return redirect('/')
    q = """SELECT DISTINCT(condition_name) as condition_name FROM conditions"""
    df = pd.read_sql(q, db_engine)
    conditions = sorted(df['condition_name'].unique())
    selected_condition = request.form.get('filter_value') or conditions[0]
    
    img = create_condition_plot(selected_condition)

    today = datetime.today().strftime('%Y-%m-%d')
    
    return render_template(
        "plot_display.html", 
        plot_title="Percentage of Patients with Condition",
        filter_values=conditions, 
        selected_filter_value=selected_condition, 
        img=img, 
        today=today
    )


def create_condition_plot(condition):
    q = """
SELECT 
condition_name, 
COUNT(DISTINCT patient_id) AS num_patients
FROM conditions 
JOIN patient_conditions 
USING (condition_id)
GROUP BY condition_name
ORDER BY 2 DESC
"""
    df = pd.read_sql(q, db_engine)
    conditions = df.values

    # Define the data for the pie chart
    data = [x[1] for x in conditions]
    labels = [x[0] for x in conditions]
    explode = [0.1 if x==condition else 0 for x in labels]

    # Create a figure and an axes object
    fig, ax = plt.subplots()

    # Plot the pie chart with the data and parameters
    ax.pie(data, labels=labels, explode=explode, shadow=True, startangle=90, autopct="%1.1f%%")

    # Show the pie chart
    plt.show()
    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return base64.b64encode(img.getvalue()).decode()




if __name__ == '__main__':
    app.run(
        debug=True, host='0.0.0.0',
        port=5000
        )