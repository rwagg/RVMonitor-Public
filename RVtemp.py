# This works for getting the temps of all of the hvac-things
import sys
import o365Text
from ReadConfigini import ReadConfigini 
from logger import setup_logger

# I got the openHAB API from here: https://pypi.org/project/python-openhab/
# I had to copy the openhab lib from /home/pi/.local/lib/python3.7/site-packages to /usr/lib/python3.7. 
# I could not run in in a shell script since it no longer had the users local env.
from openhab import OpenHAB
import re
import requests
import json
import time

# Got the basic code from here: https://pypi.org/project/python-openhab/

def get_RVTemp():

    sendEmail = False

    config_settings = ReadConfigini('/RVmonitor/rvmonitor.ini')

    logger = setup_logger(config_settings)

    logger.critical('**')
    logger.critical('Starting the RV Temp Monitor')
    logger.critical('**')
    logger.debug(config_settings)

    email_Address = config_settings['notification_address']

    base_url = config_settings['base_url']
    openhab = OpenHAB(base_url + '/rest')

    try:
        response = requests.get(base_url + '/rest/things')

    except:
        o365Text.send_email(email_Address, 'Connection Error', 'Could Not Connect to One Control - Things', '',
            config_settings['email_sender'], config_settings['server_userName'], config_settings['server_Password'], logger)
        logger.error('Could not connect to One Control things')

    if (response.status_code != 200):
        o365Text.send_email(email_Address, 'Connection Error', 'Could Not Connect to One Control - Request Failed', '',
            config_settings['email_sender'], config_settings['server_userName'], config_settings['server_Password'], logger)
        logger.error('Request Failed - Could not connect to One Control')

    try:
        json_data = response.json()

        hvac_devices = {}
        generator_details = {}
        fuel_tank = {}
        temp = 0
        for k in json_data:
            # We are looking for the Air-conditioners
            if (k["thingTypeUID"] == "idsmyrv:hvac-thing"):
                for c in k["channels"]:
                    linkedItem = c["linkedItems"]
                    linkedItem = (str(linkedItem).strip('[]')).strip("''")
                    if c['id'] == 'inside-temperature':
                        temp = openhab.get_item(linkedItem)
                        hvac_devices.update({k["label"] : {"UID":k["UID"], "Thing" : linkedItem, "Temp" : temp.state}})
            
            # We are looking for the generator
            if (k["thingTypeUID"] == 'idsmyrv:generator-thing'):
                for c in k["channels"]:
                    if c['id'] == 'battery-voltage':
                        linkedItem = c['uid'].replace(':','_')
                        linkedItem = linkedItem.replace('-','_')
                        temp = openhab.get_item(linkedItem)
                        generator_details.update({'Battery Voltage' : str(temp.state)})

                    if c['id'] == 'state':
                        linkedItem = c['uid'].replace(':','_')
                        linkedItem = linkedItem.replace('-','_')
                        state = openhab.get_item(linkedItem)
                        generator_details.update({'Running State' : state.state})

            # We are looking for the Fuel Tank sensor
            if (k["thingTypeUID"] == 'idsmyrv:tank-sensor-thing'):
                if ((k['label']).lower() == "fuel tank"):
                    for c in k["channels"]:
                        if ((c['id']).lower() == "tank-level"):
                            linkedItem = c['uid'].replace(':','_')
                            linkedItem = linkedItem.replace('-','_')
                            temp = openhab.get_item(linkedItem)
                            print('Fuel Tank level ', end = '')
                            print (temp.state)
                            fuel_tank.update({k["label"] : {"UID":k["UID"], "Thing" : linkedItem, "Fuel" :temp.state}})

        message = ''
        tempHi = config_settings['temp_hi']
        tempLow = config_settings['temp_low']
        useGarageTemp = (config_settings['use_garage_temp']).lower() == 'true'

        for room in hvac_devices:
            spc = room.find(' ')
            if (spc > 0):
                name = room[0:spc]
            else:
                name = room
            #numTemp is the temp in floating point form
            numTemp = hvac_devices[room]["Temp"]
            if ((numTemp > float(tempHi)) or (numTemp < float(tempLow))) :
                if name.lower() == 'garage' :
                    if useGarageTemp :
                        sendEmail = True
                else :
                    sendEmail = True

            temperature = "{:.0f}".format(numTemp,1)
            message += name + ' ' + temperature + '\n'
            
# This does assume you only have a single generator
        message += "Batt V " + str(generator_details['Battery Voltage']) + '\n'
        message += 'Gen State ' + generator_details['Running State'] + '\n'
        level = "{:.0f}".format(fuel_tank["Fuel Tank"]["Fuel"],0)
        message += 'Fuel ' + level + "% \n"
        message += "Hi limit " + tempHi + '\n'
        message += "Low limit " + tempLow 
        
    except:
        message = 'Error, could not read temperatures'
        logger.error('Could not read temperatures')
        # If we can't get temps, let's notify the user
        sendEmail = True

    finally:
        if sendEmail:
            o365Text.send_email(email_Address, 'Temp in Mo',
                message,  '',
                config_settings['email_senderName'],
                config_settings['email_userName'],
                config_settings['email_password'], 
                logger)
            logger.info('Gathered temps and emailed\n' + message)
        else:
            logger.info("No need to send email, temps are acceptable")
            logger.info("\n" + message)

    logAddress = config_settings['log_address']
    if ( logAddress.lower() != 'none') and (logAddress):
        o365Text.send_email(config_settings['log_address'], 'Temp in Mo',
            message,  '',
            config_settings['email_senderName'],
            config_settings['email_userName'],
            config_settings['email_password'], 
            logger)
        logger.info('Gathered temps and emailed to log address :' + logAddress)

    logger.critical('**')
    logger.critical('Ending run of the RV Temp Monitor')
    logger.critical('**\n')


get_RVTemp()
