import time

import psycopg2
import telebot
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import config

bot = telebot.TeleBot(config.TOKEN)


def game():
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("delete from bask_next;")
    time.sleep(1)
    driver.find_element_by_class_name('head__title').click()
    time.sleep(1)
    driver.find_element_by_class_name('li5').click()
    id_games = driver.find_elements_by_class_name('cell_aa')
    for i in id_games:
        connection = psycopg2.connect(config.link_db)
        connection.autocommit = True
        cursor = connection.cursor()
        i.click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        exclusion = ''
        try:
            team_ = driver.find_elements_by_class_name('participant-imglink')
            team_home = team_[1].text
            team_awey = team_[3].text
        except NoSuchElementException:
            team_awey = None
            team_home = None
            exclusion = exclusion + ' 1 '
        try:
            time_game = driver.find_element_by_class_name('mstat-date').text
        except NoSuchElementException:
            time_game = None
            exclusion = exclusion + ' 4 '
        try:
            time.sleep(1)
            r = driver.find_elements_by_class_name('button')
            re = driver.find_element_by_link_text('Передматчеві коефіцієнти').text
            try:
                t_1 = r[2].text.split('\n')
                t_2 = r[3].text.split('\n')
            except IndexError:
                t_1 = r[0].text.split('\n')
                t_2 = r[1].text.split('\n')
            if re != '':
                cof_win_team_1 = t_1[1]
                cof_win_team_2 = t_2[1]
                if cof_win_team_1 != '-' and cof_win_team_2 != '-':
                    cof_win_team_1 = float(cof_win_team_1)
                    cof_win_team_2 = float(cof_win_team_2)
                    cof_difference = cof_win_team_1 - cof_win_team_2
                else:
                    cof_win_team_1 = None
                    cof_win_team_2 = None
                    cof_difference = None
                    exclusion = exclusion + ' 9 '
            else:

                cof_win_team_1 = None
                cof_win_team_2 = None
                cof_difference = None
                exclusion = exclusion + ' 9 '

        except NoSuchElementException:
            cof_win_team_1 = None
            cof_win_team_2 = None
            cof_difference = None
            exclusion = exclusion + ' 9 '

        link_game = driver.current_url
        cursor.execute("insert into bask_next (exclusion, data, team_home, team_awey, cof_team_1, cof_team_2,"
                       " cof_difference, link_game) "
                       "values (%s,%s,%s,%s,%s,%s,%s,%s);",
                       (exclusion, time_game, team_home, team_awey, cof_win_team_1, cof_win_team_2,
                        cof_difference, link_game))
        cursor.close()
        connection.close()
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.quit()


def gf():
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    exclusion = ''
    try:
        team_ = driver.find_elements_by_class_name('participant-imglink')
        team_home = team_[1].text
        team_awey = team_[3].text
    except NoSuchElementException:
        team_awey = None
        team_home = None
        exclusion = exclusion + ' 1 '
    try:
        time_game = driver.find_element_by_class_name('mstat-date').text
    except NoSuchElementException:
        time_game = None
        exclusion = exclusion + ' 4 '
    try:
        time.sleep(1)
        r = driver.find_elements_by_class_name('button')
        re = driver.find_element_by_link_text('Передматчеві коефіцієнти').text
        try:
            t_1 = r[2].text.split('\n')
            t_2 = r[3].text.split('\n')
        except IndexError:
            t_1 = r[0].text.split('\n')
            t_2 = r[1].text.split('\n')

        if re != '':
            cof_win_team_1 = t_1[1]
            cof_win_team_2 = t_2[1]
            if cof_win_team_1 != '-' and cof_win_team_2 != '-':
                cof_win_team_1 = float(cof_win_team_1)
                cof_win_team_2 = float(cof_win_team_2)
                cof_difference = cof_win_team_1 - cof_win_team_2
            else:
                cof_win_team_1 = None
                cof_win_team_2 = None
                cof_difference = None
                exclusion = exclusion + ' 9 '
        else:

            cof_win_team_1 = None
            cof_win_team_2 = None
            cof_difference = None
            exclusion = exclusion + ' 9 '

    except NoSuchElementException:
        cof_win_team_1 = None
        cof_win_team_2 = None
        cof_difference = None
        exclusion = exclusion + ' 9 '

    link_game = driver.current_url
    cursor.execute("insert into bask_next (exclusion, data, team_home, team_awey, cof_team_1, cof_team_2,"
                   " cof_difference, link_game) "
                   "values (%s,%s,%s,%s,%s,%s,%s,%s);",
                   (exclusion, time_game, team_home, team_awey, cof_win_team_1, cof_win_team_2,
                    cof_difference, link_game))
    cursor.close()
    connection.close()
    driver.close()
    driver.quit()


def going_match():
    time.sleep(1)
   # driver.find_element_by_class_name('tomorrow').click()
    driver.find_element_by_class_name('yesterday').click()
    time.sleep(3)
    li = {'latomyg_3_WKlijxHr',# англия ббл
          'latomyg_3_nwKL1I6D',# испания акб
          'latomyg_3_rydC2Qu2',# италия а1
          'latomyg_3_O4KtaF1G',# италия а2 захид
          'latomyg_3_AL4xtWJu',#немцы ббл
          'latomyg_3_QgfOpNX2',#немцы про в
          'latomyg_3_4r8WC00A',#поляки
          'latomyg_3_Qu1RjeyI',#турки
          'latomyg_3_4E0lJKd3',#финляндия
          'latomyg_3_jBQC3vx1',#франция
          'latomyg_3_2w8dvi7S',#япония
          'latomyg_3_hIPDfVNd',#немцы про а
          'latomyg_3_UsLx0enA',#италия а2 схид
          'latomyg_3_nqXQZgpI',#
          'latomyg_3_t6WUYDaO'#
#          '',#а2 плэй аут
#          ''#а2 плэй оф
          }
    ell = driver.find_elements_by_class_name('tomyg')
    for ii in ell:
        for iii in li:
            if ii.get_attribute('id') == iii:
                ii.click()


def id_game():
    time.sleep(1)
    driver.find_element_by_class_name('head__title').click()
    time.sleep(1)
    driver.find_element_by_class_name('li5').click()
    id_games = driver.find_elements_by_class_name('cell_aa')
    for i in id_games:
        i.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        r = driver.find_elements_by_class_name('odds-wrap')
        o = r[2].text
        p = r[3].text
        z = float(o) - float(p)
        print("Коэф " + str(z))
        if 2 < z < 13 or -13 < z < -2:
            driver.find_element_by_class_name("li2").click()
            time.sleep(2)
            driver.find_element_by_id("h2h-home").click()
            rr = driver.find_elements_by_class_name("score")
            kol = 0
            for iii in rr:
                v = iii.text
                t = v.split('\n')
                q = t[0].split(' : ')
                if v != "":
                    r = q[0]
                    u = q[1]
                    t = int(r) - int(u)
                    kol = kol + 1
                    if kol > 5:
                        iii.click()
                        driver.switch_to.window(driver.window_handles[2])
                        time.sleep(3)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[1])

                    print(t)
            driver.close()
        else:
            driver.close()
        driver.switch_to.window(driver.window_handles[0])


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
driver = webdriver.Chrome(executable_path=r'C:\Users\zheny\PycharmProjects\Bot1\chromedriver.exe')
# ,chrome_options=chrome_opt)

driver.get('https://www.myscore.ua/basketball')

# driver.get('https://www.myscore.ua/match/GSzjjFsh/#match-summary')
# gf()

going_match()
game()
