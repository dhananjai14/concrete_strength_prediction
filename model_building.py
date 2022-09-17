"""
This is the Entry point for Training the Machine Learning Model.
"""

from Logger import logger
from BuildModel import train_model
from Model_save import ModelSave
from DataPreprocessing import train

import traceback


class trainModel:
    def __init__(self):
        try:
            self.log = logger.logs()
            self.log.write_log('model_building', 'inside the class "trainModel".')

        except:
            self.log.write_log('model_building', traceback.format_exc(), 'error')

    def trainingModel(self):
        try:
            self.log.write_log('model_building', 'inside the method "trainingModel"')
            self.log.write_log('model_building', 'preprocessing started')
            # Preprocessing
            preprocess = train.train_preprocess(
                r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv')
            preprocess.fill_na_value()
            cluster_count = preprocess.find_best_clusters()
            preprocess.KMeanCluster_model()
            preprocess.create_cluster()
            self.log.write_log('model_building', 'Cluster created')
            self.log.write_log('model_building', 'preprocessing Ended')

            self.log.write_log('model_building', 'Model building Started')
            model = train_model.modelFinder()
            data_train, data_test = model.train_test_split(
                r'C:\Users\preet\Desktop\DS\Project\Concrete Project\Clustered Data\training\clustered_cement.csv')

            for i in range(cluster_count):
                data_train_cluster = data_train[data_train['clusters'] == i]
                data_test_cluster = data_test[data_test['clusters'] == i]
                data_train_x, data_train_y = model.x_y_split(data_train_cluster)
                data_test_x, data_test_y = model.x_y_split(data_test_cluster)

                best_model = model.get_best_model(data_train_x, data_train_y, data_test_x, data_test_y)
                save = ModelSave.model_load()
                save.to_save(best_model, "model_cluster_{}".format(i))
            # logging the successful Training
            self.log.write_log('model_building', 'Successful end of model building')
            self.log.write_log('model_building', 'Successful end of training')
            return None

        except:
            # logging the unsuccessful Training
            self.log.write_log('model_building', 'Unsuccessful model building process', 'error')
            self.log.write_log('model_building', traceback.format_exc(), 'error')
            return traceback.format_exc()


# a = trainModel()
# a.trainingModel()
