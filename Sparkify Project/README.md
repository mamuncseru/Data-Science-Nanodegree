# Spark ML: Sparkify User Churn Analysis and Prediction

This project aims to utilize the power of Spark to analyze user churn and classify potential loyal users of Sparkify, a simulated music streaming service.     
As modern applications involve more and more users, analyzing big data of user information brings great values for business solutions and decision-making. Churn aims to tell whether a user will continue to use your application, and user behaviors give us insights to predict user churns.      
Our dataset for analysis has a volume of 12GB, from Udacity Data Scientist Nanodegree. More detailed analysis can be found at my Medium: https://medium.com/@ankaayaliu/user-churn-exploration-spark-ml-on-sparkify-music-streaming-c6493f293bdb     

## Environment
This project is conducted on Amazon Web Services using EMR Notebook integrated with Elastic MapReduce and Pyspark kernel & sessions. It's okay to use other cloud big data carriers or local Spark sessions.

## Contents
1. Mini_sparkify_event_data.rar: Zip file of mini_sparkify_event_data.json. You can use mini dataset to go throught Sparkify_Project_Mini.ipynb.     
2. Sparkify_Project_Mini.ipynb: Jupyter Notebook of initial exploration of Sparkify dataset, containing from data exploration to modeling.
3. Sparkify_Project.ipynb: Jupyter Notebook of final version of Sparkify dataset exploration and churn prediction, containing from data exploration to modeling, corresponding to my Medium article. The full 12GB data of Sparkify is available through AWS cloud storage and address included in the file. 
