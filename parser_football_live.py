import time
import psycopg2
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config

bot = telebot.TeleBot(config.TOKEN)


def game_time():
    game_time = driver.find_elements_by_class_name('cell_aa')
    return game_time


def game_score():
    score_game = driver.find_elements_by_class_name('cell_sa')
    return score_game


def id_game():
    id_games = driver.find_elements_by_class_name('stage-live')
    return id_games


def going_live_match():
    driver.find_element_by_link_text("Матчі LIVE").click()
    time.sleep(1)

    """открываем все закрытые чемпионаты"""

    fd = driver.find_elements_by_class_name('expand-league-link')
    for ii in fd:
        ii.click()
    time.sleep(1)


def insert_data_in_table_live(score_game, time, id_game):
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("delete from football_live;")
    for score_g, tim, id_g in zip(score_game, time, id_game):
         cursor.execute("insert into football_live (score, play_time, id_game) values (%s,%s,%s);",
                        (score_g.text, tim.text, id_g.get_attribute('id')))
    cursor.close()
    connection.close()


def select_t():
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(config.request_to_bd)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def select_u():
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("select * from player")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def send_message():
    try:
        player = select_u()
        game = select_t()
        for i in player:
            for j in game:
                if i[2] == u'1 тайм' and int(j[1]) == 24:
                    id_g = j[0]
                    link = f"https://www.myscore.ua/match/{id_g[4:]}/#match-summary"
                    bot.send_message(i[0], link)
                elif i[2] == u'2 тайм' and int(j[1]) == 60:
                    id_g = j[0]
                    link = f"https://www.myscore.ua/match/{id_g[4:]}/#match-summary"
                    bot.send_message(i[0], link)
    except Exception as e:
        print(e)


chrome_opt = Options()
chrome_opt.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\zheny\PycharmProjects\Bot1\chromedriver.exe',
                          chrome_options=chrome_opt)
driver.get('https://www.myscore.ua')


going_live_match()
insert_data_in_table_live(game_score(), game_time(), id_game())

driver.close()
driver.quit()

send_message()
