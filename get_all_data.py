import requests
import time
from dotenv import load_dotenv
import os


load_dotenv()
BITRIX_ADMIN_7 = os.getenv("BITRIX_ADMIN_7")


def get_all_registry_element() -> list:
    """Функция дающая информацию об элементе в процессе 'Регистрация писем'"""
    webhook_url = BITRIX_ADMIN_7 + 'lists.element.get'
    count = 0
    data_total = {
        'IBLOCK_TYPE_ID': 'lists',
        'IBLOCK_ID': '29',
        'start': count,
    }
    total = requests.post(url=webhook_url, json=data_total).json()['total']
    all_mail_id = []
    while count < total:
        print(f'{count} / {total}')
        time.sleep(1)
        data = {
            'IBLOCK_TYPE_ID': 'lists',
            'IBLOCK_ID': '29',
            'start': count,
        }
        try:
            all_mail_data = requests.post(url=webhook_url, json=data).json()['result']
        except Exception as ex:
            print("Error in get_registry_element: ", ex)
            time.sleep(2)
            all_mail_data = requests.post(url=webhook_url, json=data).json()['result']
        for mail in all_mail_data:
            all_mail_id.append(mail['ID'])
        count += 50
    print('Собраны все письма')
    return all_mail_id


def get_all_deal() -> list:
    """Функция дающая информацию об элементе в процессе 'Регистрация писем'"""
    webhook_url = BITRIX_ADMIN_7 + 'crm.deal.list'
    count = 0
    data_total = {
        'start': count,
    }
    total = requests.post(url=webhook_url, json=data_total).json()['total']
    all_deal_id = []
    while count < total:
        print(f'{count} / {total}')
        time.sleep(1)
        data = {
            'start': count,
            'select': ['ID']
        }
        try:
            all_deal_data = requests.post(url=webhook_url, json=data).json()['result']
        except Exception as ex:
            print("Error in get_registry_element: ", ex)
            time.sleep(2)
            all_deal_data = requests.post(url=webhook_url, json=data).json()['result']
        for mail in all_deal_data:
            all_deal_id.append(mail['ID'])
        count += 50
    print('Собраны все сделки')
    return all_deal_id


if __name__ == '__main__':
    pass
