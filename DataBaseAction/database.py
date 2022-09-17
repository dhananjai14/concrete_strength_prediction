# Mongo DB database used
import pymongo
import pandas as pd
import os
import shutil
from Logger import logger
import traceback


class DB_define:
    def __init__(self):
        try:
            self.log = logger.logs()
            self.log.write_log('DataBase operation', 'entering into "Database" class')

            # defining the client
            self.client = pymongo.MongoClient(
                "mongodb+srv://dhan:1212@cluster0.n0zji.mongodb.net/?retryWrites=true&w=majority")
            self.log.write_log('DataBase operation', 'Client created')

            # Creating the database name
            self.db_mongo = self.client['project']
            self.log.write_log('DataBase operation', 'Created the Database "project"')
        except:
            self.log.write_log('DataBase operation', traceback.format_exc(), 'error')

    def insert_into_db(self, collection_name, folder_path = r'C:\Users\preet\Desktop\DS\Project\Concrete Project\GoodRawFolder'):
        """
        This method will insert the data into the MongoDB.

        :param collection_name:     Name of the collection
        :param folder_path:         Path of folder containing csv files that need to be loaded into Data Base.
                                    By default, GoodRawFolder is selected.
        :return: None
        """
        try:
            self.db_mongo.drop_collection(collection_name)
            self.log.write_log('DataBase operation', 'Inside the "insert into db" method')
            self.log.write_log('DataBase operation', 'Delete "{}" collection if exists'.format(collection_name))
            path = folder_path
            self.log.write_log('DataBase operation', 'data selected from GoodRawFolder')
            files = os.listdir(path)

            final_DF = pd.DataFrame()
            for file in files:
                self.log.write_log('DataBase operation', '{} is read'.format(file))
                file = path + '\\' + file
                a = pd.read_csv(file)
                final_DF = pd.concat([final_DF, a]).reset_index(drop=True)
                self.log.write_log('DataBase operation', 'File successfully loaded into the dataframe')
            self.log.write_log('DataBase operation', 'Single data frame created for all files in GoodRawFolder')
            mongo_dict = final_DF.to_dict(orient='records')
            self.log.write_log('DataBase operation', 'Converted data frame to Dictionary')

            coll = self.db_mongo[collection_name]
            self.log.write_log('DataBase operation', 'Create "{}" collection'.format(collection_name))

            coll.insert_many(mongo_dict)
            self.log.write_log('DataBase operation', 'Data Successfully Loaded into Mongo DB')
            return None
        except:
            self.log.write_log('DataBase operation', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def extract_from_db(self, collection_name, folder_path = r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB'):
        try:
            self.log.write_log('DataBase operation', 'Inside the "extract from db" method')
            coll = self.db_mongo[collection_name]
            self.log.write_log('DataBase operation', 'called collection {}'.format(collection_name))
            datas = coll.find()
            x = []
            for data in datas:
                x.append(data)
            x = pd.DataFrame(x)
            x = x.drop(columns=['_id'], errors='ignore')
            self.log.write_log('DataBase operation', 'Data Successfully extracted from MongoDB')

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                self.log.write_log('DataBase operation', 'delete existing DataExtractedFromDB')
            os.mkdir(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB')
            self.log.write_log('predict_file_validation', 'create DataExtractedFromDB')
            x.to_csv(r'{}\cement.csv'.format(folder_path), index=False)
            self.log.write_log('DataBase operation',
                               'cement.csv file successfully loaded in folder "DataExtractedFromDB"')
            return None
        except:
            self.log.write_log('DataBase operation', traceback.format_exc(), 'error')
            return traceback.format_exc()

#
# a = DB_define()
#
# print(a.extract_from_db('concrete'))
