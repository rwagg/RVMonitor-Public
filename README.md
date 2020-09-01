# RVMonitor-Public

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
