# Health check

The **health_check.py** script run in the background every 60 seconds monitoring some of system statistics: CPU usage, disk space, available memory and network. This script should send an email if there are problems, such as:
>- Report an error if CPU usage is over 80% 
>- Report an error if available disk space is lower than 20% 
>- Report an error if available memory is less than 500MB 
>- Report an error if the hostname "localhost" cannot be resolved to "127.0.0.1"
