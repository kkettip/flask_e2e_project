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

app = Flask(__name__)

# Load the dataset
url = 'https://raw.githubusercontent.com/kkettip/datasci_4_web_viz/main/Datasets/PLACES__Local_Data_for_Better_Health__County_Data_2023_release%20%20CT.csv'
df = pd.read_csv(url)
df_obesity = df[(df['MeasureId'] == 'OBESITY') & (df['Data_Value_Type'] == 'Age-adjusted prevalence')]

@app.route('/', methods=['GET', 'POST'])
def index():
    counties = sorted(df_obesity['LocationName'].unique())
    selected_county = request.form.get('county') or counties[0]
    
    img = create_plot(selected_county)

    today = datetime.today().strftime('%Y-%m-%d')
    
    return render_template("index.html", counties=counties, selected_county=selected_county, img=img, today=today)


    
    

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

if __name__ == '__main__':
    app.run(debug=True)