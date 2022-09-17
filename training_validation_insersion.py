import traceback

from Logger import logger

from Archive import archive

from DataValidation import TrainDataValidation
from DataBaseAction import database


class train_validation:
    def __init__(self, train_folder_path):
        self.log = logger.logs()
        self.log.write_log('TrainValidationInsertion', 'Inside the class train_validation')
        self.path = train_folder_path
        self.log.write_log('TrainValidationInsertion', 'Path given is {}'.format(self.path))
        self.database_opn = database.DB_define()
        self.validation = TrainDataValidation.train_data_validation()
        self.archive = archive.move_file()

    def train_validation(self):
        try:
            self.log.write_log('TrainValidationInsertion', 'Inside the method "train_validation" ')
            self.log.write_log('TrainValidationInsertion', 'Start of validation on files')
            # validation Process
            # validating the file names
            self.validation.file_name_validate(self.path)
            # validating the columns names
            self.validation.file_column_validation()
            # validating the columns if entire column is missing
            self.validation.entire_column_missing()
            self.log.write_log('TrainValidationInsertion', 'Finish of training file validation')

            # Data Base insertion
            self.log.write_log('TrainValidationInsertion', 'DataBase insertion started')
            # Creating collection name "concrete" and inserting CSV data into the DB
            self.database_opn.insert_into_db('concrete')
            self.log.write_log('TrainValidationInsertion', 'DataBase insertion finished')
            # Deleting "GoodRawFolder" folder
            # self.action.deleteExistingGoodDataTrainingFolder()
            # self.log.write_log('TrainValidationInsertion', 'GoodRawFolder deleted')
            # Archiving the bad data folder.
            self.archive.to_archive(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
            self.log.write_log('TrainValidationInsertion', 'Bad Raw folder archived')
            # self.action.deleteExistingBadDataTrainingFolder()
            # self.log.write_log('TrainValidationInsertion', 'Bad Raw folder deleted')
            # data extraction from the DB
            self.database_opn.extract_from_db('concrete')
            self.log.write_log('TrainValidationInsertion', 'Data extracted from the data base and stored in data extracted from DB')
            self.log.write_log('TrainValidationInsertion', 'Validation operation completed')
            return None
        except:
            self.log.write_log('TrainValidationInsertion', traceback.format_exc(), 'error')
            return traceback.format_exc()

# a = train_validation(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\DataFromClient')
# a.train_validation()
