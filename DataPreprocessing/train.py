import pandas as pd
import traceback
import sklearn.metrics as metrics
from sklearn.impute import KNNImputer
from sklearn.cluster import KMeans
from Logger import logger
from Model_save import ModelSave

class train_preprocess:
    def __init__(self,path):

        try:
            self.log = logger.logs()
            self.log.write_log('TrainPreprocessing', 'inside the class "train_preprocess"')
            self.train_path = path
            self.log.write_log('TrainPreprocessing', 'path of train preprocess data {}'.format(self.train_path))
        except:
            self.log.write_log('TrainPreprocessing', traceback.format_exc(), 'error')

    def fill_na_value(self):

        try:
            data = pd.read_csv(self.train_path)
            columns = data.columns
            self.log.write_log('TrainPreprocessing' , "inside the fill na values method")
            imputer = KNNImputer(n_neighbors= 3, weights= 'uniform')
            new_data = imputer.fit_transform(data)
            self.log.write_log('TrainPreprocessing' , "null values imputed")
            new_data = pd.DataFrame(new_data, columns= columns)
            self.log.write_log('TrainPreprocessing' , "New dataframe created")
            new_data.to_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv', index = False)
            self.log.write_log('TrainPreprocessing' , "New data saved into cement.csv")
            return None
        except:
            self.log.write_log('TrainPreprocessing' , traceback.format_exc() , 'error')
            return traceback.format_exc()

    def find_best_clusters(self):

        try:
            data = pd.read_csv(self.train_path)

            self.log.write_log('TrainPreprocessing', 'inside the "KMeanCluster" method')
            cluster = []
            score = []
            for i in range(2, 13):
                labels = KMeans(n_clusters=i, random_state=200)
                cluster.append(i)
                predicted_data = labels.fit_predict(data.drop(columns= 'Strength'))
                silhouette_score = metrics.silhouette_score(data.drop(columns = 'Strength'), predicted_data , metric="euclidean")
                score.append(silhouette_score)
            silhouette_list = pd.DataFrame({'cluster': cluster , 'score': score})
            best_cluster = silhouette_list[silhouette_list['score'] == max(silhouette_list['score'])]['cluster'][0]
            self.log.write_log('TrainPreprocessing', 'Optimum amount of cluster is: {}'.format(best_cluster))
            model = ModelSave.model_load()
            model.to_save(best_cluster, 'cluster')
            self.log.write_log('TrainPreprocessing', 'cluster.sav file saved')
            return best_cluster

        except:
            self.log.write_log('TrainPreprocessing', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def KMeanCluster_model(self):

        try:
            self.log.write_log('TrainPreprocessing', 'inside the KMeanCluster method')
            no_of_cluster = ModelSave.model_load()
            no_of_cluster = no_of_cluster.to_load('cluster')
            self.log.write_log('TrainPreprocessing', 'optimum no of cluster recieved {}'.format(no_of_cluster))
            data = pd.read_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv')
            self.log.write_log('TrainPreprocessing', 'cement.csv loaded into the system')
            model_kmean = KMeans(n_clusters=no_of_cluster, random_state=200)
            model_kmean.fit(data.drop(columns = 'Strength'))

            self.log.write_log('TrainPreprocessing', 'KMean++ model build with clusters = {} and random state = 200'.format(no_of_cluster))
            save = ModelSave.model_load()
            save.to_save(model_kmean, 'kmean')
            self.log.write_log('TrainPreprocessing', 'model saved with kmean.sav')
            return None

        except:
            self.log.write_log('TrainPreprocessing', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def create_cluster(self):

        try:
            self.log.write_log('TrainPreprocessing', 'inside the "create cluster" method')
            data = pd.read_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv')
            self.log.write_log('TrainPreprocessing', 'Data loaded')

            model = ModelSave.model_load()
            model = model.to_load('kmean')
            self.log.write_log('TrainPreprocessing', 'KMean model loaded')
            clusters = model.predict(data.drop(columns = 'Strength'))
            data['clusters'] = clusters
            self.log.write_log('TrainPreprocessing', 'created cluster')
            data.to_csv(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\Clustered Data\training\clustered_cement.csv', index = False)
            self.log.write_log('TrainPreprocessing', r'Data set with clusters loaded into the "Clustered Data\training\clustered_cement.csv"')
            return None

        except:
            self.log.write_log('TrainPreprocessing' , traceback.format_exc(), 'error')
            return print(traceback.format_exc())


#
# a = train_preprocess(r"C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB\cement.csv")
# a.fill_na_value()
# cluster_cnt = a.find_best_clusters()
# print(cluster_cnt)
# a.KMeanCluster_model()
# a.create_cluster()



