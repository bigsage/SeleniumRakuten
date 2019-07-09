from rakuten.dao.client_dao import ClientDao
from rakuten.dao.item_dao import ItemDao
from rakuten.dao.item_image_dao import ItemImageDao
from rakuten.dao.client_item_choice_dao import ClientItemChoiceDao
from rakuten.dao.delete_item_management_dao import DeleteItemManagementDao
from rakuten.util.config import *
from rakuten.util.csv import *
from rakuten.entity.delete_item_management_entity import DeleteItemManagementEntity
from selenium import webdriver
from rakuten.service.base.rakuten import *
from rakuten.util.encrypt import Encrypt
from rakuten.util.logger import Logger
from tkinter import filedialog
import sys
import tkinter


class Kkoichan(RakutenService):
    __header = None
    __TEST_MODE = False
    if __TEST_MODE:
        __client_id = 1
    else:
        __client_id = 1

    @classmethod
    def convert(cls, preg_item_number: str):
        try:
            cls.__header = get_csv_config()

            client = ClientDao.get_client(cls.__client_id)
            root = tkinter.Tk()
            root.withdraw()
            file_type = [("CSVファイル", "*.csv")]
            file_name = filedialog.askopenfilename(
                filetypes=file_type, initialdir=client.client_original_data_site_collection[0].path)
            df = read_sjis_csv(file_name)

            df = cls.__get_variable_data(df, preg_item_number)
            ItemDao.create_item_list_by_color_me(cls.__client_id, df)
        except Exception as e:
            print(e)

    @classmethod
    def update_rms_pass(cls, rms_pass: str):
        try:
            ClientDao.update_rms_pass(cls.__client_id, rms_pass)
        except Exception as e:
            print(e)

    @classmethod
    def update_item_image(cls):
        try:
            cls.__header = get_image_judge_config()
            root = tkinter.Tk()
            root.withdraw()
            file_type = [("CSVファイル", "*.csv")]
            file_name = filedialog.askopenfilename(filetypes=file_type, initialdir=os.getcwd() + "\\data\\csv")
            df = read_sjis_csv(file_name)
            result_df = df[df[cls.__header["image_url"]].str.match("https://.+")]
            num = ItemImageDao.update_item_image(client_id=cls.__client_id, df=result_df)
            client_entity = ClientDao.get_client(cls.__client_id)
            log_msg = "商品画像の判定更新を行いました。：計" + str(num)
            print(log_msg)
            Logger.write(client_entity.name, log_msg)
        except Exception as e:
            print(e)

    @classmethod
    def input(cls):
        try:
            item_entity_list = ItemDao.get_item_list(cls.__client_id)
            client_entity = ClientDao.get_client(cls.__client_id)
            cls.driver = webdriver.Chrome("C:/Drivers/chromedriver.exe")
            cls.driver.get(cls.TARGET_DOMAIN)
            # move login page and login
            try:
                cls.login(
                    client_entity.rms_id, Encrypt.decrypt(client_entity.rms_pass),
                    client_entity.mail_address, Encrypt.decrypt(client_entity.password))
            except CustomError as e:
                print(e)
                return

            # input item info
            browser = Browser(cls.driver)
            success_item_list = []

            for index, item_entity in enumerate(item_entity_list):
                try:
                    cls.move_regist_page()
                    elem_header = get_elem_regist_header(cls.driver)
                    browser.scroll_by_elem_and_offset(elem_header, 0)

                    cls.set_item_number(item_entity.item_number)
                    cls.set_item_name(item_entity.name)
                    cls.set_item_pc_catch_copy(item_entity.catch_copy_for_pc)
                    cls.set_item_mobile_catch_copy(item_entity.catch_copy_for_mobile)
                    elem_item_price = cls.set_item_price(item_entity.price)

                    browser.scroll_by_elem_and_offset(elem_item_price, 0)

                    cls.set_item_display_price(item_entity.item_display_price_collection[0])
                    cls.set_item_consump_tax_type(item_entity.item_consump_tax_type_collection[0])
                    cls.set_item_shipping_cost_type(item_entity.item_shipping_cost_type_collection[0])
                    cls.set_item_cod_type(item_entity.item_cod_type_collection[0])
                    cls.set_item_noshi_type(item_entity.item_noshi_type_collection[0])
                    cls.set_item_order_button_type(item_entity.item_order_button_type_collection[0])
                    cls.set_item_document_request_type(item_entity.item_document_request_type_collection[0])
                    cls.set_item_inquiry_button_type(item_entity.item_inquiry_button_type_collection[0])
                    cls.set_item_restock_button_type(item_entity.item_restock_button_type_collection[0])
                    elem_item_sales_period = cls.set_item_sales_period(item_entity.item_sales_period_collection)

                    browser.scroll_by_elem_and_offset(elem_item_sales_period, 0)

                    cls.set_item_reception_num_type(item_entity.item_reception_num_type_collection[0])
                    cls.set_item_stock_type(item_entity.item_stock_type_collection[0])
                    cls.set_item_amount_stock(item_entity.amount_stock)
                    cls.set_item_stock_display_type(item_entity.item_stock_display_type_collection[0])
                    cls.set_item_order_sold_out_flg(item_entity.order_sold_out_flg)
                    elem_delivery_info = \
                        cls.set_item_delivery_info_display_list(item_entity.item_delivery_info_display_collection)

                    browser.scroll_by_elem_and_offset(elem_delivery_info, 60)

                    cls.set_item_description_for_pc(item_entity.description_for_pc)
                    cls.set_item_description_for_mobile(item_entity.description_for_mobile)
                    elem_desc_for_pc_sale = cls.set_item_description_for_pc_sale(item_entity.description_for_pc_sale)

                    browser.scroll_by_elem_and_offset(elem_desc_for_pc_sale, 60)

                    elem_item_image = cls.set_item_image_list(item_entity.item_image_collection)

                    browser.scroll_by_elem_and_offset(elem_item_image, 100)

                    cls.set_item_white_bg_image(item_entity.white_bg_image_collection)
                    elem_movie_html = cls.set_item_movie_url(item_entity.movie_html)

                    browser.scroll_by_elem_and_offset(elem_movie_html, 100)

                    cls.set_item_all_item_directory_id(item_entity.item_all_item_directory_id_collection[0])
                    cls.set_item_tag_id(item_entity.item_tag_id_collection)
                    cls.set_item_catalog_id(item_entity.catalog_id_collection[0])
                    cls.set_item_display_manufacturer_info_flg(item_entity.display_manufacturer_info_flg)
                    elem_display_category = \
                        cls.set_item_display_category_list(item_entity.item_display_category_collection)

                    browser.scroll_by_elem_and_offset(elem_display_category, 200)

                    cls.set_item_shop_category_display_rank(item_entity.shop_category_display_rank)
                    cls.set_item_search_not_display_flg(item_entity.search_not_display_flg)
                    cls.set_item_black_market_password(item_entity.black_market_password)
                    elem_warehouse_type = cls.set_item_warehouse_type(item_entity.item_warehouse_type_collection[0])

                    browser.scroll_by_elem_and_offset(elem_warehouse_type, 0)

                    cls.set_item_every_item_stock(item_entity.every_item_stock_collection)
                    cls.set_item_point_conversion_info(item_entity.item_point_conversion_info_collection)

                    cls.submit()

                    success_item_list.append(item_entity)
                    print("item_id: {0} : is registed".format(str(item_entity.id)))
                except CustomError as e:
                    tb = sys.exc_info()[2]
                    print("item_id: {0} : {1}".format(str(item_entity.id), e.with_traceback(tb)))

            ItemDao.update_registed_item(success_item_list)
            cls.driver.quit()
        except Exception as e:
            print(e)

    @classmethod
    def add_browser_item_style(cls):
        try:
            client_entity = ClientDao.get_client(cls.__client_id)
            cls.driver = webdriver.Chrome("C:/Drivers/chromedriver.exe")
            cls.driver.get(cls.TARGET_DOMAIN)
            # move login page and login
            try:
                cls.login(
                    client_entity.rms_id, Encrypt.decrypt(client_entity.rms_pass),
                    client_entity.mail_address, Encrypt.decrypt(client_entity.password))
            except CustomError as e:
                print(e)
                return

            # input item info
            browser = Browser(cls.driver)
            item_entity_list = ItemDao.get_item_no_style_list(cls.__client_id)
            client_item_choice_list = ClientItemChoiceDao.get_client_item_choice_list(cls.__client_id)
            print("a total of item is {0}".format(str(len(item_entity_list))))
            success_item_list = []
            failure_item_list = []
            for each_item in item_entity_list:
                try:
                    cls.move_item_list_page()
                    cls.search_item_name(each_item.name)
                    result_url_list = cls.get_search_result_url_list()
                    # 同名の商品名を登録可能なので、その場合全て変更する
                    for result_url in result_url_list:
                        cls.add_item_style(each_item, result_url, client_item_choice_list)
                    success_item_list.append(each_item)
                    print("update style: item_id: {0} : success".format(str(each_item.id)))
                except CustomError as e:
                    tb = sys.exc_info()[2]
                    failure_item_list.append((each_item))
                    print("update style: item_id: {0} : {1}".format(str(each_item.id), e.with_traceback(tb)))
            ItemDao.update_registed_style_item(success_item_list)
            for each_item in failure_item_list:
                print("failure item_id : {0}".format(str(each_item.id)))
            cls.driver.quit()
        except Exception as e:
            print(e)

    @classmethod
    def check_item_of_no_image(cls):
        try:
            client_entity = ClientDao.get_client(cls.__client_id)
            cls.driver = webdriver.Chrome("C:/Drivers/chromedriver.exe")
            cls.driver.get(cls.TARGET_DOMAIN)
            # move login page and login
            try:
                cls.login(
                    client_entity.rms_id, Encrypt.decrypt(client_entity.rms_pass),
                    client_entity.mail_address, Encrypt.decrypt(client_entity.password))
            except CustomError as e:
                print(e)
                return

            # input item info
            cls.move_item_list_page()
            delete_item_managed_list = []
            # 商品一覧画面で商品画像が表示されてないものを抽出
            while True:
                item_list = cls.get_search_result_list()
                for elem_each_item in item_list:
                    if cls.is_deleted_image_for_item_search_list(elem_each_item):
                        item_name = elem_each_item.find_elements_by_tag_name("td")[3].text
                        item_managed_num = elem_each_item.find_elements_by_tag_name("td")[5].text
                        delete_item_managed_list.append(
                            DeleteItemManagementEntity(cls.__client_id, item_name, item_managed_num))
                if cls.is_search_last_page():
                    break
                cls.driver.find_element_by_class_name("page-next").find_element_by_tag_name("a").click()
                wait_reload_item_list(cls.driver)

            DeleteItemManagementDao.create_list(delete_item_managed_list)
            log_txt = "num of no imaged items : {0}".format(str(len(delete_item_managed_list)))
            print(log_txt)
            Logger.write(client_entity.name, log_txt)
            cls.driver.quit()
        except Exception as e:
            print(e)

    @classmethod
    def delete_item_of_no_image(cls):
        try:
            client_entity = ClientDao.get_client(cls.__client_id)
            cls.driver = webdriver.Chrome("C:/Drivers/chromedriver.exe")
            cls.driver.get(cls.TARGET_DOMAIN)
            # move login page and login
            try:
                cls.login(
                    client_entity.rms_id, Encrypt.decrypt(client_entity.rms_pass),
                    client_entity.mail_address, Encrypt.decrypt(client_entity.password))
            except CustomError as e:
                print(e)
                return

            # input item info
            cls.move_item_list_page()
            delete_item_managed_list = DeleteItemManagementDao.get_not_deleted_list(cls.__client_id)
            success_delete_list = []
            failure_delete_list = []
            # 対象商品を検索して削除
            for each_entity in delete_item_managed_list:
                try:
                    cls.move_item_list_page()
                    cls.search_item_managed_number(each_entity.managed_number)
                    cls.delete_item(cls.get_search_result_list()[0])
                    success_delete_list.append(each_entity)
                except CustomError:
                    failure_delete_list.append(each_entity)

            DeleteItemManagementDao.update_delete_flg_list(success_delete_list)
            print("num of failured item : {0}".format(str(len(failure_delete_list))))
            print(failure_delete_list)
            Logger.write(client_entity.name, "item delete is success: {0} : {1}".format(
                str(len(success_delete_list)), ",".join(success_delete_list)))
            Logger.write(client_entity.name, "item delete is failure: {0} :{1}".format(
                str(len(failure_delete_list)), ",".join(failure_delete_list)))
            cls.driver.quit()
        except Exception as e:
            print(e)

    @classmethod
    def __get_variable_data(cls, df: pandas.DataFrame, preg_item_number: str) -> pandas.DataFrame:
        result_df = df[df[cls.__header["item_name"]].str.match(".+" + preg_item_number)]
        return result_df
