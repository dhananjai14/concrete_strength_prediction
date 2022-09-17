import traceback

from Logger import logger

from Archive import archive

from DataValidation import PredictionDataValidation
from DataBaseAction import database


class prediction_validation:
    def __init__(self, predict_folder_path):
        self.log = logger.logs()
        self.log.write_log('PredictValidationInsertion', 'Inside the class prediction_validation')
        self.path = predict_folder_path
        self.log.write_log('PredictValidationInsertion', 'Path given is {}'.format(self.path))
        self.database_opn = database.DB_define()
        self.validation = PredictionDataValidation.predict_data_validation()
        self.archive = archive.move_file()

    def predict_validation(self):
        try:
            self.log.write_log('PredictValidationInsertion', 'Inside the method "predict_validation" ')
            self.log.write_log('PredictValidationInsertion', 'Start of validation on files')
            # validation Process
            # validating the file names
            self.validation.file_name_validate(self.path)
            # validating the columns names
            self.validation.file_column_validation()
            # validating the columns if entire column is missing
            self.validation.entire_column_missing()
            self.log.write_log('PredictValidationInsertion', 'Finish of training file validation')

            # Data Base insertion
            self.log.write_log('PredictValidationInsertion', 'DataBase insertion started')
            # Creating collection name "predictConcrete" inserting CSV data into the DB
            self.database_opn.insert_into_db('predictConcrete')
            self.log.write_log('PredictValidationInsertion', 'DataBase insertion finished')
            # Archiving the bad data folder.
            self.archive.to_archive(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
            self.log.write_log('PredictValidationInsertion', 'Bad Raw folder archived')
            # data extraction from the DB
            self.database_opn.extract_from_db('predictConcrete')
            self.log.write_log('PredictValidationInsertion', 'Data extracted from the data base and stored in data extracted from DB')
            self.log.write_log('PredictValidationInsertion', 'Validation operation completed')
            return None
        except:
            self.log.write_log('PredictValidationInsertion', traceback.format_exc(), 'error')
            return traceback.format_exc()

# a = prediction_validation(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataExtractedFromDB')
# a.predict_validation()
