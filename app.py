from utils import FirebaseApi, camera
from dotenv import dotenv_values
import time
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px



config = dotenv_values(".env")
api = FirebaseApi(config['creds_file'],
       config['db_url'], config['location_id'])


cupsin, cupsout = api.visualize()
print(cupsin)
print(cupsout)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart')
def chart1():
    cupsin, cupsout = api.visualize()
    df = pd.DataFrame({
        "Cups": ["Cupin", "Cupsout"],
        "Amount": [cupsin, cupsout],
    })
    fig = px.bar(df, x="Cups", y="Amount", barmode="group")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Cups Status"
    description = """
    Cup Status and measurements inside UWCSEA dover
    """
    return render_template('chart.html', graphJSON=graphJSON, header=header,description=description)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/style.css')
def style():
    return render_template('style.css')

@app.route('/script.js')
def script():
    return render_template('script.js')

