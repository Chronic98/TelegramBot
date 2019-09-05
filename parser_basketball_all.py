import time

import psycopg2
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import config


def going_all_math_lig():
    stop = 1
    iiiii = 0
    time.sleep(1)
    while stop < 5:
        cle = driver.find_element_by_id('tournament-page-results-more')
        cl = cle.text
        if cl != '':
            cle.click()
        else:
            stop = 10
        time.sleep(3)
    driver.find_element_by_class_name('head').click()
    lig = driver.current_url
    ligg = lig.split('/')
    liga = ligg[4] + ' ' + ligg[5]
    ell = driver.find_elements_by_class_name('cell_ad')
    for ii in ell:
        connection = psycopg2.connect(config.link_db)
        connection.autocommit = True
        cursor = connection.cursor()
        ii.click()
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
            r = driver.find_elements_by_class_name('odds-wrap')
            re = driver.find_element_by_class_name('odds-wrap').text
            if re != '':
                cof_win_team_1 = r[0].text
                cof_win_team_2 = r[1].text
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


chrome_opt = Options()
chrome_opt.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r'C:\Users\zheny\PycharmProjects\Bot1\chromedriver.exe',
                          chrome_options=chrome_opt)
li = {'https://www.myscore.ua/basketball/united-kingdom/bbl-2016-2017/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-2017-2018/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-2018-2019/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-cup-2016-2017/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-cup-2017-2018/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-cup-2018-2019/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-trophy-2016-2017/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-trophy-2017-2018/results/',
      'https://www.myscore.ua/basketball/united-kingdom/bbl-trophy-2018-2019/results/',
      'https://www.myscore.ua/basketball/spain/acb-2016-2017/results/',
      'https://www.myscore.ua/basketball/spain/acb-2017-2018/results/',
      'https://www.myscore.ua/basketball/spain/acb-2018-2019/results/',
      'https://www.myscore.ua/basketball/italy/lega-a-2016-2017/results/',
      'https://www.myscore.ua/basketball/italy/lega-a-2017-2018/results/',
      'https://www.myscore.ua/basketball/italy/lega-a-2018-2019/results/',
      'https://www.myscore.ua/basketball/italy/a2-west-2016-2017/results/',
      'https://www.myscore.ua/basketball/italy/a2-west-2017-2018/results/',
      'https://www.myscore.ua/basketball/italy/a2-west-2018-2019/results/',
      'https://www.myscore.ua/basketball/italy/a2-east-2016-2017/results/',
      'https://www.myscore.ua/basketball/italy/a2-east-2017-2018/results/',
      'https://www.myscore.ua/basketball/italy/a2-east-2018-2019/results/',
      'https://www.myscore.ua/basketball/italy/a2-play-offs-2016-2017/results/',
      'https://www.myscore.ua/basketball/italy/a2-play-offs-2017-2018/results/',
      'https://www.myscore.ua/basketball/italy/a2-play-offs-2015-2016/results/',
      'https://www.myscore.ua/basketball/italy/a2-play-out-2016-2017/results/',
      'https://www.myscore.ua/basketball/italy/a2-play-out-2017-2018/results/',
      'https://www.myscore.ua/basketball/italy/a2-play-out-2015-2016/results/',
      'https://www.myscore.ua/basketball/germany/bbl-2016-2017/results/',
      'https://www.myscore.ua/basketball/germany/bbl-2017-2018/results/',
      'https://www.myscore.ua/basketball/germany/bbl-2018-2019/results/',
      'https://www.myscore.ua/basketball/germany/pro-b-2017-2018/results/',
      'https://www.myscore.ua/basketball/germany/pro-b-2018-2019/results/',
      'https://www.myscore.ua/basketball/germany/pro-a-2016-2017/results/',
      'https://www.myscore.ua/basketball/germany/pro-a-2017-2018/results/',
      'https://www.myscore.ua/basketball/germany/pro-a-2018-2019/results/',
      'https://www.myscore.ua/basketball/poland/tauron-basket-liga-2016-2017/results/',
      'https://www.myscore.ua/basketball/poland/tauron-basket-liga-2017-2018/results/',
      'https://www.myscore.ua/basketball/poland/tauron-basket-liga-2018-2019/results/',
      'https://www.myscore.ua/basketball/turkey/super-ligi-2016-2017/results/',
      'https://www.myscore.ua/basketball/turkey/super-ligi-2017-2018/results/',
      'https://www.myscore.ua/basketball/turkey/super-ligi-2018-2019/results/',
      'https://www.myscore.ua/basketball/finland/korisliiga-2016-2017/results/',
      'https://www.myscore.ua/basketball/finland/korisliiga-2017-2018/results/',
      'https://www.myscore.ua/basketball/finland/korisliiga-2018-2019/results/',
      'https://www.myscore.ua/basketball/france/lnb-2016-2017/results/',
      'https://www.myscore.ua/basketball/france/lnb-2017-2018/results/',
      'https://www.myscore.ua/basketball/france/lnb-2018-2019/results/',
      'https://www.myscore.ua/basketball/japan/b-league-2016-2017/results/',
      'https://www.myscore.ua/basketball/japan/b-league-2017-2018/results/',
      'https://www.myscore.ua/basketball/japan/b-league-2018-2019/results/'
      }


def del_table():
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("delete from bask_all;")
    cursor.close()
    connection.close()


def gdf():
    connection = psycopg2.connect(config.link_db)
    connection.autocommit = True
    cursor = connection.cursor()
    time.sleep(1)
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
        r = driver.find_elements_by_class_name('odds-wrap')
        re = driver.find_element_by_class_name('odds-wrap').text
        if re != '':
            cof_win_team_1 = r[0].text
            cof_win_team_2 = r[1].text
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

    cursor.execute(
        "insert into bask_all (exclusion,data, team_home, team_awey, cof_team_1, cof_team_2, cof_difference,"
        " team_home_score, team_awey_score, difference_score_game, difference_score_p1, difference_score_p2,"
        "difference_score_p3, difference_score_p4, link_game) "
        "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        (exclusion, time_game, team_home, team_awey, cof_win_team_1, cof_win_team_2, cof_difference,
         team_home_score, team_awey_score, difference_score_game, difference_score_p1, difference_score_p2,
         difference_score_p3, difference_score_p4, link_game))

    cursor.close()
    connection.close()
    driver.close()

driver.close()
driver.quit()

