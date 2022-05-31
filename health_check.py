#!/usr/bin/env python3

import os
import shutil
import psutil
import socket
import email.message
import smtplib
import sched, time


sch_timer = sched.scheduler(time.time, time.sleep)


def check_disk(disk, min_gb, min_percent):
    """Returns True if there isn't enough disk space, False otherwise."""
    du = shutil.disk_usage(disk)
    percent_free = 100 * du.free / du.total
    gigabytes_free = du.free / 2**30
    if gigabytes_free < min_gb or percent_free < min_percent:
        return True
    return False

def check_memory_reminder(min_mb, max_percent):
    """Returns True if there isn't enough memory space, False otherwise."""
    memory = psutil.virtual_memory()
    percent_load = memory.percent
    megabytes_free = memory.free / 2**20
    if megabytes_free < min_mb or percent_load > max_percent:
        return True
    return False

def check_root():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk(disk="/", min_gb=2, min_percent=20)

def check_cpu():
    """Returns True if the the cpu is having too much usage, False otherwise."""
    return psutil.cpu_percent(1) > 80

def check_memory_overloaded():
    """Returns True if the the memory is having too much usage, False otherwise."""
    return check_memory_reminder(min_mb=500, max_percent=95)

def check_no_network():
    """Returns True if it fails to resolve Google's URL, False otherwise."""
    try:
        socket.gethostbyname("localhost")
        return False
    except:
        return True

def generate_error_report(sender, recipient, subject, body):
    """Creates an simple email"""
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    return message

def send_email(message):
    """Sends the message to the configured SMTP server."""
    mail_server = smtplib.SMTP('localhost')
    mail_server.send_message(message)
    mail_server.quit()


def main(timer):
    checks = [
        (check_root, "Error - Available disk space is less than 20%"),
        (check_cpu, "Error - CPU usage is over 80%"),
        (check_memory_overloaded, "Error - Available memory is less than 500MB"),
        (check_no_network, "Error - localhost cannot be resolved to 127.0.0.1"),
    ]
    health = True
    for check, msg in checks:
        if check():
            sender = "automation@example.com"
            receiver = "{}@example.com".format(os.environ.get('USER'))
            health = False
            email_body = "Please check your system and resolve the issue as soon as possible."
            message = generate_error_report(sender, receiver, msg, email_body)
            send_email(message)

    if not health:
        print("Please check the system, something is wrong!")

    print("Everything ok.")
    timer.enter(60, 1, main, (timer,))


sch_timer.enter(10, 1, main, (sch_timer,))
sch_timer.run()
