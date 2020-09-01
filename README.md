# RVMonitor-Public

The purpose of this application is to alert my wife and myself if the temperature in our RV is outisde of our defined temperature boundaries. 
We do this because we have a dog in our RV and we want to ensure that if there is a power loss, or other failure in our RV, our dog does not 
get too hot or too cold.

The RVmonitor is a python application that will run on a separate Raspberry Pi installed on the same network as 
the LCI One Control device. This was built to run on a Grand Design Momentum toy hauler. The One Control device controls the 
Air Conditioners in the Toy Hauler, so the One Control knows the temperature of each room in the RV.

I also use this same Raspberry Pi as a Plex media server for our RV. Plex was setup first, and I took on this project as a way to take advantage of the
compute power while we were away from our RV.

Definations:
Alert - This means that the temperature of the RV is outside of the user defined boundaries and will send an email to the address defined in the line 
        'notification_address' This address can be an email, or a text address. This is the address that receives alerts. To text the alert to your cell phone 
        (what I do), I entered my phonenumber@mms.att.net as the notification address. This sends the temperatures to my phone as a text message. 
        the rvmonitor.ini.Example file includes the formats for sending text messages to phones on a few of the other carriers.

Logs - This application generates a lot of logging. It generates a separate log file each day and is able to clean up old log files older than the 'log_retention' 
        setting in the rvmonitor.ini file. This setting is based on the number of days you want to keep the logs. There is not a mechanism to completely disable the logs, 
        so if you don't want them, set the log_retention to 1 or 2 and it will just keep a couple of days of logs.

This application will query the One Control device for the temperatures in each room, then send a text message if any of the temperatures 
are ourside of the temperature boundaries you define.  Since we are talking about a Toy Hauler, I have  the option to ignore the temperature in the garage
in case the garage temperature is not a concern. Setting the 'use_garage_temp = false' in the rvmonitor.ini file will still cause the temperature in the garage 
to be reported, but will not generate an alert based on the garage temperature.


The rvmonitor.ini.Example file provides a good overview of the settings available.
This application assumes everything is places in a directory off the root of 
/RVmonitor and there is a file in that directory named rvmonitor.ini
You can use the rvmonitor.ini.Example as a starting point for the file. It is pretty well documented.

In the directory /RVmonitor, please create a directory /RVmonitor/logs/ That is where all of the diagnostic logs will
be stored. I tried to generate a lot of logs and assumed storage is cheap. As you can see in the rvmonitor.ini file, 
you can provide an alternate location for the log files if you need additional storage. Having the application run 
every 15 minutes 24x7 will generate a log file of about 51K per day. Each day is stored in a separate log file and the 
application will clean up logs older than the 'log_retention' setting in the rvmonitor.ini file. I did not provide a way to 
eleminate the log files all together. If you don't want them, please set the log retention to something like 1 or 2. Honestly, 
I use the log for debugging and to make sure things are running properly. I don't see the little space they consume as an issue.


Setup:
On the root of your Raspberry Pi, create a directory named '/RVmonitor' and a directory named '/RVmonitor/logs' 
copy all of the .py files into the /RVmonitor directorie, the /logs directory will fill itself.
Take the file rvmonitor.ini.Example and rename it to rvmonitor.ini. If the file rvmonitor.ini is missing, the application will crash.



