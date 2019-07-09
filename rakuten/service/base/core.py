from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from typing import List


def get_elem_regist_header(driver: WebDriver) -> WebElement:
    return driver.find_element_by_tag_name("form")


def get_elem_radio_btn(driver: WebDriver, name: str, value: str) -> WebElement:
    return driver.find_element_by_css_selector("input[type='radio'][name='" + name + "'][value='" + value + "']")


def set_value_select_box(driver: WebDriver, name: str, value: str) -> WebElement:
    elem_select = driver.find_element_by_name(name)
    Select(elem_select).select_by_value(value)
    return elem_select


def get_validation_message(driver: WebDriver) -> str:
    elem_title = driver.find_element_by_xpath("descendant::*[contains(text(), '項目の入力エラーがあります。')]")
    elem_tbody = elem_title.find_element_by_xpath("ancestor::tbody[1]")
    return elem_tbody.find_element_by_xpath("./tr[1]/td/table/tbody/tr[0]").text


def wait_show_finish(driver: WebDriver):
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((
        By.XPATH, "descendant::*[contains(text(), '商品の登録が完了しました。')]")))


def wait_enabled_select_box(driver: WebDriver, elem_name: str):
    WebDriverWait(driver, 5).until(EC.element_to_be_selected(driver.find_element_by_name(elem_name)))


def wait_reload_item_list(driver: WebDriver):
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((
        By.XPATH, "descendant::*[contains(text(), '読み込み中です。少々お待ちください。')]")))


def is_image_correct(image_judge: str) -> bool:
    return image_judge != "×" and image_judge != "エラー"

