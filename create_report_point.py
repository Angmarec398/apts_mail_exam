import os
import time
from datetime import datetime
import requests
from dotenv import load_dotenv
from model import Deal, session, Email
load_dotenv()
BITRIX_ADMIN_7 = os.getenv("BITRIX_ADMIN_7")# Этот файл запускается при создании контейнера, точка отчета.

def get_all_registry_element() -> list:
    """Функция собирает все нужные значения для БД с 'Регистрация писем'"""
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
            # Получаем last_modified или используем текущее время, если его нет
            last_modified = mail.get('PROPERTY_257')
            if last_modified is None:
                now = datetime.now()
                formatted_now = now.strftime("%d.%m.%Y %H:%M:%S")
            else:
                formatted_now = list(last_modified.values())[0] if isinstance(last_modified, dict) else last_modified

            data = mail.get('PROPERTY_107', {})
            all_mail_id.append({
                'id_email': mail.get('ID'),
                'number': mail.get('NAME'),
                'data': list(data.values())[0] if data else None,
                'last_modified': formatted_now
            })
        count += 50
    print('Собраны все письма')
    return all_mail_id


def get_all_deal() -> list:
    """Функция собирает все нужные значения для БД с 'Сделки'"""
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


def add_all_emails_to_db():
    """Функция для добавления всех найденных писем в БД, таблица  - Email."""
    # Стираем все записи из таблицы Email
    session.query(Email).delete()
    session.commit()
    # Получаем все письма
    all_emails = get_all_registry_element()
    for email in all_emails:
        # Создаем новую запись
        new_email = Email(
            id_email=email['id_email'],
            number=email['number'],
            data=email['data'],
            recent_changes_data=email['last_modified']
        )
        # Добавляем и сохраняем в базе данных
        session.add(new_email)
    session.commit()
    print('Все письма добавлены в базу данных.')

def add_id_deal():
    """Функция для записи в БД, таблица - Deal"""
    session.query(Deal).delete()
    session.commit()
    for id_deal in get_all_deal():
        new_deal = Deal(
            id_deal=id_deal
        )
        session.add(new_deal)
    session.commit()
    session.close()

if __name__ == '__main__':
    start_time = time.time()
    add_id_deal()
    add_all_emails_to_db()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Точка отчета успешно прошла")
    print(f"Время выполнения: {elapsed_time:.2f} секунд")