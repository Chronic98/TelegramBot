import time

import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config


def insert_football(id_game):
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    cof_wins_team1 = driver.find_element_by_xpath(f"//tr[@id='{id_game.get_attribute('id')}']/td[6]")
    cof_wins_team2 = driver.find_element_by_xpath(f"//tr[@id='{id_game.get_attribute('id')}']/td[8]")
    home_team = driver.find_element_by_xpath(f"//tr[@id='{id_game.get_attribute('id')}']/td[3]")
    guest_team = driver.find_element_by_xpath(f"//tr[@id='{id_game.get_attribute('id')}']/td[4]")
    if (cof_wins_team1.text != '-'):
        cursor.execute("insert into football (id_game, team_home, team_guest, coeff_home, coeff_guest) "
                       "values (%s,%s,%s,%s,%s);",
                       (id_game.get_attribute('id'), home_team.text, guest_team.text,
                        float(cof_wins_team1.text), float(cof_wins_team2.text)))
    cursor.close()
    connection.close()


def id_game_all():
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("delete from football;")
    id_g_l = driver.find_elements_by_class_name('stage-scheduled')
    id_games = driver.find_elements_by_class_name('stage-live')
    id_game = id_games + id_g_l
    for id_ in id_game:
        insert_football(id_)
    cursor.close()
    connection.close()


chrome_opt = Options()
chrome_opt.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\zheny\PycharmProjects\Bot1\chromedriver.exe',
                          chrome_options=chrome_opt)
driver.get('https://www.myscore.ua')
driver.find_element_by_link_text("Коефіцієнти").click()
time.sleep(3)

id_game_all()

driver.close()
driver.quit()
