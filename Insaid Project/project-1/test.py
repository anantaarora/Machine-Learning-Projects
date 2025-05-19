import pandas
from luigi_Pipeline import Train
from sklearn.externals import joblib
from feature_builder import FeatureBuilder
from model_builder import test_model


def test():
    df = pandas.read_csv("C:/Users/Ananta Arora/Documents/Major Project/project-1/data/test.csv")
    #df_stores = pandas.read_csv("/tmp/rossman_sales_train_stores.csv")
    #df = pandas.merge(df_test, df_stores, on='Store')
    #df["Sales"] = 0
    ml_model = joblib.load(Train().output().path)
    fb = FeatureBuilder(df)
    df = fb.featurize()
    #print(df.columns)
    test_model(df,ml_model)
    #print(test_model(df,ml_model))


if __name__ == '__main__':
    test()
