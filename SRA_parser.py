
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
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
import time

def main(file_path, save_path):
    
    # chrome_options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    prefs = {'download.default_directory' : str("/home/" + save_path)}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)

    lines = open("/home/" + file_path, 'r').read().split('\n')
    for each_line in lines:
        # skip empty line
        if each_line == "":
            continue
        # If the file is already prepared, skip
        if os.path.isfile("/home/" + save_path + each_line + ".1"):
            print(each_line+" is already existed.")
            continue
        URL = 'https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?run=' + each_line

        print('Downloading File : {}'.format(each_line))
        # driver = webdriver.Safari()
        # move to url address
        driver.get(url=URL)
        # data access
        driver.find_element(By.XPATH, '//*[@id="sra-viewer-app"]/ul/li[4]/a/span').click()
        # driver.find_element_by_xpath('//*[@id="sra-viewer-app"]/ul/li[4]/a/span').click() # deprecated
        # click link
        if each_line.find("SRR") >= 0:
            driver.find_element(By.XPATH, '//*[@id="sra-viewer-app"]/div[4]/div[1]/div/table/tbody/tr[1]/td[4]/a').click() # SRA
        if each_line.find("ERR") >= 0:
            driver.find_element(By.XPATH, '//*[@id="sra-viewer-app"]/div[4]/div[1]/div/table/tbody/tr[3]/td[2]/a').click() # ERR

        while not os.path.exists("/home/" + save_path + each_line + ".1"):
            time.sleep(1)
    open("/home/" + file_path, 'r').close()


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
    os.system('ls /home/'+save_path+' | while read result;\
        do\
            if [[ $result != *.fastq ]] ;\
            then\   
                fasterq-dump /home/'+save_path+'$result --split-files -O /home/'+save_path+' -e '+str(os.cpu_count())+ ' -p;\
                echo $result; fi\
        done')
    sys.exit()
