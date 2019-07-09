from rakuten.exception.custom import CustomError
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from rakuten.service.base.core import *
from rakuten.util.singleton import Singleton
from rakuten.util.browser import Browser
from rakuten.util.web_image import WebImage
import datetime
import time
import re
import cv2


class RakutenService(Singleton):
    driver: WebDriver = None
    TARGET_DOMAIN = "https://mainmenu.rms.rakuten.co.jp/rms"

    def __init__(self, driver):
        if self.driver is None:
            self.driver = driver

    @classmethod
    def login(cls, rms_id, rms_pass, mail_address, password):
        # R-Login
        try:
            rms_id_txt = cls.driver.find_element_by_name("login_id")
            rms_id_txt.send_keys(rms_id)
            rms_pass_txt = cls.driver.find_element_by_name("passwd")
            rms_pass_txt.send_keys(rms_pass)
            rms_login_btn = cls.driver.find_element_by_name("submit")
            rms_login_btn.click()
        except NoSuchElementException as e:
            raise CustomError("R-loginログイン情報入力欄が見つかりませんでした\n", e)

        try:
            cls.driver.find_element_by_xpath(
                "descendant::p[contains(@class, 'rf-form-login--input-error rf-form-message rf-form-error')]")
        except NoSuchElementException:
            print("R-Login is success")
        else:
            raise CustomError("R-Loginに失敗しました。IDかパスワードが間違っています。")

        # 楽天会員認証
        try:
            login_mailadderss_txt = cls.driver.find_element_by_name("user_id")
            login_mailadderss_txt.send_keys(mail_address)
            login_password_txt = cls.driver.find_element_by_name("user_passwd")
            login_password_txt.send_keys(password)
            login_btn = cls.driver.find_element_by_name("submit")
            login_btn.click()
        except NoSuchElementException as e:
            raise CustomError("楽天会員ログイン情報入力欄が見つかりませんでした\n", e)

        try:
            cls.driver.find_element_by_xpath(
                "descendant::p[contains(@class, 'rf-form-login--input-error rf-form-message rf-form-error')]")
        except NoSuchElementException:
            print("User-Login is success")
        else:
            raise CustomError("楽天Loginに失敗しました。ユーザIDかパスワードが間違っています。")

        # ホーム画面まで遷移
        try:
            cls.driver.find_element_by_name("submit").click()
            cls.driver.find_element_by_class_name("tac").click()
        except NoSuchElementException:
            print("ログイン後ホーム画面へ遷移中に必要な要素が見つかりませんでした。")

        return

    @classmethod
    def move_regist_page(cls):
        cls.driver.get("https://mainmenu.rms.rakuten.co.jp/")
        cls.driver.find_element_by_id("rmsUnder-navsetting").click()
        cls.driver.find_element_by_id("com_gnavi0101").click()
        cls.driver.find_element_by_id("mm_sub0101_05").click()
        cls.driver.find_element_by_link_text("商品個別登録").click()

    @classmethod
    def move_item_list_page(cls):
        cls.driver.get("https://mainmenu.rms.rakuten.co.jp/")
        cls.driver.find_element_by_id("rmsUnder-navsetting").click()
        cls.driver.find_element_by_id("com_gnavi0101").click()
        cls.driver.find_element_by_id("mm_sub0101_04").click()

    @classmethod
    def set_item_number(cls, item_number: str) -> WebElement:
        try:
            elem_input = cls.driver.find_element_by_name("item_number")
            if item_number is None:
                return elem_input
            elem_input.send_keys(item_number)
        except NoSuchElementException as e:
            raise CustomError("商品番号入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品番号入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品番号入力時に不明なエラーが出ました", e)
        return elem_input

    @classmethod
    def set_item_name(cls, item_name: str) -> WebElement:
        try:
            elem_input = cls.driver.find_element_by_name("item_name")
            elem_input.send_keys(item_name)
        except NoSuchElementException as e:
            raise CustomError("商品名入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品名入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品名入力時に不明なエラーが出ました", e)
        return elem_input

    @classmethod
    def set_item_pc_catch_copy(cls, txt: str) -> WebElement:
        try:
            elem_input = cls.driver.find_element_by_name("catch_copy")
            if txt is None:
                return elem_input
            elem_input.send_keys(txt)
        except NoSuchElementException as e:
            raise CustomError("PC用キャッチコピー入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("PC用キャッチコピー入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("PC用キャッチコピー入力時に不明なエラーが出ました", e)
        return elem_input

    @classmethod
    def set_item_mobile_catch_copy(cls, txt: str) -> WebElement:
        try:
            elem_input = cls.driver.find_element_by_name("mobile_catch_copy")
            if txt is None:
                return elem_input
            elem_input.send_keys(txt)
        except NoSuchElementException as e:
            raise CustomError("Mobile用キャッチコピー入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("Mobile用キャッチコピー入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("Mobile用キャッチコピー入力時に不明なエラーが出ました", e)
        return elem_input

    @classmethod
    def set_item_price(cls, txt: str) -> WebElement:
        try:
            elem_input = cls.driver.find_element_by_name("price")
            if txt is None:
                return elem_input
            elem_input.send_keys(txt)
        except NoSuchElementException as e:
            raise CustomError("販売価格入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("販売価格入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("販売価格入力時に不明なエラーが出ました", e)
        return elem_input

    @classmethod
    def set_item_display_price(cls, item_display_price_entity) -> WebElement:
        try:
            elem_dual_price_wording_select = set_value_select_box(
                cls.driver, "dual_price_id", item_display_price_entity.dual_price_wording.value)
            if item_display_price_entity.open_price_flg:
                get_elem_radio_btn(cls.driver, 'regular_price_type', "2").click()
                elem_regular_price = cls.driver.find_element_by_name("regular_price")
                if item_display_price_entity.display_price is None:
                    elem_regular_price.send_keys(item_display_price_entity.display_price)
            else:
                get_elem_radio_btn(cls.driver, 'regular_price_type', "1").click()
        except NoSuchElementException as e:
            raise CustomError("商品表示価格入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品表示価格入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品表示価格入力時に不明なエラーが出ました", e)
        return elem_dual_price_wording_select

    @classmethod
    def set_item_consump_tax_type(cls, item_consump_tax_type_entity) -> WebElement:
        try:
            elem_radio_btn = \
                get_elem_radio_btn(cls.driver, 'tax_flag', item_consump_tax_type_entity.consump_tax_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("消費税入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("消費税入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("消費税入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_shipping_cost_type(cls, item_shipping_cost_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'postage_flag', item_shipping_cost_type_entity.shipping_cost_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("送料入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("送料入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("送料入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_single_shipping_cost(cls, value: int) -> WebElement:
        try:
            elem_input = cls.driver.find_element_by_name("postage")
            if value is None:
                return elem_input
            elem_input.send_keys(str(value))
        except NoSuchElementException as e:
            raise CustomError("個別送料入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("個別送料入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("個別送料入力時に不明なエラーが出ました", e)
        return elem_input

    @classmethod
    def set_item_cod_type(cls, item_cod_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'daibiki_flag', item_cod_type_entity.cod_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("代引料入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("代引料入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("代引料入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_noshi_type(cls, item_noshi_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'noshi_flag', item_noshi_type_entity.noshi_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("のし対応入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("のし対応入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("のし対応入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_order_button_type(cls, item_order_button_type_entity) -> WebElement:
        try:
            radio_btn_value = item_order_button_type_entity.order_button_type.value
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'sell_flag', radio_btn_value)
            if radio_btn_value == 2:
                if item_order_button_type_entity.release_date is not None:
                    release_date = datetime.datetime(item_order_button_type_entity.release_date.year)
                    set_value_select_box(cls.driver, "release_date_year", str(release_date.year))
                    set_value_select_box(cls.driver, "release_date_month", str(release_date.month))
                    set_value_select_box(cls.driver, "release_date_day", str(release_date.day))
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("注文ボタン入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("注文ボタン入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("注文ボタン入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_document_request_type(cls, item_document_request_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'panf_flag', item_document_request_type_entity.document_request_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("資料請求ボタン入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("資料請求ボタン入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("資料請求ボタン入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_inquiry_button_type(cls, item_inquiry_button_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'ask_flag', item_inquiry_button_type_entity.inquiry_button_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("問い合わせボタン入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("問い合わせボタン入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("問い合わせボタン入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_restock_button_type(cls, item_restock_button_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'stock_notify_flag', item_restock_button_type_entity.restock_button_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("再入荷お知らせボタン入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("再入荷お知らせボタン入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("再入荷お知らせボタン入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_sales_period(cls, item_sales_period_list) -> WebElement:
        try:
            elem_select = cls.driver.find_element_by_name("sale_stime_year")
            if len(item_sales_period_list) == 0:
                return elem_select
            item_sales_period_entity = item_sales_period_list[0]
            if item_sales_period_entity.start_date is not None:
                start_date = datetime.datetime(item_sales_period_entity.start_date)
                set_value_select_box(cls.driver, "sale_stime_year", str(start_date.year))
                set_value_select_box(cls.driver, "sale_stime_month", str(start_date.month))
                set_value_select_box(cls.driver, "sale_stime_day", str(start_date.day))
                set_value_select_box(cls.driver, "sale_stime_hour", str(start_date.hour))
                set_value_select_box(cls.driver, "sale_stime_min", str(start_date.minute))
            if item_sales_period_entity.end_date is not None:
                end_date = datetime.datetime(item_sales_period_entity.end_date)
                set_value_select_box(cls.driver, "sale_etime_year", str(end_date.year))
                set_value_select_box(cls.driver, "sale_etime_month", str(end_date.month))
                set_value_select_box(cls.driver, "sale_etime_day", str(end_date.day))
                set_value_select_box(cls.driver, "sale_etime_hour", str(end_date.hour))
                set_value_select_box(cls.driver, "sale_etime_min", str(end_date.minute))
        except NoSuchElementException as e:
            raise CustomError("販売期間指定入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("販売期間指定入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("販売期間指定入力時に不明なエラーが出ました", e)
        return elem_select

    @classmethod
    def set_item_reception_num_type(cls, item_reception_num_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'units_type', item_reception_num_type_entity.reception_num_type.value)
            elem_radio_btn.click()

            if item_reception_num_type_entity.reception_num_type_id == 3 and \
                    item_reception_num_type_entity.reception_num is not None:
                elem_max_units = cls.driver.find_element_by_name("units")
                elem_max_units.send_keys(item_reception_num_type_entity.reception_num)
        except NoSuchElementException as e:
            raise CustomError("注文受付数入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("注文受付数入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("注文受付数入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_stock_type(cls, item_stock_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'inventory_type', item_stock_type_entity.stock_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("在庫タイプ入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("在庫タイプ入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("在庫タイプ入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_amount_stock(cls, amount_stock: int) -> WebElement:
        try:
            elem_input = cls.driver.find_element_by_name("inventory")
            if amount_stock is not None:
                elem_input.send_keys(amount_stock)
        except NoSuchElementException as e:
            raise CustomError("在庫数（通常在庫）入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("在庫数（通常在庫）入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("在庫数（通常在庫）入力時に不明なエラーが出ました", e)
        return elem_input

    @classmethod
    def set_item_stock_display_type(cls, item_stock_display_type_entity) -> WebElement:
        try:
            elem_radio_btn = get_elem_radio_btn(
                cls.driver, 'nokori', item_stock_display_type_entity.stock_display_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("在庫表示入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("在庫表示入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("在庫表示入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_setting_back_stock_flg(cls, setting_back_stock_flg: bool) -> WebElement:
        try:
            elem_check_box = cls.driver.find_element_by_name("restore_inventory_flag")
            if elem_check_box.is_selected() != setting_back_stock_flg:
                elem_check_box.click()
        except NoSuchElementException as e:
            raise CustomError("在庫戻し設定入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("在庫戻し設定入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("在庫戻し設定入力時に不明なエラーが出ました", e)
        return elem_check_box

    @classmethod
    def set_item_order_sold_out_flg(cls, order_sold_out_flg: bool) -> WebElement:
        try:
            elem_check_box = cls.driver.find_element_by_name("backorder_flag")
            if elem_check_box.is_selected() != order_sold_out_flg:
                elem_check_box.click()
        except NoSuchElementException as e:
            raise CustomError("在庫切れ時の注文入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("在庫切れ時の注文入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("在庫切れ時の注文入力時に不明なエラーが出ました", e)
        return elem_check_box

    @classmethod
    def set_item_delivery_info_display_list(cls, item_delivery_info_display_list) -> WebElement:
        try:
            elem_select = cls.driver.find_element_by_name("normal_delvdate_id")
            if len(item_delivery_info_display_list) == 0:
                return elem_select
            elif len(item_delivery_info_display_list) <= 2:
                for entity in item_delivery_info_display_list:
                    if entity.delivery_info_type_id == 1:
                        set_value_select_box(cls.driver, "normal_delvdate_id", entity.delivery_info_display.value)
                    elif entity.delivery_info_type_id == 2:
                        set_value_select_box(cls.driver, "backorder_delvdate_id", entity.delivery_info_display.value)
                    else:
                        raise CustomError("DBに登録されている納品情報区分が不明です。")
            else:
                raise CustomError("DBに登録されている納品情報表示が仕様より多く登録されています。")

        except NoSuchElementException as e:
            raise CustomError("納期情報の表示入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("納期情報の表示入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("納期情報の表示入力時に不明なエラーが出ました", e)
        return elem_select

    @classmethod
    def set_item_description_for_pc(cls, description_for_pc: str) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("catalog_caption")
            if description_for_pc is not None:
                elem_txt.send_keys(description_for_pc)
        except NoSuchElementException as e:
            raise CustomError("PC用商品説明文入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("PC用商品説明文入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("PC用商品説明文入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_description_for_mobile(cls, description_for_mobile: str) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("smart_caption")
            if description_for_mobile is not None:
                elem_txt.send_keys(description_for_mobile)
        except NoSuchElementException as e:
            raise CustomError("スマートフォン用商品説明文入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("スマートフォン用商品説明文入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("スマートフォン用商品説明文入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_description_for_pc_sale(cls, description_for_pc_sale: str) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("display_caption")
            if description_for_pc_sale is not None:
                elem_txt.send_keys(description_for_pc_sale)
        except NoSuchElementException as e:
            raise CustomError("PC用販売説明文入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("PC用販売説明文入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("PC用販売説明文入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_image_list(cls, item_image_list) -> WebElement:
        try:
            cls.driver.find_element_by_link_text("+商品画像(4)以降を表示").click()
            elem_max_txt = cls.driver.find_element_by_name("image_url20")
            if len(item_image_list) == 0:
                return elem_max_txt

            browser = Browser(cls.driver)
            index = 1
            for entitiy in sorted(item_image_list, key=lambda i_image: i_image.image_url):
                if not is_image_correct(entitiy.total_judge):
                    continue
                elem_url_txt = cls.driver.find_element_by_name("image_url" + str(index))
                elem_url_txt.send_keys(entitiy.image_url)

                if entitiy.image_alt is not None:
                    elem_alt_txt = cls.driver.find_element_by_name("image_alt" + str(index))
                    elem_alt_txt.send_keys(entitiy.image_alt)
                index += 1
                browser.scroll_by_elem_and_offset(elem_url_txt, 100)
        except NoSuchElementException as e:
            raise CustomError("商品画像入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品画像入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品画像入力時に不明なエラーが出ました", e)
        return elem_max_txt

    @classmethod
    def set_item_white_bg_image(cls, white_bg_image_list) -> WebElement:
        try:
            elem_url_txt = cls.driver.find_element_by_name("image_search_url")
            if len(white_bg_image_list) == 0:
                return elem_url_txt
            white_bg_image_entity = white_bg_image_list[0]
            if is_image_correct(white_bg_image_entity.total_judge):
                elem_url_txt.send_keys(white_bg_image_entity.image_url)
        except NoSuchElementException as e:
            raise CustomError("白背景画像入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("白背景画像入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("白背景画像入力時に不明なエラーが出ました", e)
        return elem_url_txt

    @classmethod
    def set_item_movie_url(cls, movie_url: str) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("movie_url")
            if movie_url is not None:
                elem_txt.send_keys(movie_url)
        except NoSuchElementException as e:
            raise CustomError("動画(HTMLソース）入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("動画(HTMLソース）入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("動画(HTMLソース）入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_all_item_directory_id(cls, item_all_item_directory_id_entity) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("genre_id")
            if item_all_item_directory_id_entity is not None:
                elem_txt.send_keys(item_all_item_directory_id_entity.all_item_directory_id.directory_id)
        except NoSuchElementException as e:
            raise CustomError("全商品ディレクトリID入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("全商品ディレクトリID入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("全商品ディレクトリID入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_tag_id(cls, item_tag_id_list) -> WebElement:
        return cls.driver.find_element_by_name("tag_id")

    @classmethod
    def set_item_catalog_id(cls, catalog_id_entity) -> WebElement:
        try:
            time.sleep(0.1)
            if catalog_id_entity.not_catalog_id_flg:
                radio_value = "2"
                elem_radio_btn = get_elem_radio_btn(cls.driver, "rcatalogid_type", radio_value)
                elem_radio_btn.click()
                set_value_select_box(
                    cls.driver, "catalogId_exemption_reason", catalog_id_entity.not_catalog_id_reason.value)
            else:
                radio_value = "1"
                elem_radio_btn = get_elem_radio_btn(cls.driver, "rcatalogid_type", radio_value)
                elem_radio_btn.click()
                catalog_id_txt = catalog_id_entity.value
                if catalog_id_txt is not None:
                    cls.driver.find_element_by_name("rcatalog_id").send_keys(catalog_id_txt)
        except NoSuchElementException as e:
            raise CustomError("カタログID入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("カタログID入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("カタログID入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_display_manufacturer_info_flg(cls, display_manufacturer_info_flg: bool) -> WebElement:
        try:
            elem_check_box = cls.driver.find_element_by_name("display_maker_contents")
            if elem_check_box.is_selected() != display_manufacturer_info_flg:
                elem_check_box.click()
        except NoSuchElementException as e:
            raise CustomError("メーカー提供情報表示入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("メーカー提供情報表示入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("メーカー提供情報表示入力時に不明なエラーが出ました", e)
        return elem_check_box

    @classmethod
    def set_item_display_category_list(cls, display_category_list) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("category_1")
            if len(display_category_list) == 0:
                return elem_txt
            for index, entity in enumerate(display_category_list):
                cls.driver.find_element_by_name("category_" + str(index + 1)).send_keys(entity.display_category.name)
        except NoSuchElementException as e:
            raise CustomError("表示先カテゴリ入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("表示先カテゴリ入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("表示先カテゴリ入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_shop_category_display_rank(cls, shop_category_display_rank: int) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("item_weight")
            if shop_category_display_rank is not None:
                elem_txt.send_keys(str(shop_category_display_rank))
        except NoSuchElementException as e:
            raise CustomError("店舗内カテゴリでの表示順位入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("店舗内カテゴリでの表示順位入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("店舗内カテゴリでの表示順位入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_search_not_display_flg(cls, search_not_display_flg: bool) -> WebElement:
        try:
            elem_check_box = cls.driver.find_element_by_name("limited_flag")
            if elem_check_box.is_selected() != search_not_display_flg:
                elem_check_box.click()
        except NoSuchElementException as e:
            raise CustomError("サーチ非表示入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("サーチ非表示入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("サーチ非表示入力時に不明なエラーが出ました", e)
        return elem_check_box

    @classmethod
    def set_item_black_market_password(cls, black_market_password: str) -> WebElement:
        try:
            elem_txt = cls.driver.find_element_by_name("limited_passwd")
            if black_market_password is not None:
                elem_txt.send_keys(str(black_market_password))
        except NoSuchElementException as e:
            raise CustomError("闇市パスワード入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("闇市パスワード入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("闇市パスワード入力時に不明なエラーが出ました", e)
        return elem_txt

    @classmethod
    def set_item_warehouse_type(cls, item_warehouse_type_entity) -> WebElement:
        try:
            elem_radio_btn = \
                get_elem_radio_btn(cls.driver, "depot_flag", item_warehouse_type_entity.warehouse_type.value)
            elem_radio_btn.click()
        except NoSuchElementException as e:
            raise CustomError("倉庫指定入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("倉庫指定入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("倉庫指定入力時に不明なエラーが出ました", e)
        return elem_radio_btn

    @classmethod
    def set_item_every_item_stock(cls, every_item_stock_list) -> WebElement:
        try:
            elem_h_axis = cls.driver.find_element_by_name("ha_name")
            elem_v_axis = cls.driver.find_element_by_name("va_name")
            if len(every_item_stock_list) == 0:
                return elem_h_axis
            every_item_stock_entity = every_item_stock_list[0]
            if every_item_stock_entity.h_axis_name is not None:
                elem_h_axis.send_keys(every_item_stock_entity.h_axis_name)
            if every_item_stock_entity.elem_v_axis is not None:
                elem_v_axis.send_keys(every_item_stock_entity.elem_v_axis)

            elem_radio_btn = get_elem_radio_btn(
                    cls.driver, "inventory_disp_type", every_item_stock_entity.display_threshold_type.value)
            elem_radio_btn.click()
            if every_item_stock_entity.threshold is not None and \
                    every_item_stock_entity.display_threshold_type.value == "3":
                set_value_select_box(cls.driver, "inventory_disp", every_item_stock_entity.threshold)
        except NoSuchElementException as e:
            raise CustomError("項目選択肢別在庫用入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("項目選択肢別在庫用入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("項目選択肢別在庫用入力時に不明なエラーが出ました", e)
        return elem_h_axis

    @classmethod
    def set_item_point_conversion_info(cls, item_point_conversion_info_list) -> WebElement:
        try:
            elem_select = cls.driver.find_element_by_name("point_rate")
            if len(item_point_conversion_info_list) == 0:
                return elem_select
            item_point_conversion_info_entity = item_point_conversion_info_list[0]
            set_value_select_box(
                cls.driver, "point_rate", item_point_conversion_info_entity.point_conversion_rate.value)
            if item_point_conversion_info_entity.adaptation_start_date is not None:
                start_date = datetime.datetime(item_point_conversion_info_entity.adaptation_start_date)
                set_value_select_box(cls.driver, "point_stime_year", str(start_date.year))
                set_value_select_box(cls.driver, "point_stime_month", str(start_date.month))
                set_value_select_box(cls.driver, "point_stime_day", str(start_date.day))
                set_value_select_box(cls.driver, "point_stime_hour", str(start_date.hour))

                end_date = datetime.datetime(item_point_conversion_info_entity.adaptation_end_date)
                set_value_select_box(cls.driver, "point_etime_year", str(end_date.year))
                set_value_select_box(cls.driver, "point_etime_month", str(end_date.month))
                set_value_select_box(cls.driver, "point_etime_day", str(end_date.day))
                set_value_select_box(cls.driver, "point_etime_hour", str(end_date.hour))
        except NoSuchElementException as e:
            raise CustomError("商品別ポイント変倍情報入力時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品別ポイント変倍情報入力時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品別ポイント変倍情報入力時に不明なエラーが出ました", e)
        return elem_select

    @classmethod
    def submit(cls):
        try:
            cls.driver.find_element_by_id("submitButton").click()
            try:
                wait_show_finish(cls.driver)
            except TimeoutException:
                raise TimeoutException(get_validation_message(cls.driver))
        except NoSuchElementException as e:
            raise CustomError("商品登録時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError(e)
        except Exception as e:
            raise CustomError("商品登録時に不明なエラーが出ました", e)
        return

    @classmethod
    def search_item_name(cls, item_name):
        try:
            elem_search_panel = cls.driver.find_element_by_class_name("itemListSearch-itemName")
            elem_search_box = elem_search_panel.find_element_by_id("_searchText")
            elem_search_box.send_keys(item_name)
            elem_search_panel.find_element_by_name("submit").click()
        except NoSuchElementException as e:
            raise CustomError("商品検索時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品検索時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品検索時に不明なエラーが出ました", e)
        return

    @classmethod
    def search_item_managed_number(cls, item_managed_number):
        try:
            elem_search_panel = cls.driver.find_element_by_class_name("itemListSearch-itemName")
            elem_search_panel.find_element_by_link_text("検索条件のクリア").click()

            elem_search_text_box = cls.driver.find_element_by_id("_searchText")
            elem_search_text_box.send_keys(item_managed_number)
            cls.driver.find_element_by_id("mngNumberSearchId").click()
            elem_search_panel.find_element_by_name("submit").click()
        except NoSuchElementException as e:
            raise CustomError("商品検索時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品検索時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品検索時に不明なエラーが出ました", e)
        return

    @classmethod
    def get_search_result_url_list(cls) -> List:
        try:
            url_list = []
            for elem_tr in cls.get_search_result_list():
                url_list.append(elem_tr.find_element_by_link_text("変更").get_attribute("href"))
            return url_list
        except NoSuchElementException as e:
            raise CustomError("検索結果取得時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("検索結果取得時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("検索結果取得時に不明なエラーが出ました", e)

    @classmethod
    def get_search_result_list(cls) -> List[WebElement]:
        try:
            elem_result_panel = cls.driver.find_element_by_id("tableBootstrap")
            return elem_result_panel.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        except NoSuchElementException as e:
            raise CustomError("検索結果一覧取得時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("検索結果一覧取得時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("検索結果一覧取得時に不明なエラーが出ました", e)

    @classmethod
    def add_item_style(cls, item_entity, result_url: str, client_item_choice_list):
        try:
            cls.driver.get(result_url)
            browser = Browser(cls.driver)
            browser.scroll_by_elem_and_offset(cls.driver.find_element_by_id("submitButton"), 100)
            cls.driver.find_element_by_link_text("項目選択肢の追加・変更・削除をする").click()
            for cic_entity in client_item_choice_list:
                # 項目一覧ページ
                try:
                    elem_table = cls.driver.find_element_by_xpath("/html/body/table[17]")
                    elem_tr_list = elem_table.find_elements_by_xpath("./tbody/tr/td/table/tbody/tr")
                    registed_style_list = []
                    for elem_tr in elem_tr_list:
                        registed_style_list.append(elem_tr.find_elements_by_tag_name("td")[0].text)
                    if str(cic_entity.name) in registed_style_list:
                        print("item_id: {0}, {1} is already exist".format(str(item_entity.id), cic_entity.name))
                        continue
                except NoSuchElementException:
                    print("No registed Item")
                elem_main_form = cls.driver.find_element_by_xpath("/html/body/form")
                elem_main_form.find_element_by_tag_name("table").find_element_by_tag_name("input").click()

                # 項目追加ページ
                cls.driver.find_element_by_name("choice_name").send_keys(cic_entity.name)
                get_elem_radio_btn(cls.driver, "style", cic_entity.item_choice_type.value).click()
                index_elem = 1
                for iic_entity in item_entity.item_item_choice_collection:
                    if cic_entity.id == iic_entity.client_item_choice_id:
                        cls.driver.find_element_by_name("value_" + str(index_elem)).send_keys(iic_entity.value)
                        index_elem += 1
                elem_regist_btn = cls.driver.find_element_by_xpath("descendant::input[@type='submit']")
                elem_regist_btn.click()

        except NoSuchElementException as e:
            raise CustomError("商品の色サイズ更新時に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品の色サイズ更新時にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品の色サイズ更新時に不明なエラーが出ました", e)

    @classmethod
    def is_search_last_page(cls) -> bool:
        try:
            text = cls.driver.find_element_by_class_name("pagination-info").text
            r = re.compile(r"[0-9]+")
            sum_items = r.search(text).group(0)
            return len(re.compile(sum_items).findall(text)) == 2
        except NoSuchElementException as e:
            raise CustomError("商品一覧の最終ページ判定中に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品一覧の最終ページ判定中にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品一覧の最終ページ判定中に不明なエラーが出ました", e)

    @classmethod
    def is_deleted_image_for_item_search_list(cls, elem_row: WebElement) -> bool:
        try:
            elem_img_td = elem_row.find_elements_by_tag_name("td")[2]
            try:
                elem_img = elem_img_td.find_element_by_tag_name("img")
                img = WebImage.imread_web(elem_img.get_attribute("src"))
                if img is None:
                    return True
                if img.shape[0] == 1 or img.shape[1] == 1:
                    return True
                else:
                    return False
            except NoSuchElementException:
                return True
        except NoSuchElementException as e:
            raise CustomError("商品画像の削除判定中に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品画像の削除判定中にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品画像の削除判定中に不明なエラーが出ました", e)

    @classmethod
    def delete_item(cls, elem_item: WebElement):
        try:
            elem_item.find_element_by_link_text("削除").click()
            cls.driver.find_elements_by_tag_name("form")[0].find_element_by_tag_name("input").click()
        except NoSuchElementException as e:
            raise CustomError("商品削除中に必要な要素が見つかりませんでした", e)
        except TimeoutException as e:
            raise CustomError("商品削除中にタイムアウトしました", e)
        except Exception as e:
            raise CustomError("商品削除中に不明なエラーが出ました", e)
