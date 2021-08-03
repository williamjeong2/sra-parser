
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import argparse
import os.path
import os
import sys

def main(file_path, save_path):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    prefs = {'download.default_directory' : str(save_path)}
    chrome_options.add_experimental_option('prefs', prefs)
    path_chrome = './chromedriver'
    driver = webdriver.Chrome(path_chrome, chrome_options=chrome_options)

    lines = open(file_path, 'r').read().split('\n')
    for each_line in lines:
        # skip empty line
        if each_line == "":
            continue
        # If the file is already prepared, skip
        if os.path.isfile(os.getcwd() + "/" + save_path + each_line + ".1"):
            print(each_line+" is already existed.")
            continue
        URL = 'https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?run=' + each_line

        print('Downloading File : {}'.format(each_line))
        # driver = webdriver.Safari()
        # 사이트로 주소로 이동
        driver.get(url=URL)
        # data access 클릭
        driver.find_element_by_xpath('//*[@id="sra-viewer-app"]/ul/li[4]/a/span').click()
        # 링크 클릭
        if each_line.find("SRR") >= 0:
            driver.find_element_by_xpath('//*[@id="sra-viewer-app"]/div[4]/div[1]/div/table/tbody/tr[1]/td[4]/a').click() # SRA
        if each_line.find("ERR") >= 0:
            driver.find_element_by_xpath('//*[@id="sra-viewer-app"]/div[4]/div[1]/div/table/tbody/tr[3]/td[2]/a').click() # ERR
        
        time.sleep(300)
    open(file_path, 'r').close()


def get_arguments():
    parser = argparse.ArgumentParser(description = 'SRR Downloder')
    parser.add_argument('--file', required=True, help="Text file with SRR number")
    parser.add_argument('--out', required=True, help='Path to save')

    file_path = parser.parse_args().file
    save_path = parser.parse_args().out

    return file_path, save_path


if __name__ == '__main__':
    file_path, save_path = get_arguments()
    main(file_path, save_path)
    os.system('ls '+save_path+' | while read result;\
        do\
            fasterq-dump '+save_path+'$result --split-files -O '+save_path+' -e '+os.cpu_count()+ ' -p;\
                echo $result;\
        done')
    sys.exit()
