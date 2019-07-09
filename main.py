import rakuten.service.kkoichan
import rakuten.service.client
import rakuten.service.kkoichan


def main():
    #rakuten.service.kkoichan.Kkoichan.update_rms_pass("")
    # rakuten.service.client.ClientService.create(client_name, rms_id, rms_pass, mail_address, password, site_id)
    # 指定ファイルを抽出して保存
    rakuten.service.kkoichan.Kkoichan.convert("(390[1-9]|39[1-9][0-9]|4000)")
    # 楽天からのチェック結果を反映
    rakuten.service.kkoichan.Kkoichan.update_item_image()

    rakuten.service.kkoichan.Kkoichan.input()

    rakuten.service.kkoichan.Kkoichan.add_browser_item_style()
    # 画像が削除されている商品を抽出
    rakuten.service.kkoichan.Kkoichan.check_item_of_no_image()
    rakuten.service.kkoichan.Kkoichan.delete_item_of_no_image()


if __name__ == '__main__':
    main()

