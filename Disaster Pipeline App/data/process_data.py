import sys
#basic library
import pandas as pd
#SQL library
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
   """
   Load csv files of disaster categories and messages specified by python 
   command  `python data/process_data.py data/disaster_messages.csv 
   data/disaster_categories.csv data/DisasterResponse.db`, by the first two
   arguments.
    
   Input: messages_filepath: path of messages('disaster_messages.csv')
        categories_filepath: path of categories('disaster_categories.csv')
   Return: df: concatenated dataframe of messages and categories 
   """
   # read csv files 
   messages=pd.read_csv(messages_filepath)
   categories=pd.read_csv(categories_filepath)
    
   # merge and return datasets
   df=pd.merge(messages, categories, how='left', on='id')
   return df



def clean_data(df):
   """
   Three processed seal in clean_data function:
   1. Label the message categories
   2. Merge category 2 into category 1
   3.Drop the duplicates
    
   Input: df: concatenated disaster dataframe from load_data()
   Return: df: clean disaster dataframe
   """
   # split category names from categories column and extract category names
   categories = df['categories'].str.split(pat=';', expand=True)
   categories.columns = categories.iloc[0,:].apply(lambda x: x[:-2])

   # pick the last number to mark the alert and restrict int range
   for column in categories:
        categories[column] = categories[column].str[-1].astype(int)
   categories=categories.clip(0,1)
    
   # concatenate df with expanded disaster message columns
   # remove old categories column
   # drop duplicates and return dataframe
   df = pd.concat((df, categories), axis=1).drop('categories', axis=1).drop_duplicates()
    
   return df

def save_data(df, database_filename):
    """
    Store dataset into SQLite database
    
    Input: df: clean disaster dataframe
        database_filename: file name of database file
   
    """
    
    # create SQLite database to save dataframe to SQLite
    engine = create_engine('sqlite:///'+database_filename)
    df.to_sql('disaster_messages', engine, if_exists='replace', index=False)
    engine.dispose()

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()