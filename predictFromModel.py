import pandas as pd
from Logger import logger
from DataPreprocessing import predict
from Model_save import ModelSave
import traceback


class prediction:
    def __init__(self):
        try:
            self.log = logger.logs()
            self.log.write_log('prediction', 'inside the class "prediction".')
        except:
            self.log.write_log('prediction', traceback.format_exc(), 'error')

    def predictionFromModel(self):
        try:
            self.log.write_log('prediction', 'inside the method "predictionFromModel"')
            self.log.write_log('prediction', 'preprocessing started')
            # Preprocessing
            preprocess = predict.predict_preprocess(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv')
            preprocess.fill_na_value()
            preprocess.create_cluster()
            self.log.write_log('prediction', 'preprocessing ended')

            self.log.write_log('prediction', 'Prediction started')
            file_opn = ModelSave.model_load()
            cluster_count = file_opn.to_load('cluster')
            data = pd.read_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\Clustered Data\predict\clustered_cement.csv')
            final_data = pd.DataFrame()
            for i in range(cluster_count):
                data_predict_cluster = data[data['clusters'] == i]
                model = file_opn.to_load('model_cluster_{}'.format(i))
                if len(data_predict_cluster) == 0:
                    continue
                data_predict_cluster['PredictedStrength'] = model.predict(data_predict_cluster)
                final_data = pd.concat([final_data, data_predict_cluster])
            final_data.to_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\FinalPredictedData\cement.csv', index=False)

            return final_data

        except:
            # logging the unsuccessful Training
            self.log.write_log('model_building', 'Unsuccessful model building process', 'error')
            self.log.write_log('model_building', traceback.format_exc(), 'error')
            return traceback.format_exc()

# a = prediction()
# print(a.predictionFromModel())

