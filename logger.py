# This will be for my logger functionality

import logging
from ReadConfigini import ReadConfigini 
import logging.config
import time
import os
from os import path
from datetime import datetime, timedelta

def setup_logger(config_settings):

     # create logger
    logger = logging.getLogger('rvmonitor') 

    logPath = config_settings['log_path']
    logFileName = config_settings['log_file']
    logLevel = int(config_settings['log_level'])
    logRetention = int(config_settings['log_retention'])

    completeLogFileName = logPath + time.strftime('%Y-%m-%d-') + logFileName
    print('compledteLogFileName = ' + completeLogFileName)

    hdlr = logging.FileHandler(completeLogFileName)


    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logLevel)

    # Now that we have the logger setup, let's remove, and log any files removed
    # We will look for files from the log retention period, back an additional 30 days to make sure we get them all.
    try: 
        for day in range(logRetention, logRetention + 30):
            oldLogDate = datetime.today() - timedelta(days=day)
            oldLogFileName = logPath + oldLogDate.strftime('%Y-%m-%d-') + logFileName
            if (os.path.exists(oldLogFileName)):
                # OK, we have an old log file that needs to go.
                os.remove(oldLogFileName)
                logger.info('deleted old log ' + oldLogFileName)
                              
    except:
        print("couldn't delete old logs\n")

    return logger


if (__name__ == "__main__"):
    
    config_settings = ReadConfigini('rvmonitor.ini')
    
    logger = setup_logger(config_settings)

    logger.critical('-- In test Code testing logging--')
    logger.critical('This is Critical')
    logger.error('This is error')
    logger.warning('This is warning')
    logger.info('this is info')
    logger.debug('this is debug')  
    logger.critical('-- Ending Test Code--\n')

    print('\n')

 