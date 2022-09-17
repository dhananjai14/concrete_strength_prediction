import pickle
import traceback
from Logger import logger


class model_load:
    def __init__(self):
        try:
            self.log = logger.logs()
            self.log.write_log('file_action' , 'inside the class model_load')
            pass
        except:
            self.log.write_log('file_action', traceback.format_exc(), 'error')

    def to_save(self, model,filename_without_extension):

        try:
            self.log.write_log('file_action', 'inside the method "to_save"')

            with open(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\model\training\{}.sav'.format(filename_without_extension), 'wb') as f:
                pickle.dump(model,f)
            self.log.write_log('file_action', 'file successfully saved {}.sav'.format(filename_without_extension))
        except:
            self.log.write_log('file_action', traceback.format_exc(), 'error' )
            return traceback.format_exc()

    def to_load(self, filename_without_extension):
        try:
            self.log.write_log('file_action', 'inside the method "to_load"')
            file = open(r'C:\Users\preet\Desktop\DS\Project\Concrete Project\model\training\{}.sav'.format(filename_without_extension), 'rb')
            object_file = pickle.load(file)
            file.close()
            self.log.write_log('file_action', 'file {}.sav successfully loaded'.format(filename_without_extension))
            return object_file
        except:
            self.log.write_log('file_action', traceback.format_exc(), 'error' )
            return traceback.format_exc()


