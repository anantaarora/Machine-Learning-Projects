# Import packages
import configparser
import luigi
import pandas
import os
from feature_builder import FeatureBuilder
from model_builder import train_random_forest
import pickle
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


config = configparser.ConfigParser()
config.read('luigi.cfg')

# Defining module TrainDataIngestion

class TrainDataIngestion(luigi.Task):

#define run to read the csv file

    def run(self):
        df_data = pandas.read_csv(config.get('Paths','train-data-path'))
        df_data.to_csv(self.output().path, index=False)

#define output to save the imported file to temp folder

    def output(self):
        return luigi.LocalTarget(config.get('Paths','TrainDataIngestion-out'))

# Defining DataPreProcessing module

class DataPreProcessing(luigi.Task):

# define require to callback the TrainDataIngestion

    def requires(self):
       return TrainDataIngestion()

# define run to do implement the featureBuilder for data pre pricessing

    def run(self):
        fb = FeatureBuilder(pandas.read_csv(TrainDataIngestion().output().path))
        dataframe = fb.featurize()
        print("In Data Pre Processing")
        print(dataframe.columns)
        dataframe.to_csv(self.output().path, index=False)

# define output to save the processed data

    def output(self):
        return luigi.LocalTarget(config.get('Paths','DataPreProcessing-out'))

# Defining Train module

class Train(luigi.Task):

    def requires(self):
        return DataPreProcessing()

    def run(self):
        value_model = train_random_forest(pandas.read_csv(DataPreProcessing().output().path))
        with open(self.output().path, 'wb') as f:
            pickle.dump(value_model,f )
        request = Request(config.get('Paths','Load-Model-To-Flask-API'))
        try:
            print("Reloading models")
            response = urlopen(request)
        except URLError as e:
            "No Status Prediction", e



    def output(self):
        return luigi.LocalTarget(config.get('Paths','Train-out'))


if __name__ == '__main__':
    luigi.run()
