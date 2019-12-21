import smtplib
import time
import requests
import sys
import random
from bs4 import BeautifulSoup

URL = 'https://www.alza.cz/magic-mouse-2-d3753149.htm?o=1'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

title = ''
threshold = 0
server = smtplib.SMTP('smtp.gmail.com', 587)


def check_price():
    global title
    global threshold

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title_arr = soup.findAll("h1")
    price_arr = soup.findAll("span", {"class": "price_withVat"})

    if len(title_arr) == 0 or len(price_arr) == 0:
        send_warning_mail()
        end_script()

    title = title_arr[0].get_text().strip()
    price = price_arr[0].get_text()

    converted_price = int(''.join(price[0:5].split()))

    print(title)
    print(converted_price)

    threshold = 2000

    if converted_price < threshold:
        send_success_mail()


def setup_email_service():
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('simon.smejkal13@gmail.com', 'pgidzabtdhckiybq')


def send_email(msg):
    server.sendmail('simon.smejkal13@gmail.com',
                    'simon.smejkal@seznam.cz', msg)

    print('Email has been sent!')

    server.quit()


def send_success_mail():
    setup_email_service()

    subject = f'Price of {title} fell down under {threshold}'
    body = f'Check the amazon link: {URL}'
    msg = f'Subject: {subject}\n\n{body}'

    send_email(msg)


def send_warning_mail():
    setup_email_service()

    subject = 'The item you were tracking was not found'
    body = f'Something has changed and the link {URL} is probably no longer valid'
    msg = f'Subject: {subject}\n\n{body}'

    send_email(msg)


def end_script():
    print('Exiting the script...')
    sys.exit()


while(True):
    random_hours = random.randint(4, 8)
    random_offset = random.randint(60, 1200)
    check_price()
    time.sleep(60 * 60 * random_hours + random_offset)
