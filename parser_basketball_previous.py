import time

import psycopg2
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import config


def game():
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
            team_home = driver.find_element_by_xpath("//tr[@class='odd']/td[1]//a[1]").text
        except NoSuchElementException:
            team_home = None
            exclusion = exclusion + ' 1 '
        try:
            team_awey = driver.find_element_by_xpath("//tr[@class='even']/td[1]//a[1]").text
        except NoSuchElementException:
            team_awey = None
            exclusion = exclusion + ' 2 '
        try:
            team_home_score = int(driver.find_element_by_xpath("//tr[@class='odd']/td[2]/strong[1]").text)
            team_awey_score = int(driver.find_element_by_xpath("//tr[@class='even']/td[2]/strong[1]").text)
            difference_score_game = int(team_home_score) - int(team_awey_score)
        except NoSuchElementException:
            team_home_score = None
            team_awey_score = None
            difference_score_game = None
            exclusion = exclusion + ' 3 '
        try:
            time_game = driver.find_element_by_class_name('mstat-date').text
        except NoSuchElementException:
            time_game = None
            exclusion = exclusion + ' 4 '
        try:
            p1_home = driver.find_element_by_class_name('p1_home').text
            p1_away = driver.find_element_by_class_name('p1_away').text
            difference_score_p1 = int(p1_home) - int(p1_away)
        except NoSuchElementException:
            difference_score_p1 = None
            exclusion = exclusion + ' 5 '
        try:
            p2_home = driver.find_element_by_class_name('p2_home').text
            p2_away = driver.find_element_by_class_name('p2_away').text
            difference_score_p2 = int(p2_home) - int(p2_away)
        except NoSuchElementException:
            difference_score_p2 = None
            exclusion = exclusion + ' 6 '
        try:
            p3_home = driver.find_element_by_class_name('p3_home').text
            p3_away = driver.find_element_by_class_name('p3_away').text
            difference_score_p3 = int(p3_home) - int(p3_away)
        except NoSuchElementException:
            difference_score_p3 = None
            exclusion = exclusion + ' 7 '
        try:
            p4_home = driver.find_element_by_class_name('p4_home').text
            p4_away = driver.find_element_by_class_name('p4_away').text
            difference_score_p4 = int(p4_home) - int(p4_away)
        except NoSuchElementException:
            difference_score_p4 = None
            exclusion = exclusion + ' 8 '

        try:
            time.sleep(1)
            r = driver.find_elements_by_class_name('odds-wrap')
            re = driver.find_element_by_class_name('odds-wrap').text
            try:
                t_1 = r[2].text.split('\n')
                t_2 = r[3].text.split('\n')
            except IndexError:
                t_1 = r[0].text.split('\n')
                t_2 = r[1].text.split('\n')
            if re != '':
                cof_win_team_1 = t_1[0]
                cof_win_team_2 = t_2[0]
                if cof_win_team_1 != '-' and cof_win_team_2 != '-':
                    cof_win_team_1 = float(cof_win_team_1)
                    cof_win_team_2 = float(cof_win_team_2)
                    cof_difference = cof_win_team_1 - cof_win_team_2
                else:
                    cof_win_team_1 = None
                    cof_win_team_2 = None
                    cof_difference = None
            else:
                cof_win_team_1 = None
                cof_win_team_2 = None
                cof_difference = None

        except NoSuchElementException:
            cof_win_team_1 = None
            cof_win_team_2 = None
            cof_difference = None
            exclusion = exclusion + ' 9 '

        link_game = driver.current_url

        lig = driver.find_element_by_xpath("//div[@class='fleft']/span[2]").text
        q = lig.split(' - ')
        r = q[0]
        dict_lig = {'ВЕЛИКА БРИТАНІЯ: ББЛ': 'united-kingdom bbl-2018-2019',
                    'ІТАЛІЯ: А2 - Плей-аут': 'italy a2-play-out-2018-2019',
                    'ЯПОНІЯ: B.League': 'japan b-league-2018-2019',
                    'ПОЛЬЩА: Таурон Баскет Ліга': 'poland tauron-basket-liga-2018-2019',
                    'ІТАЛІЯ: А2 Захід': 'italy a2-west-2018-2019',
                    'ВЕЛИКА БРИТАНІЯ: Трофей ББЛ': 'united-kingdom bbl-trophy-2018-2019',
                    'ІСПАНІЯ: АКБ': 'spain acb-2018-2019',
                    'ФРАНЦІЯ: ЛНБ': 'france lnb-2018-2019',
                    'НІМЕЧЧИНА: Про А': 'germany pro-a-2018-2019',
                    'ІТАЛІЯ: Ліга А': 'italy lega-a-2018-2019',
                    'ІТАЛІЯ: А2 Схід': 'italy a2-east-2018-2019',
                    'ФІНЛЯНДІЯ: Корісліга': 'finland korisliiga-2018-2019',
                    'ВЕЛИКА БРИТАНІЯ: Кубок ББЛ': 'united-kingdom bbl-cup-2018-2019',
                    'ТУРЕЧЧИНА: Суперліга': 'turkey super-ligi-2018-2019',
                    'НІМЕЧЧИНА: ББЛ': 'germany bbl-2018-2019',
                    'НІМЕЧЧИНА: Pro B': 'germany pro-b-2018-2019',
                    'ІТАЛІЯ: А2 - Плей-оф': 'italy a2-play-offs-2018-2019'}
        key = r
        if key in dict_lig:
            f = dict_lig[key]
        liga = f

        cursor.execute(
            "insert into bask_all (exclusion,data, team_home, team_awey, cof_team_1, cof_team_2, cof_difference,"
            " team_home_score, team_awey_score, difference_score_game, difference_score_p1, difference_score_p2,"
            "difference_score_p3, difference_score_p4, liga, link_game) "
            "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            (exclusion, time_game, team_home, team_awey, cof_win_team_1, cof_win_team_2, cof_difference,
             team_home_score, team_awey_score, difference_score_game, difference_score_p1, difference_score_p2,
             difference_score_p3, difference_score_p4, liga, link_game))
        cursor.close()
        connection.close()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.quit()


def going_match():
    time.sleep(1)
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



chrome_opt = Options()
chrome_opt.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\zheny\PycharmProjects\Bot1\chromedriver.exe')
# ,chrome_options=chrome_opt)

driver.get('https://www.myscore.ua/basketball')

going_match()
game()
