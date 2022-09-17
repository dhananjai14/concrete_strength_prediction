from Logger import logger
import os
import shutil
import pandas as pd
import traceback


class predict_data_validation:

    def __init__(self):

        try:
            self.log = logger.logs()
            self.log.write_log('predict_file_validation', 'entering prediction data validation class', 'info')
            pass
        except:
            self.log.write_log('predict_file_validation', traceback.format_exc(), 'error')

    def file_name_validate(self, predict_folder_path):
        """
        Checking the file name provided by the client.
        :param predict_folder_path:
        :return: None
        """

        try:
            self.log.write_log('predict_file_validation', 'inside the method file_name_validation')
            self.log.write_log('predict_file_validation', 'predict folder path is {}'.format(predict_folder_path))
            path = predict_folder_path
            file_names = os.listdir(path) # Get the file names in the directory
            self.log.write_log('predict_file_validation', 'File name fetched')
            if os.path.exists(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder'):
                shutil.rmtree(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
                self.log.write_log('predict_file_validation', 'delete existing BadRawFolder')
            os.mkdir(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
            self.log.write_log('predict_file_validation', 'create BadRawFolder')

            if os.path.exists(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\GoodRawFolder'):
                shutil.rmtree(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\GoodRawFolder')
                self.log.write_log('predict_file_validation', 'delete existing GoodRawFolder')
            os.makedirs(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\GoodRawFolder')
            self.log.write_log('predict_file_validation', 'create GoodRawFolder')

            for file_name in file_names:
                i = file_name
                i = i.split('.')
                if i[1] == 'csv':
                    i = i[0].split('_')
                    if len(i) == 2:
                        if len(i[1]) == 6:
                            if i[0] == 'Concrete':
                                shutil.move('{}\{}'.format(predict_folder_path, file_name),
                                            r'C:\Users\preet\Desktop\DS\Project\Concrete Project\GoodRawFolder')
                                self.log.write_log('predict_file_validation',
                                              'File {} has name in proper format. File moved to GoodRawFolder'.format(
                                                  file_name))
                            else:
                                shutil.move('{}\{}'.format(predict_folder_path, file_name),
                                            r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
                                self.log.write_log('predict_file_validation',
                                              'File name {} is not in proper format. File moved to BadRawFolder'.format(
                                                  file_name),
                                              'warning')
                        else:
                            shutil.move('{}\{}'.format(predict_folder_path, file_name),
                                        r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
                            self.log.write_log('predict_file_validation',
                                          'File name {} is not in proper format. File moved to BadRawFolder'.format(
                                              file_name),
                                          'warning')
                    else:
                        shutil.move('{}\{}'.format(predict_folder_path, file_name),
                                    r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
                        self.log.write_log('predict_file_validation',
                                      'File name {} is not in proper format. File moved to BadRawFolder'.format(
                                          file_name),
                                      'warning')
                else:
                    shutil.move('{}\{}'.format(predict_folder_path, file_name),
                                r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
                    self.log.write_log('predict_file_validation',
                                  'File name {} is not in proper format. File moved to BadRawFolder'.format(file_name),
                                  'warning')
        except:
            self.log.write_log('predict_file_validation', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def file_column_validation(self):
        """
        check if the columns names are as per the agreement.
        :return: None
        """

        try:

            path = r'C:\Users\preet\Desktop\DS\Project\Concrete Project\GoodRawFolder'
            self.log.write_log('predict_file_validation', 'Inside the file_column_validation method')
            file_lists = os.listdir(path)
            self.log.write_log('predict_file_validation', 'good raw folder path {}'.format(path))

            for files in file_lists:
                path = path + "\\" + files
                a = pd.read_csv(path)
                self.log.write_log('predict_file_validation', 'file {} was fetched'.format(files))
                actual_column = ['Cement', 'BlastFurnaceSlag', 'FlyAsh', 'Water', 'Superplasticizer', 'CoarseAggregate',
                                 'FineAggregate', 'Age']
                file_column = a.columns
                self.log.write_log('predict_file_validation', 'Columns fetched')
                for column in file_column:
                    if column in actual_column:
                        pass
                    else:
                        shutil.move(path, r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
                        self.log.write_log('predict_file_validation', '{} column name not in order'.format(column),
                                      log_level='warning')
                        self.log.write_log('predict_file_validation', '{} moved to BadRawFolder'.format(files),
                                      log_level='warning')
                        break
                self.log.write_log('predict_file_validation', 'column name validation completed for file {}'.format(files),
                              log_level='info')

        except:
            self.log.write_log('predict_file_validation', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def entire_column_missing(self):

        try:

            path = r'C:\Users\preet\Desktop\DS\Project\Concrete Project\GoodRawFolder'
            self.log.write_log('predict_file_validation', 'inside entire column missing method', log_level='info')
            files = os.listdir(path)
            self.log.write_log('predict_file_validation', 'path given is: {}'.format(path), log_level='info')

            for file in files:
                path = path + "\\" + file
                a = pd.read_csv(path)
                self.log.write_log('predict_file_validation', '{} file successfully loaded'.format(file), log_level='info')
                for column in a:
                    if a[column].isna().sum() == len(a):
                        self.log.write_log('predict_file_validation', '{} column has all missing values'.format(column),
                                      log_level='warning')
                        shutil.move(path, r'C:\Users\preet\Desktop\DS\Project\Concrete Project\BadRawFolder')
                        self.log.write_log('predict_file_validation', 'file {} moved to bad raw folder'.format(file),
                                      log_level='warning')
                        break
                self.log.write_log('predict_file_validation', 'column validation completer for file {}'.format(file))
        except:
            self.log.write_log('predict_file_validation', traceback.format_exc(), 'error')
            return traceback.format_exc()
