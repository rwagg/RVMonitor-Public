# RVMonitor-Public

The purpose of this application is to alert my wife and myself if the temperature in our RV is outisde of our defined temperature boundaries. 
We do this because we have a dog in our RV and we want to ensure that if there is a power loss, or other failure in our RV, our dog does not 
get too hot or too cold.

RVmonitor.py is a python application that will run on a separate Raspberry Pi installed on the same network as 
the LCI One Control device. This was built to run on a Grand Design Momentum toy hauler. The One Control device in the Momentum controls the 
Air Conditioners in the RV, so the One Control knows the temperature of each room in the RV. 

I also use this same Raspberry Pi as a Plex media server for our RV. Plex was setup first, and I took on this project as a way to take advantage of the
compute power while we are away from our RV.

This application will send a text alert if the temperatures are out of our defined boundaries, this application is also capabile of sending emails to a
separate email account each time the application runs. I do this so I can easily ensure that the application is running as it is supposed to and I can 
proactively check on the RV temperatures.

Definations:

Alert - This means that the temperature of the RV is outside of the user defined boundaries and will send an email to the address defined in the line 
        'notification_address' in the rvmonitor.ini file. This address can be an email, or a text address. This is the address that receives alerts. 
        To text the alert to your cell phone (what I do), I entered my phonenumber@mms.att.net as the notification address. This sends the temperatures 
        to my AT&T phone as a text message. The rvmonitor.ini.Example file includes the formats for sending text messages to phones on a few of the other carriers.
        

Logs - This application generates a lot of logging. It generates a separate log file each day and is able to clean up log files older than the 'log_retention' 
        setting in the rvmonitor.ini file. This setting is based on the number of days you want to retain the logs. There is not a mechanism to completely disable the logs, 
        so if you don't want them, set the log_retention to 1 or 2 and it will just keep a couple of days of logs. I keep about 5 days worth of logs so I 
        can troubleshoot any abnormalities. 
        

This application will query the One Control device for the temperatures in each room, then send a text message to the 'notification_address' if any of the temperatures 
are outside of the temperature boundaries you define.  Since we are talking about a Toy Hauler, I enabled the option to ignore the temperature in the garage
in case the garage temperature is not a concern. Setting the 'use_garage_temp = false' in the rvmonitor.ini file will still cause the temperature in the garage 
to be reported, but will not generate an alert based on the garage temperature.


The 'rvmonitor.ini.Example' file provides a good overview of the settings available.
This application assumes everything is placed in a directory off the root named /RVmonitor and there is a file in that directory named 'rvmonitor.ini'
You can use the rvmonitor.ini.Example as a starting point for the file. This file is pretty well documented.

In the directory /RVmonitor, please create a directory /RVmonitor/logs/ That is where all of the diagnostic logs will
be stored. I tried to generate a lot of logs and assumed storage is cheap. As you can see in the rvmonitor.ini file, 
you can provide an alternate location for the log files if you need additional storage. Having the application run 
every 15 minutes 24x7 will generate a log file of about 51K per day. Each day is stored in a separate log file and the 
application will clean up logs older than the 'log_retention' setting in the rvmonitor.ini file. I use the log for debugging 
and to make sure things are running properly. I don't see the little space they consume as an issue.



To Setup the application on your Raspberry Pi:

On the root of your Raspberry Pi, create a directory named '/RVmonitor' and a directory named '/RVmonitor/logs' 

Set the permissions so that Anyone can View Content, Change Content and Access content. You can do this through the File Manager.

copy all of the .py files into the /RVmonitor directory, the /logs directory will fill itself.

copy the file 'rvtemp.sh' to the /RVmonitor directory as well

use chmod to configure the rvtemp.sh file as an executable, for example

sudo chmod +x /RVmonitor/rvtemp.sh 

Take the file rvmonitor.ini.Example and rename it to rvmonitor.ini. If the file rvmonitor.ini is missing, the application will crash.

Configure cron to run the application every 15 minutes. Use the command line

sudo crontab -e (and choose your favorite editor if this is the first time to use cron)

At the bottom of the file add the following line:

*/15 * * * * /RVmonitor/rvtemp.sh

This command tells cron to run the file rvtemp.sh every 15 minutes.

If everything is setup properly, you should start seeing the log file grow every 15 minutes.



