import pandas as pd
import traceback
from sklearn.impute import KNNImputer
from Logger import logger
from Model_save import ModelSave


class predict_preprocess:
    def __init__(self,path):
        try:
            self.log = logger.logs()
            self.log.write_log('PredictProcessing', 'inside the class "predict_preprocess"')
            self.predict_path = path
            self.log.write_log('PredictProcessing', 'path of predict preprocess data {}'.format(self.predict_path))
        except:
            self.log.write_log('PredictProcessing', traceback.format_exc(), 'error')

    def fill_na_value(self):
        try:
            data = pd.read_csv(self.predict_path)
            columns = data.columns

            self.log.write_log('PredictProcessing' , "inside the fill na values method")
            imputer = KNNImputer(n_neighbors = 3, weights= 'uniform')
            new_data = imputer.fit_transform(data)
            self.log.write_log('PredictProcessing' , "null values imputed")
            new_data = pd.DataFrame(new_data, columns=columns)
            self.log.write_log('PredictProcessing' , "New dataframe created")
            new_data.to_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv', index = False)
            self.log.write_log('PredictProcessing' , "New data saved into cement.csv")
        except:
            self.log.write_log('PredictProcessing' , traceback.format_exc() , 'error')
            return traceback.format_exc()

    def create_cluster(self):
        try:
            self.log.write_log('predictPreprocessing', 'inside the "create cluster" method')
            data = pd.read_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv')
            self.log.write_log('predictPreprocessing', 'Data loaded')

            model = ModelSave.model_load()
            model = model.to_load('kmean')
            self.log.write_log('predictPreprocessing', 'KMean model loaded')
            clusters = model.predict(data)
            data['clusters'] = clusters
            self.log.write_log('predictPreprocessing', 'created cluster')
            data.to_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\Clustered Data\predict\clustered_cement.csv', index = False)
            self.log.write_log('predictPreprocessing', r'Data set with clusters loaded into the "Clustered Data\predict\clustered_cement.csv"')

        except:
            self.log.write_log('predictPreprocessing' , traceback.format_exc(), 'error')
            return print(traceback.format_exc())


# a = predict_preprocess(r"C:\Users\preet\Desktop\DS\Project\Concrete Project\Data to Predict\cement.csv")
# a.fill_na_value()
# a.create_cluster()


