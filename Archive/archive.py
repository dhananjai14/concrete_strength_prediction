import os
import shutil
from datetime import datetime
from Logger import logger
import traceback


class move_file:
    def __init__(self):
        try:
            self.log = logger.logs()
            self.log.write_log('archive', 'Inside the move file class')
        except:
            self.log.write_log('archive', traceback.format_exc(), 'error')

    def to_archive(self, source_path):
        try:
            self.log.write_log('archive', 'inside the "to_archive" method')
            self.log.write_log('archive', 'path of folder to be archived {}'.format(source_path))
            time = datetime.now().strftime('%d_%m_%Y %H.%M')
            self.destination = r'C:\Users\preet\Desktop\DS\Project\Concrete Project\Data Archive' + '\\' + time
            os.mkdir(self.destination)
            self.log.write_log('archive', 'destination archive folder "{}" created'.format(time))
            files = os.listdir(source_path)
            for file in files:
                path = source_path + '\\' + file
                shutil.move(path, self.destination)
                self.log.write_log('archive', 'file {} moved to archive folder'.format(file))
        except:
            self.log.write_log('archive', traceback.format_exc(), 'error')
            return traceback.format_exc()

