from selenium import webdriver
import pyautogui as pg
import time

class Downloader:
    def __init__(self):
        options=webdriver.FirefoxOptions()
        options.add_argument('lang=pt-br')
        self.driver=webdriver.Firefox(executable_path=r'./geckodriver.exe')

    def start(self,links):
        self.driver.get('https://ytmp3.cc/en13/')
        time.sleep(25)
        first=False
        for link in links:
            time.sleep(6)
            box=self.driver.find_element_by_id('input')
            box.click()
            box.send_keys(link)

            convert=self.driver.find_element_by_id('submit')
            convert.click()

            time.sleep(5)

            buttons=self.driver.find_element_by_id('buttons')
            dwnld_button=buttons.find_element_by_xpath('.//*')
            dwnld_button.click()
            time.sleep(6)

            if not first:
                pg.press('down')
                first=True
            pg.press('enter')
            time.sleep(3)

            pg.moveTo(434,15)
            pg.click()
            pg.moveTo(747,51)
            pg.click()
            pg.press('enter')
        
        pg.moveTo(1341,14)
        pg.click()

links=["https://www.youtube.com/watch?v=ApXoWvfEYVU&feature=youtu.be"]
sla=Downloader()
sla.start(links)
