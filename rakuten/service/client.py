from rakuten.dao.client_dao import ClientDao


class ClientService:

    @classmethod
    def create(
            cls, name: str, rms_id: str, rms_pass: str, mail_address: str, password: str, original_data_site_id: int):
        try:
            ClientDao.create_client(name, rms_id, rms_pass, mail_address, password, original_data_site_id)
        except Exception as e:
            print(e)

