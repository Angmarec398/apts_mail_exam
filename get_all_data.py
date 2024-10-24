import os
import time
from typing import Union
from datetime import datetime
import requests
from dotenv import load_dotenv

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
            all_mail_id.append({
            'id_email': mail['result'][0]['ID'],
            'number': mail['result'][0]['NAME'],
            'data': mail['result'][0]['PROPERTY_107'],
            'last_modified': mail['result'][0]['PROPERTY_257']
        })
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
    print(requests.post(url=webhook_url, json=data_total).json())
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
            print(all_deal_data)
        except Exception as ex:
            print("Error in get_registry_element: ", ex)
            time.sleep(2)
            all_deal_data = requests.post(url=webhook_url, json=data).json()['result']
        for mail in all_deal_data:
            all_deal_id.append(mail['ID'])
        count += 50
    print('Собраны все сделки')
    return all_deal_id


def last_day_mail_element(need_days: str, step: int = 0) -> Union[list, TimeoutError]:
    """Функция дающая информацию об элементе в процессе 'Регистрация писем'"""
    webhook_url = BITRIX_ADMIN_7 + 'lists.element.get'
    data_total = {
        'IBLOCK_TYPE_ID': 'lists',
        'IBLOCK_ID': '29',
        'FILTER': {
            '>=DATE_CREATE': f'{need_days} 00:00:00',
            '<=DATE_CREATE': f'{need_days} 23:59:59',
        }
    }
    all_mail = requests.post(url=webhook_url, json=data_total)
    if all_mail.status_code != 200 and step < 3:
        time.sleep(2)
        return last_day_mail_element(need_days, step + 1)
    elif step > 3:
        return TimeoutError("Превышен лимит запросов")
    else:
        if len(all_mail.json()['result']) == 0:
            return []
        else:
            mail_list_to_id = []
            for mail in all_mail.json()['result']:
                last_modified = mail.get('PROPERTY_257')
                if last_modified is None:
                    now = datetime.now()
                    formatted_now = now.strftime("%d.%m.%Y %H:%M:%S")
                else:
                    formatted_now = list(last_modified.values())[0] if isinstance(last_modified, dict) else last_modified

                data = mail.get('PROPERTY_107', {})
                mail_list_to_id.append({
                    'id_email': mail.get('ID'),
                    'number': mail.get('NAME'),
                    'data': list(data.values())[0] if data else None,
                    'last_modified': formatted_now
                })
            return mail_list_to_id

def last_timestamp_mail_element(need_days: str, step: int = 0) -> Union[list, TimeoutError]:
    """Функция дающая информацию об элементе в процессе 'Регистрация писем'"""
    webhook_url = BITRIX_ADMIN_7 + 'lists.element.get'
    data_total = {
        'IBLOCK_TYPE_ID': 'lists',
        'IBLOCK_ID': '29',
        'FILTER': {
            '>=TIMESTAMP_X': f'{need_days} 00:00:00',
            '<=TIMESTAMP_X': f'{need_days} 23:59:59',
        }
    }
    all_mail = requests.post(url=webhook_url, json=data_total)
    if all_mail.status_code != 200 and step < 3:
        time.sleep(2)
        return last_day_mail_element(need_days, step + 1)
    elif step > 3:
        return TimeoutError("Превышен лимит запросов")
    else:
        if len(all_mail.json()['result']) == 0:
            return []
        else:
            mail_list_to_id = []
            for mail in all_mail.json()['result']:
                last_modified = mail.get('PROPERTY_257')
                if last_modified is None:
                    now = datetime.now()
                    formatted_now = now.strftime("%d.%m.%Y %H:%M:%S")
                else:
                    formatted_now = list(last_modified.values())[0] if isinstance(last_modified, dict) else last_modified
                data = mail.get('PROPERTY_107', {})
                mail_list_to_id.append({
                    'id_email': mail.get('ID'),
                    'number': mail.get('NAME'),
                    'data': list(data.values())[0] if data else None,
                    'last_modified': formatted_now
                })
            return mail_list_to_id

if __name__ == '__main__':
    import datetime
    days = datetime.datetime.today() - datetime.timedelta(days=1)
    day = datetime.datetime.today()
    print(f"Измененные за сегодня: {last_timestamp_mail_element(day.strftime("%d.%m.%Y"))}")
    print(f"За вчера: {last_day_mail_element(days.strftime("%d.%m.%Y"))}")
