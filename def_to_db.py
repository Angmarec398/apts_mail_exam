from datetime import datetime
import pandas as pd
from model import Email, Deal, session
from get_all_data import get_all_deal


def add_emails_from_excel(file_path):
    """изначальная точка для БД email"""
    df = pd.read_excel(file_path, engine='openpyxl')
    now = datetime.now()
    formatted_now = now.strftime("%d.%m.%Y %H:%M:%S")
    for index, row in df.iterrows():
        id_email = int(row.iloc[0]) if pd.notna(row.iloc[0]) else 0
        number = row.iloc[1]
        data = row.iloc[2]
        recent_changes_data = row.iloc[3] if pd.notna(row.iloc[3]) else formatted_now

        new_email = Email(
            id_email=id_email,
            number=number,
            data=data,
            recent_changes_data=recent_changes_data
        )
        session.add(new_email)
    session.commit()
    session.close()


def add_id_deal():
    """для записи в бд deal"""
    for id_deal in get_all_deal():
        new_deal = Deal(
            id_deal=id_deal
        )
        session.add(new_deal)
    session.commit()
    session.close()

def add_id_deals(test_deals):
    """функция для теста"""
    for id_deal in test_deals:
        new_deal = Deal(
            id_deal=id_deal
        )
        session.add(new_deal)
    session.commit()
    session.close()


def get_all_id_deal_db() -> list:
    """Функция дающая информацию об элементе из таблицы Deal в БД"""
    all_deals = session.query(Deal.id_deal).all()
    session.close()
    all_deal_id = [deal[0] for deal in all_deals]
    print('Собраны все сделки из БД')
    print(all_deal_id)
    return all_deal_id


def get_all_id_imail_db() -> list:
    """Функция дающая информацию об элементе из таблицы Email в БД"""
    all_mail_ids = session.query(Email.id_email).all()
    session.close()
    all_mail_id = [mail_id[0] for mail_id in all_mail_ids]  # Извлечение первого элемента из каждого кортежа
    print('Собраны все письма из БД')
    return all_mail_id


# if __name__ == '__main__':
    # add_emails_from_excel('C:/Users/Egor_yrm/Downloads/list_t.xls.xlsx')
    # add_id_deal()
    # get_all_deal_db()
    # get_all_id_imail_db()
    # pass