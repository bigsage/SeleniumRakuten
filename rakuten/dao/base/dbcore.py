from sqlalchemy import create_engine
from sqlalchemy.orm import *
from sqlalchemy.ext.automap import automap_base


class DbCore:
    Base = None
    engine = None
    session = None
    Item = None
    Client = None
    ClientOriginalDataSite = None
    OriginalDataSite = None
    ItemImage = None
    WhiteBgImage = None
    DualPriceWording = None
    ItemDisplayPrice = None
    ConsumpTaxType = None
    ItemConsumpTaxType = None
    ShippingCostType = None
    ItemShippingCostType = None
    CodType = None
    ItemCodType = None
    NoshiType = None
    ItemNoshiType = None
    OrderButtonType = None
    ItemOrderButtonType = None
    DocumentRequestType = None
    ItemDocumentRequestType = None
    InquiryButtonType = None
    ItemInquiryButtonType = None
    RestockButtonType = None
    ItemRestockButtonType = None
    ItemSalesPeriod = None
    ReceptionNumType = None
    ItemReceptionNumType = None
    StockType = None
    ItemStockType = None
    StockDisplayType = None
    ItemStockDisplayType = None
    DeliveryInfoDisplay = None
    DeliveryInfoType = None
    ItemDeliveryInfoDisplay = None
    AllItemDirectoryId = None
    ItemAllItemDirectoryId = None
    TagId = None
    ItemTagId = None
    NotCatalogIdReason = None
    CatalogId = None
    DisplayCategory = None
    ItemDisplayCategory = None
    WarehouseType = None
    ItemWarehouseType = None
    DisplayThresholdType = None
    EveryItemStock = None
    PointConversionRate = None
    ItemPointConversionInfo = None
    ItemItemChoice = None
    ItemChoiceType = None
    ClientItemChoice = None
    DeleteItemManagement = None

    @classmethod
    def connect(cls):
        cls.Base = automap_base()
        cls.engine = create_engine("postgresql://postgres:@localhost:5432/selenium_rakuten")
        cls.Base.prepare(cls.engine, reflect=True)
        cls.session = create_session(bind=cls.engine, autocommit=False, autoflush=False)
        cls.Item = cls.Base.classes.item
        cls.Client = cls.Base.classes.client
        cls.ClientOriginalDataSite = cls.Base.classes.client_original_data_site
        cls.OriginalDataSite = cls.Base.classes.original_data_site
        cls.ItemImage = cls.Base.classes.item_image
        cls.WhiteBgImage = cls.Base.classes.white_bg_image
        cls.DualPriceWording = cls.Base.classes.dual_price_wording
        cls.ItemDisplayPrice = cls.Base.classes.item_display_price
        cls.ConsumpTaxType = cls.Base.classes.consump_tax_type
        cls.ItemConsumpTaxType = cls.Base.classes.item_consump_tax_type
        cls.ShippingCostType = cls.Base.classes.shipping_cost_type
        cls.ItemShippingCostType = cls.Base.classes.item_shipping_cost_type
        cls.CodType = cls.Base.classes.cod_type
        cls.ItemCodType = cls.Base.classes.item_cod_type
        cls.NoshiType = cls.Base.classes.noshi_type
        cls.ItemNoshiType = cls.Base.classes.item_noshi_type
        cls.OrderButtonType = cls.Base.classes.order_button_type
        cls.ItemOrderButtonType = cls.Base.classes.item_order_button_type
        cls.DocumentRequestType = cls.Base.classes.document_request_type
        cls.ItemDocumentRequestType = cls.Base.classes.item_document_request_type
        cls.InquiryButtonType = cls.Base.classes.inquiry_button_type
        cls.ItemInquiryButtonType = cls.Base.classes.item_inquiry_button_type
        cls.RestockButtonType = cls.Base.classes.restock_button_type
        cls.ItemRestockButtonType = cls.Base.classes.item_restock_button_type
        cls.ItemSalesPeriod = cls.Base.classes.item_sales_period
        cls.ReceptionNumType = cls.Base.classes.reception_num_type
        cls.ItemReceptionNumType = cls.Base.classes.item_reception_num_type
        cls.StockType = cls.Base.classes.stock_type
        cls.ItemStockType = cls.Base.classes.item_stock_type
        cls.StockDisplayType = cls.Base.classes.stock_display_type
        cls.ItemStockDisplayType = cls.Base.classes.item_stock_display_type
        cls.DeliveryInfoDisplay = cls.Base.classes.delivery_info_display
        cls.DeliveryInfoType = cls.Base.classes.delivery_info_type
        cls.ItemDeliveryInfoDisplay = cls.Base.classes.item_delivery_info_display
        cls.AllItemDirectoryId = cls.Base.classes.item_all_item_directory_id
        cls.ItemAllItemDirectoryId = cls.Base.classes.item_all_item_directory_id
        cls.TagId = cls.Base.classes.tag_id
        cls.ItemTagId = cls.Base.classes.item_tag_id
        cls.NotCatalogIdReason = cls.Base.classes.not_catalog_id_reason
        cls.CatalogId = cls.Base.classes.catalog_id
        cls.DisplayCategory = cls.Base.classes.display_category
        cls.ItemDisplayCategory = cls.Base.classes.item_display_category
        cls.WarehouseType = cls.Base.classes.warehouse_type
        cls.ItemWarehouseType = cls.Base.classes.item_warehouse_type
        cls.DisplayThresholdType = cls.Base.classes.display_threshold_type
        cls.EveryItemStock = cls.Base.classes.every_item_stock
        cls.PointConversionRate = cls.Base.classes.point_conversion_rate
        cls.ItemPointConversionInfo = cls.Base.classes.item_point_conversion_info
        cls.ItemItemChoice = cls.Base.classes.item_item_choice
        cls.ItemChoiceType = cls.Base.classes.item_choice_type
        cls.ClientItemChoice = cls.Base.classes.client_item_choice
        cls.DeleteItemManagement = cls.Base.classes.delete_item_management

    @classmethod
    def close(cls):
        cls.session.close()

    @classmethod
    def flush(cls):
        cls.session.flush()

    @classmethod
    def commit(cls):
        cls.session.commit()

    @classmethod
    def rollback(cls):
        cls.session.rollback()

