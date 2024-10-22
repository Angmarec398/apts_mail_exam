from model import Email, Deal, session


def get_all_id_deal_db() -> list:
    """Функция дающая информацию об элементе из таблицы Deal в БД"""
    all_deals = session.query(Deal.id_deal).all()
    session.close()
    all_deal_id = [deal[0] for deal in all_deals]
    print('Собраны все сделки из БД')
    # print(all_deal_id)
    return all_deal_id


def get_all_id_imail_db() -> list:
    """Функция дающая информацию об элементе из таблицы Email в БД"""
    all_mail_ids = session.query(Email.id_email).all()
    session.close()
    all_mail_id = [mail_id[0] for mail_id in all_mail_ids]  # Извлечение первого элемента из каждого кортежа
    print('Собраны все письма из БД')
    # print(all_mail_id)
    return all_mail_id


def add_id_deals(test_deals):
    """функция для теста"""
    for id_deal in test_deals:
        new_deal = Deal(
            id_deal=id_deal
        )
        session.add(new_deal)
    session.commit()
    session.close()
