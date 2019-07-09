from rakuten.service.base.rakuten import *
from rakuten.util.browser import Browser
import re
import time
import os


def check_master_all_derectory_id_and_tag_id(driver: WebDriver):
    try:
        driver.get("https://rosie.rms.rakuten.co.jp/master/assist/tag/show?dirgenre=&addtags=&target=tag_id" +
                   "&serviceid=nrms&detailSellType=0&medicineFlag=0&usedTagType=2")
        elem_step_1 = driver.find_element_by_xpath("descendant::div[contains(@class, 'block-step step-1')]")
        elem_step_2 = driver.find_element_by_xpath("descendant::div[contains(@class, 'block-step step-2')]")

        step_1_block = elem_step_1.find_element_by_xpath(
            "descendant::div[contains(@class, 'block-category clearfix block-list js-block-category')]")

        browser = Browser(driver)
        top_index = 0
        directory_tab_index = [top_index]
        all_item_directory_list = []
        while True:
            while True:
                print(directory_tab_index)
                # browser.scroll_by_elem_and_offset(elem_step_1)
                time.sleep(0.1)
                step_1_display_last_list = \
                    __get_directory_list(step_1_block)[len(directory_tab_index)-1].find_elements_by_tag_name("li")
                if len(step_1_display_last_list) - 1 < directory_tab_index[-1]:
                    print("this category is finished")
                    directory_tab_index.pop(-1)
                    if len(directory_tab_index) > 0:
                        directory_tab_index[-1] += 1
                    break
                print("directory click")
                each_data = step_1_display_last_list[directory_tab_index[-1]]
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, each_data.text)))
                each_data.click()
                time.sleep(0.1)
                last_data = __get_directory_list(step_1_block)[-1].find_elements_by_tag_name("li")[0].text
                if last_data == "「全商品ディレクトリID」は\n選択完了しました。":
                    print("directory id is found")
                    elem_display_directory_info = elem_step_1.find_element_by_xpath(
                        "descendant::div[contains(@class, 'breadcrumb js-breadcrumb')]")
                    all_item_directory_id = \
                        elem_display_directory_info.find_elements_by_tag_name("ul")[0].find_elements_by_tag_name("li")[1].text
                    all_item_directory_path = \
                        re.sub('ディレクトリパス：', '', elem_display_directory_info.find_elements_by_tag_name("ul")[1].text)

                    browser.scroll_by_elem_and_offset(elem_step_2, 100)
                    all_item_directory_list.append({"id": all_item_directory_id,
                                                    "path": all_item_directory_path.replace("\n", ""),
                                                    "tag": []})
                    directory_tab_index[-1] += 1
                else:
                    # 次のリストがあるためそのインデックスを作成
                    directory_tab_index.append(0)
                    print("next category is found\n")
            if len(directory_tab_index) == 0:
                break
        with open(os.getcwd() + "\\data\\sql\\all_directory_id.txt", mode="a") as f:
            f.write("insert into all_item_derectory_id (name, derectory_id) values ")
            for index, all_item_directory in enumerate(all_item_directory_list):
                f.write("('" +
                        str(all_item_directory["path"]).replace("'", "''") +
                        "', " + all_item_directory["id"] + ")")
                if index == len(all_item_directory_list) - 1:
                    f.write(";\n")
                else:
                    f.write(",\n")

            f.close()
    except CustomError as e:
        raise CustomError(e)
    return


def __get_directory_list(step_block):
    return step_block.find_elements_by_xpath(
        "descendant::div[contains(@class, 'part-category js-category')]")


def __get_tag_list(driver: WebDriver, elem_tag_id_area: WebElement):
    tag_id_list = []
    elem_category_list = elem_tag_id_area.find_element_by_xpath(
        "descendant::div[contains(@class, 'part-category js-category')]").find_elements_by_tag_name("li")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-check")))
    print("tag id start")
    for index, elem_category in enumerate(elem_category_list):
        elem_category.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "item")))
        elem_tag_id_list = elem_tag_id_area.find_element_by_xpath(
            "descendant::div[contains(@class, 'part-category part-tag js-category js-tag-list')]")
        for elem_tag_id in elem_tag_id_list.find_elements_by_tag_name("ul")[index].find_elements_by_tag_name("li"):
            print(elem_tag_id.text)
            tag_id_list.append({"name": elem_category.text + " > " + elem_tag_id.text,
                                "tag_id": elem_tag_id.get_attribute("data-id")})
    print("tag id end")
    return tag_id_list
