# Disaster Response Pipeline Project

### Introduction:
This project intends to realized two important parts: analyze disaster message categories and web app visualization.

### Content
app: The folder containing javascript modules and app.py implementing Flask & Plotly to create web app.   
data: The folder containing ETL pipeline .py file and necessary .csv disaster datasets and clean dataset of disaster_category, stored in SQLite database format.   
model: The folder containg NLP and Machine Learning Pipeline .py file to process SQLite database file from data folder, with stored trained pickle file of Machine Learning model.  

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to the http location shown after command `python run.py`.
