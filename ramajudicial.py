from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from datetime import date, datetime, timedelta

import time
import dateparser
import logging

URL = 'https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx'

def start_session():
    global driver
    global wait
    logging.info('Rama Judicial: Starting selenium session')
    driver = WebDriver(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities={'browserName': 'chrome'})
    wait = WebDriverWait(driver, 10)


def verify_process(process_id, city, entity):
    logging.info('Rama Judicial: Starting process verification with id (radicado): {process_id}'.format(process_id=process_id))
    for retry in range(2):
        logging.info('Rama Judicial: Retry {retry}'.format(retry=retry+1))
        try:
            driver.get(URL)
            logging.info('Rama Judicial: Selecting city {city}'.format(city=city))
            citySelect = Select(driver.find_element_by_id('ddlCiudad'))
            citySelect.select_by_value(city)
            time.sleep(5)
            logging.info('Rama Judicial: Selecting entity {entity}'.format(entity=entity))
            entitySelect = Select(driver.find_element_by_id('ddlEntidadEspecialidad'))
            entitySelect.select_by_value(entity)
            time.sleep(5)
            logging.info('Rama Judicial: Setting process id')
            process = driver.find_element_by_css_selector('#divNumRadicacion tr:nth-child(2) input')
            process.send_keys(process_id)
            logging.info('Rama Judicial: Clicking slide captcha')
            slider = driver.find_element_by_id('sliderBehaviorNumeroProceso_railElement')
            ActionChains(driver).move_to_element(slider).move_by_offset(10, 0).click().perform()
            searchBtn = driver.find_element_by_css_selector('#divNumRadicacion input[value=Consultar]')
            searchBtn.click()
            logging.info('Rama Judicial: Waiting for results')
            wait.until(lambda d: d.find_element_by_css_selector('#divActuacionesDetalle tr.tr_contenido:nth-child(2) td:first-child span').is_displayed())
            logging.info('Rama Judicial: Reading results')
            updatedDateCell = driver.find_element_by_css_selector('#divActuacionesDetalle tr.tr_contenido:nth-child(2) td:first-child span')
            updatedDate = dateparser.parse(updatedDateCell.text).date()
            yesterday = date.today() - timedelta(days=1)
            logging.info('Rama Judicial: Verification process finished')
            return updatedDate == yesterday
        except:
            logging.exception('Rama Judicial retry failure')
    raise VerificationError('Error during verification of process {id}'.format(id = process_id))

def end_session():
    logging.info('Rama Judicial: Ending selenium session')
    driver.quit()

class VerificationError(Exception):
    pass