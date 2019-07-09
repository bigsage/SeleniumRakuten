from rakuten.util.encrypt import Encrypt
from rakuten.dao.base.dbcore import *
from rakuten.service.base.rakuten import *
from sqlalchemy.inspection import inspect


class ClientDao(DbCore):
    def __init__(self):
        super(ClientDao, self).__init__()

    @classmethod
    def create_client(
            cls, name: str, rms_id: str, rms_pass: str, mail_address: str, password: str, original_data_site_id: int):
        try:
            cls.connect()
            print(cls.Client)
            mapper = inspect(cls.Client)
            for prop in mapper.iterate_properties:
                print("\t", prop.key, type(prop))
            result = cls.session.query(cls.Client).filter_by(mail_address=mail_address).first()
            if result is not None:
                cls.session.close()
                print("すでにこのクライアントは追加されています")
                return None

            new_client = cls.Client(name=name, rms_id=rms_id, rms_pass=Encrypt.encrypt(rms_pass),
                                    mail_address=mail_address, password=Encrypt.encrypt(password))
            new_client_ods = cls.ClientOriginalDataSite(
                client_id=new_client.id, original_data_site_id=original_data_site_id)
            new_client.client_original_data_site_collection.append(new_client_ods)
            ret = cls.session.add(new_client)
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

    @classmethod
    def get_client(cls, client_id):
        try:
            cls.connect()
            result = cls.session.query(cls.Client).filter_by(id=client_id).one()
            result.client_original_data_site_collection
            return result
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

    @classmethod
    def update_rms_pass(cls, client_id, rms_pass: str):
        try:
            cls.connect()
            client = cls.session.query(cls.Client).filter_by(id=client_id).one()
            client.rms_pass = Encrypt.encrypt(rms_pass)
            client.update_date = datetime.datetime.today()
            cls.flush()
            cls.commit()
        except Exception as e:
            raise CustomError(e)
        finally:
            cls.close()

