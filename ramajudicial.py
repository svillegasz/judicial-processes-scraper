from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from datetime import date, datetime, timedelta

import time
import dateparser

URL = 'https://procesos.ramajudicial.gov.co/procesoscs/ConsultaJusticias21.aspx'

def start_session():
    global driver
    global wait
    print('Rama Judicial: Starting selenium session')
    driver = WebDriver(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities={'browserName': 'chrome'})
    wait = WebDriverWait(driver, 10)


def verify_process(process_id, city, entity):
    driver.get(URL)
    print('Rama Judicial: Starting process verification with id (radicado): {process_id}'.format(process_id=process_id))
    print('Rama Judicial: Selecting city {city}'.format(city=city))
    citySelect = Select(driver.find_element_by_id('ddlCiudad'))
    citySelect.select_by_value(city)
    time.sleep(3)
    print('Rama Judicial: Selecting entity {entity}'.format(entity=entity))
    entitySelect = Select(driver.find_element_by_id('ddlEntidadEspecialidad'))
    entitySelect.select_by_value(entity)
    time.sleep(2)
    print('Rama Judicial: Setting process id')
    process = driver.find_element_by_css_selector('#divNumRadicacion tr:nth-child(2) input')
    process.send_keys(process_id)
    print('Rama Judicial: Clicking slide captcha')
    slider = driver.find_element_by_id('sliderBehaviorNumeroProceso_railElement')
    ActionChains(driver).move_to_element(slider).move_by_offset(10, 0).click().perform()
    searchBtn = driver.find_element_by_css_selector('#divNumRadicacion input[value=Consultar]')
    searchBtn.click()
    print('Rama Judicial: Waiting for results')
    wait.until(lambda d: d.find_element_by_css_selector('#divActuacionesDetalle tr.tr_contenido:nth-child(2) td:first-child span').is_displayed())
    print('Rama Judicial: Reading results')
    updatedDateCell = driver.find_element_by_css_selector('#divActuacionesDetalle tr.tr_contenido:nth-child(2) td:first-child span')
    updatedDate = dateparser.parse(updatedDateCell.text).date()
    yesterday = date.today() - timedelta(days=1)
    print('Rama Judicial: Verification process finished')
    return updatedDate == yesterday

def end_session():
    print('Rama Judicial: Ending selenium session')
    driver.quit()