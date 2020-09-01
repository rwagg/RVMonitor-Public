# This will read all of the settings in the config.ini file

# Take from https://docs.python.org/3/library/configparser.html

import configparser
import logging

def ReadConfigini(settings_file = 'config.ini'):

    config_settings = {}
    config = configparser.ConfigParser()
    config.read(settings_file)

    config_settings.update( {'email_userName' : config.get('EMAIL ACCOUNT', 'email_userName', fallback = 'error')})
    config_settings.update( {'email_password' : config.get('EMAIL ACCOUNT', 'email_password', fallback = 'error')})
    config_settings.update( {'email_senderName' : config.get('EMAIL ACCOUNT', 'email_senderName', fallback = 'error')})
    config_settings.update( {'notification_address' : config.get('NOTIFICATION ADDRESS', 'notification_address', fallback = 'error')})
    
    config_settings.update( {'base_url' : config.get('PI INFORMATION', 'base_url', fallback = 'error')})
    
    config_settings.update( {'logging_detail' : config.get('LOGGING', 'logging_detail', fallback = 'CRITICAL')})
    config_settings.update( {'log_file' : config.get('LOGGING', 'log_file', fallback = 'logfile.log')})
    config_settings.update( {'log_path' : config.get('LOGGING', 'log_path', fallback = '/home/pi/')})
    config_settings.update( {'log_level' : config.get('LOGGING', 'log_level', fallback = logging.DEBUG)})
    config_settings.update( {'log_retention' : config.get('LOGGING', 'log_retention', fallback = 30)})

    config_settings.update( {'temp_hi' : config.get('THRESHOLDS', 'temp_hi', fallback = 80)})
    config_settings.update( {'temp_low' : config.get('THRESHOLDS', 'temp_low', fallback = 40)})
    config_settings.update( {'use_garage_temp' : config.get('THRESHOLDS', 'use_garage_temp', fallback = 'true')})

    config_settings.update( {'log_address' : config.get('LOG ADDRESS', 'log_address', fallback = 'none')})
    
    return config_settings      

if (__name__ == "__main__"):
    c_settings = ReadConfigini('/RVmonitor/rvmonitor.ini')
    print('\nin testcode dumping config.ini dict ' + __file__ + '\n')
    print('-- Key --'.center(21, ' ') + ':' + '-- value --'.center(15, ' '))
    for key, value in c_settings.items() :
        print (key.ljust(20, ' ') + " : ", end='')
        print(value)
    print('\n')

# End of file
 
 