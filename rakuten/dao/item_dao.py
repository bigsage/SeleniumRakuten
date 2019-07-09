from rakuten.dao.base.dbcore import *
from rakuten.service.base.rakuten import *
from rakuten.util.web_image import WebImage
import rakuten.util.csv
import pandas
import rakuten.util.config
import datetime


class ItemDao(DbCore):
    def __init__(self):
        super(ItemDao, self).__init__()

    @classmethod
    def create_item_list_by_color_me(cls, client_id: int, df: pandas.DataFrame):
        try:
            config = rakuten.util.config.get_csv_config()
            cls.connect()
            client = cls.session.query(cls.Client).filter(cls.Client.id == client_id).one()
            display_category_list = \
                cls.session.query(cls.DisplayCategory).filter(cls.DisplayCategory.client_id == client_id).all()

            requeslt_file_path = client.client_original_data_site_collection[0].image_judge_dir_path
            image_file_path_list = []
            for i, row in df.iterrows():
                row_item_desc = row[config["item_desc"]]
                row_sell_price = row[config["sell_price"]]
                row_item_name = row[config["item_name"]]
                row_amount_stock = row[config["amount_stock"]]
                row_category_l = row[config["category_l"]]
                row_category_s = row[config["category_s"]]
                row_item_id = row[config["item_id"]]
                row_model_num = row[config["model_num"]]
                row_img_url_list = [row[config["img_url"]]]
                if not pandas.isnull(row[config["img_other1"]]):
                    row_img_url_list.append(row[config["img_other1"]])
                if not pandas.isnull(row[config["img_other2"]]):
                    row_img_url_list.append(row[config["img_other2"]])
                if not pandas.isnull(row[config["img_other3"]]):
                    row_img_url_list.append(row[config["img_other3"]])
                if not pandas.isnull(row[config["img_other4"]]):
                    row_img_url_list.append(row[config["img_other4"]])
                if not pandas.isnull(row[config["img_other5"]]):
                    row_img_url_list.append(row[config["img_other5"]])
                if not pandas.isnull(row[config["img_other6"]]):
                    row_img_url_list.append(row[config["img_other6"]])
                if not pandas.isnull(row[config["img_other7"]]):
                    row_img_url_list.append(row[config["img_other7"]])
                if not pandas.isnull(row[config["img_other8"]]):
                    row_img_url_list.append(row[config["img_other8"]])
                if not pandas.isnull(row[config["img_other9"]]):
                    row_img_url_list.append(row[config["img_other9"]])
                print(str(row_item_id) + " is start")
                color_me_number = rakuten.util.csv.get_color_me_number(client_id, row_item_name)
                item_number = rakuten.util.csv.get_item_number(client_id, row_item_name)
                item_name = rakuten.util.csv.convert_item_name(client_id, row_item_name)
                item_desc = rakuten.util.csv.convert_item_desc(client_id, row_item_desc)
                item_price = rakuten.util.csv.get_item_price(client_id, row_sell_price)
                item = cls.Item(client_id=client_id, name=item_name, color_me_number=color_me_number,
                                item_number=item_number,
                                description_for_pc=item_desc, description_for_mobile=item_desc,
                                amount_stock=row_amount_stock, price=item_price)

                for row_img_url in row_img_url_list:
                    rakuten_file_path = WebImage.download_image(row_img_url, client.name)
                    item_image = cls.ItemImage(item_id=item.id, image_url=rakuten_file_path)
                    item.item_image_collection.append(item_image)
                    image_file_path_list.append(rakuten_file_path)
                dual_price_wording_id = rakuten.util.csv.get_dual_price_wording_id(client_id)
                dual_price_wording = cls.ItemDisplayPrice(item_id=item.id, dual_price_wording_id=dual_price_wording_id)
                item.item_display_price_collection.append(dual_price_wording)

                consump_tax_type_id = rakuten.util.csv.get_consump_tax_type_id(client_id)
                consump_tax_type = cls.ItemConsumpTaxType(item_id=item.id, consump_tax_type_id=consump_tax_type_id)
                item.item_consump_tax_type_collection.append(consump_tax_type)

                shipping_cost_type_id = rakuten.util.csv.get_shipping_cost_type_id(client_id)
                shipping_cost_type = \
                    cls.ItemShippingCostType(item_id=item.id, shipping_cost_type_id=shipping_cost_type_id)
                item.item_shipping_cost_type_collection.append(shipping_cost_type)

                cod_type_id = rakuten.util.csv.get_cod_type_id(client_id)
                cod_type = cls.ItemCodType(item_id=item.id, cod_type_id=cod_type_id)
                item.item_cod_type_collection.append(cod_type)

                noshi_type_id = rakuten.util.csv.get_noshi_type_id(client_id)
                noshi_type = cls.ItemNoshiType(item_id=item.id, noshi_type_id=noshi_type_id)
                item.item_noshi_type_collection.append(noshi_type)

                order_button_type_id = rakuten.util.csv.get_order_button_type_id(client_id)
                order_button_type = cls.ItemOrderButtonType(item_id=item.id, order_button_type_id=order_button_type_id)
                item.item_order_button_type_collection.append(order_button_type)

                document_request_type_id = rakuten.util.csv.get_document_request_type_id(client_id)
                document_request_type = \
                    cls.ItemDocumentRequestType(item_id=item.id, document_request_type_id=document_request_type_id)
                item.item_document_request_type_collection.append(document_request_type)

                inquiry_button_type_id = rakuten.util.csv.get_inquiry_button_type_id(client_id)
                inquiry_button_type = \
                    cls.ItemInquiryButtonType(item_id=item.id, inquiry_button_type_id=inquiry_button_type_id)
                item.item_inquiry_button_type_collection.append(inquiry_button_type)

                restock_button_type_id = rakuten.util.csv.get_restock_button_type_id(client_id)
                restock_button_type = \
                    cls.ItemRestockButtonType(item_id=item.id, restock_button_type_id=restock_button_type_id)
                item.item_restock_button_type_collection.append(restock_button_type)

                reception_num_type_id = rakuten.util.csv.get_reception_num_type_id(client_id)
                reception_num_type = \
                    cls.ItemReceptionNumType(item_id=item.id, reception_num_type_id=reception_num_type_id)
                item.item_reception_num_type_collection.append(reception_num_type)

                stock_type_id = rakuten.util.csv.get_stock_type_id(client_id)
                stock_type = cls.ItemStockType(item_id=item.id, stock_type_id=stock_type_id)
                item.item_stock_type_collection.append(stock_type)

                stock_display_type_id = rakuten.util.csv.get_stock_display_type_id(client_id)
                stock_display_type = \
                    cls.ItemStockDisplayType(item_id=item.id, stock_display_type_id=stock_display_type_id)
                item.item_stock_display_type_collection.append(stock_display_type)

                # FIXME 在庫有無による納品情報を追加する
                delivery_info_display_id = rakuten.util.csv.get_delivery_info_display_id(client_id)
                delivery_info_type_stock_id = rakuten.util.csv.get_delivery_info_type_id_for_stock()
                delivery_info_type_not_stock_id = rakuten.util.csv.get_delivery_info_type_id_for_not_stock()

                all_item_directory_id_id = rakuten.util.csv.get_all_item_directory_id_id(client_id, row_category_l)
                all_item_directory_id = \
                    cls.ItemAllItemDirectoryId(item_id=item.id, all_item_directory_id_id=all_item_directory_id_id)
                item.item_all_item_directory_id_collection.append(all_item_directory_id)

                # FIXME 商品タグ追加するときにはマスタ追加後

                not_catalog_id_reason_id = rakuten.util.csv.get_not_catalog_id_reason_id(client_id)
                catalog_id = \
                    cls.CatalogId(item_id=item.id, not_catalog_id_reason_id=not_catalog_id_reason_id,
                                  not_catalog_id_flg=rakuten.util.csv.get_not_catalog_id_flg(not_catalog_id_reason_id))
                item.catalog_id_collection.append(catalog_id)

                display_category_id = \
                    rakuten.util.csv.get_display_category_id(client_id, display_category_list, row_category_l)
                display_category = cls.ItemDisplayCategory(item_id=item.id, display_category_id=display_category_id)
                item.item_display_category_collection.append(display_category)

                warehouse_type_id = rakuten.util.csv.get_warehouse_type_id(client_id)
                warehouse_type = cls.ItemWarehouseType(item_id=item.id, warehouse_type_id=warehouse_type_id)
                item.item_warehouse_type_collection.append(warehouse_type)

                item_color_choice_list = rakuten.util.csv.get_item_color_choice_list(client_id, item_desc)
                if item_color_choice_list is not None:
                    color_client_item_choice_id = rakuten.util.csv.get_item_color_client_item_choice_id(client_id)
                    for each_color in item_color_choice_list:
                        item_color_choice = cls.ItemItemChoice(client_item_choice_id=color_client_item_choice_id,
                                                               item_id=item.id, value=each_color)
                        item.item_item_choice_collection.append(item_color_choice)

                item_size_choice_list = rakuten.util.csv.get_item_size_choice_list(client_id, item_desc)
                if item_size_choice_list is not None:
                    size_client_item_choice_id = rakuten.util.csv.get_item_size_client_item_choice_id(client_id)
                    for each_size in item_size_choice_list:
                        item_color_choice = cls.ItemItemChoice(client_item_choice_id=size_client_item_choice_id,
                                                               item_id=item.id, value=each_size)
                        item.item_item_choice_collection.append(item_color_choice)

                ret = cls.session.add(item)
            cls.flush()
            cls.commit()

            print("リクエストCSV作成開始")
            rakuten.util.csv.create_request_csv(requeslt_file_path, image_file_path_list)
            print("リクエストCSV作成終了")
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

    @classmethod
    def get_item_list(cls, client_id: int):
        try:
            cls.connect()
            # 削除フラグの判定は　==　でないとデータが取れない
            item_list = \
                cls.session.query(cls.Item).filter(
                    cls.Item.client_id == client_id,
                    cls.Item.regist_flg == False,
                    cls.Item.style_update_flg == False).options(
                    eagerload_all("item_image_collection"),
                    eagerload_all("white_bg_image_collection"),
                    eagerload_all("item_display_price_collection.dual_price_wording"),
                    eagerload_all("item_consump_tax_type_collection.consump_tax_type"),
                    eagerload_all("item_cod_type_collection.cod_type"),
                    eagerload_all("item_shipping_cost_type_collection.shipping_cost_type"),
                    eagerload_all("item_noshi_type_collection.noshi_type"),
                    eagerload_all("item_order_button_type_collection.order_button_type"),
                    eagerload_all("item_document_request_type_collection.document_request_type"),
                    eagerload_all("item_inquiry_button_type_collection.inquiry_button_type"),
                    eagerload_all("item_restock_button_type_collection.restock_button_type"),
                    eagerload_all("item_sales_period_collection"),
                    eagerload_all("item_reception_num_type_collection.reception_num_type"),
                    eagerload_all("item_stock_type_collection.stock_type"),
                    eagerload_all("item_stock_display_type_collection.stock_display_type"),
                    eagerload_all("item_delivery_info_display_collection.delivery_info_display"),
                    eagerload_all("item_delivery_info_display_collection.delivery_info_type"),
                    eagerload_all("item_all_item_directory_id_collection.all_item_directory_id"),
                    eagerload_all("item_tag_id_collection.tag_id"),
                    eagerload_all("catalog_id_collection.not_catalog_id_reason"),
                    eagerload_all("item_display_category_collection.display_category"),
                    eagerload_all("item_warehouse_type_collection.warehouse_type"),
                    eagerload_all("every_item_stock_collection.display_threshold_type"),
                    eagerload_all("item_point_conversion_info_collection.point_conversion_rate")).order_by(
                    cls.Item.id).all()
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()
            return item_list

    @classmethod
    def get_item_no_style_list(cls, client_id: int):
        try:
            cls.connect()
            # 削除フラグの判定は　==　でないとデータが取れない
            item_list = \
                cls.session.query(cls.Item).filter(
                    cls.Item.client_id == client_id,
                    cls.Item.regist_flg == True, cls.Item.style_update_flg == False).options(
                    eagerload_all("item_item_choice_collection.client_item_choice.item_choice_type")).order_by(
                    cls.Item.id).all()
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()
            return item_list

    @classmethod
    def update_registed_item(cls, item_list):
        try:
            cls.connect()
            update_date = datetime.datetime.now()
            for each_item in item_list:
                item = cls.session.query(cls.Item).filter(cls.Item.id == each_item.id).one()
                item.regist_flg = True
                item.update_date = update_date
                cls.session.add(item)
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

    @classmethod
    def update_registed_style_item(cls, item_list):
        try:
            cls.connect()
            update_date = datetime.datetime.now()
            for each_item in item_list:
                item = cls.session.query(cls.Item).filter(cls.Item.id == each_item.id).one()
                item.style_update_flg = True
                item.update_date = update_date
                cls.session.add(item)
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()
