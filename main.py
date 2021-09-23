from math import prod
import telebot
from bs4 import BeautifulSoup
import requests
import config, database
from fake_useragent import UserAgent
from random import randint
from datetime import datetime
import time

bot = telebot.TeleBot(config.token)
popular_link = 'https://www.yakaboo.ua/ua/top100/category/popular/id/4723/?custom=statistics_is_for_promotion'

url_list = []


def get_url_list():
    response = requests.get(popular_link, headers=requests.utils.default_headers())
    soup = BeautifulSoup(response.text, 'lxml')

    for p_name in soup.findAll('a', attrs={'class':'product-name'}):
        if p_name not in url_list:
            url_list.append(p_name['href'])

def get_product_info():
    item_random = randint(0, len(url_list))
    product_link = url_list[item_random]
    product_response = requests.get(product_link, headers=requests.utils.default_headers())
    product_content = BeautifulSoup(product_response.text, 'lxml')

    book_name = ''
    for b_name in product_content.findAll('h1', attrs={'itemprop':'description'}):
        book_name = b_name.text

    book_description = ''
    for b_desc in product_content.findAll('div', attrs={'class':'description-shadow'}):
        book_description = b_desc.text

    book_image = ''
    for b_img in product_content.findAll('img', attrs={'id':'image'}):
        book_image = b_img['src']

    print(book_name)
    print(book_description)
    print(product_link)
    print(book_image)

    return book_name, str(book_description).replace('Усе про книжку ' + str(book_name) + '\n\n', ''), book_image, product_link

def main():
    get_url_list()

    product_info = get_product_info()
    product_link = product_info[3]
    new_records = database.check_new_book(product_link)
    if new_records == None:
        book_name = product_info[0]
        book_desc = product_info[1]
        book_img = product_info[2]

        menu = telebot.types.InlineKeyboardMarkup()
        menu.row(telebot.types.InlineKeyboardButton('👉 Замовити 👈', url='https://instagram.com/booken.ua'))

        message_text = """📖 {0}

🗯 Анотація
{1}""".format(str(book_name).strip(), str(book_desc).strip())
        response = requests.get(book_img)
        file = open("top_img.png", "wb")
        file.write(response.content)
        file.close()
        
        top_img = open("top_img.png", 'rb') 
        bot.send_photo('@booken_ua', photo=top_img, caption='👇 Детальніше 👇')
        top_img.close()

        bot.send_message('@booken_ua', message_text, parse_mode='Markdown', reply_markup=menu)
        database.inser_book_in_db(product_link)
        time.sleep(3600*4)
    else:
        time.sleep(1)

while True:
    try:
        hour_now = int(datetime.now().hour)
        if hour_now > 10 and hour_now < 20:
            main()
        else:
            time.sleep(3600*3)
    except Exception as e:
        database.insert_bugs(str(e))
        time.sleep(3)