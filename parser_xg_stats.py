from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def take_xg(driver):
    for e in range(1, 4):
        driver.find_element(By.XPATH, f"//*[@class='filters']/div[2]/label[{e}]").click()

        kol_komand = len(driver.find_elements(By.XPATH, '//*[@id="league-chemp"]/table/tbody/tr'))
        link_team_list = []
        for i in range(1, kol_komand + 1):
            tr_line_lig_xg = driver.find_elements(By.XPATH, f"//*[@id='league-chemp']/table/tbody/tr[{i}]")
            for j in tr_line_lig_xg:
                line_command_xg = j.text
                print(line_command_xg)

            link_team = driver.find_element(By.XPATH, f"//*[@id='league-chemp']/table/tbody/tr[{i}]/td/a") \
                .get_attribute('href')
            link_team_list.append(link_team)
    return link_team_list


def open_all_xg(driver):
    driver.find_element(By.XPATH, '//*[@id="league-chemp"]/div[1]/button').click()
    open_all_xg = driver.find_elements(By.CLASS_NAME, "row-display")
    for i in range(0, 20):
        if i == 0:
            open_all_xg[i].click()
        elif i == 10:
            open_all_xg[i].click()
        elif 11 < i <= 17:
            open_all_xg[i].click()
    driver.find_element(By.CLASS_NAME, "button-apply").click()


def open_all_xg_player(driver):
    driver.find_element(By.XPATH, '//*[@id="team-players"]/div[1]/button').click()

    for i in range(1, 25):
        if i == 1 or i == 7 or i == 12 or i == 14 or i == 15 or i == 17 or i == 19 or i == 20 or i == 21 or i == 22 \
                or i == 23 or i == 24:
            driver.find_element(By.XPATH, f'//*[@id="team-players"]/div[2]/div[2]/div/div[{i}]/div[2]').click()
    driver.find_element(By.XPATH, '//*[@id="team-players"]/div[2]/div[3]/a[2]').click()


def close_nomer(driver):
    driver.find_element(By.XPATH, '//*[@id="team-statistics"]/div[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="team-statistics"]/div[2]/div[2]/div/div[1]/div[2]').click()
    driver.find_element(By.XPATH, '//*[@id="team-statistics"]/div[2]/div[3]/a[2]').click()


def take_xg_team_situation(driver):
    kol_el = len(driver.find_elements(By.XPATH, '//*[@id="team-statistics"]/table/tbody/tr'))
    kol_vkladok_team = driver.find_elements(By.XPATH, f"//*[@class='filters']/div/label")
    for ii in kol_vkladok_team[:-2]:
        driver.execute_script("arguments[0].click();", ii)
        for i in range(1, kol_el + 1):
            team_situation = driver.find_elements(By.XPATH, f'//*[@id="team-statistics"]/table/tbody/tr[{i}]')
            for j in team_situation:
                line_team_situation = j.text
                print(line_team_situation)


def take_xg_players(driver):
    kol_el_gamers = len(driver.find_elements(By.XPATH, '//*[@id="team-players"]/table/tbody/tr'))
    for i in range(1, kol_el_gamers + 1):
        gamer_xg = driver.find_elements(By.XPATH, f'//*[@id="team-players"]/table[1]/tbody[1]/tr[{i}]')
        for j in gamer_xg:
            line_gamer_xg = j.text
            print(line_gamer_xg)


def main():
    chrome_opt = Options()
    chrome_opt.add_argument("--headless")
    chrome_opt.add_argument("--disable-gpu")
    chrome_opt.add_argument("--window-size=1920,1080")
    service = Service('chromedriver.exe')
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    driver = webdriver.Chrome(options=chrome_opt,
                              service=service,
                              desired_capabilities=capabilities)

    link_team_list = []

    links = ["https://understat.com/league/EPL/2021",
             "https://understat.com/league/La_liga/2021",
             "https://understat.com/league/Bundesliga/2021",
             "https://understat.com/league/Serie_A/2021",
             "https://understat.com/league/Ligue_1/2021"]
    stop = 0
    for i in links:
        driver.get(i)
        if stop == 0:
            open_all_xg(driver)
            stop += 1
        link_team_list.append(take_xg(driver))
    stop = 0
    for i in link_team_list:
        for j in i:
            driver.get(j)
            if stop == 0:
                close_nomer(driver)
                open_all_xg_player(driver)
                stop += 1
            take_xg_team_situation(driver)
            take_xg_players(driver)
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
