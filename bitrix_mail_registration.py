import requests
import time

from def_to_db import get_all_id_deal_db, get_all_id_imail_db
from get_all_data import get_all_registry_element, get_all_deal, last_day_mail_element
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
BITRIX_ADMIN_7 = os.getenv("BITRIX_ADMIN_7")
ID_ALL_DEAL = get_all_id_deal_db()
ALL_MAIL_ID = get_all_id_imail_db()


def clear_id_list(all_id: list):
    """Функция удаляющая 0 и None из списка"""
    try:
        all_id.remove(0)
    except:
        pass
    try:
        all_id.remove('0')
    except:
        pass
    try:
        all_id.remove('None')
    except:
        pass
    try:
        all_id.remove(None)
    except:
        pass
    try:
        if len(all_id) == 0:
            pass
        else:
            return all_id
    except:
        return all_id


def get_registry_element(id_element: int or str):
    try:
        """Функция дающая информацию об элементе в процессе 'Регистрация писем'"""
        webhook_url = BITRIX_ADMIN_7 + 'lists.element.get'
        data = {'IBLOCK_TYPE_ID': 'lists',
                'IBLOCK_ID': '29',
                'ELEMENT_ID': id_element
                }
        response = requests.post(url=webhook_url, json=data).json()
        return response
    except Exception as ex:
        print("Error in get_registry_element: ", ex)
        time.sleep(1)
        get_registry_element(id_element)


def element_to_dict(id_element: int or str):
    # try:
    """Функция превращающая элемент списка 'Регистрация писем' из json файла в словарь"""
    old_data = get_registry_element(id_element=id_element)['result'][0]
    name_element = old_data['NAME']
    try:
        data_element = old_data['PROPERTY_107']
    except:
        data_element = '01.01.2000'
    type_element = old_data['PROPERTY_225']
    name_company = old_data['PROPERTY_115']
    try:
        responsible_employee = old_data['PROPERTY_113']
    except:
        responsible_employee = {'42149': '1'}
    try:
        mail_theme = old_data['PROPERTY_249']
    except:
        mail_theme = None
    try:
        add_to = old_data['PROPERTY_109']
    except:
        add_to = None
    try:
        from_to = old_data['PROPERTY_111']
    except:
        from_to = None
    try:
        mail_add_to = old_data['PROPERTY_117']
    except:
        mail_add_to = None
    try:
        mail_from_to = old_data['PROPERTY_137']
    except:
        mail_from_to = None
    try:
        number_other_organization = old_data['PROPERTY_229']
    except:
        number_other_organization = None
    try:
        where = old_data['PROPERTY_237']
    except:
        where = None
    try:
        executor_other_organization = old_data['PROPERTY_227']
    except:
        executor_other_organization = None

    try:
        other_text = old_data['PROPERTY_119']
    except:
        other_text = None

    try:
        chain_deal = old_data['PROPERTY_121']
    except:
        chain_deal = None
    try:
        chain_element = old_data['PROPERTY_123']
    except:
        chain_element = {'n0': None}
    try:
        file = old_data['PROPERTY_125']
    except:
        file = None
    dict_element = {
        'name_element': name_element,
        'data_element': data_element,
        'type_element': type_element,
        'name_company': name_company,
        'add_to': add_to,
        'from_to': from_to,
        'responsible_employee': responsible_employee,
        'mail_add_to': mail_add_to,
        'mail_from_to': mail_from_to,
        'number_other_organization': number_other_organization,
        'where': where,
        'mail_theme': mail_theme,
        'executor_other_organization': executor_other_organization,
        'other_text': other_text,
        'chain_deal': chain_deal,
        'chain_element': chain_element,
        'file': file
    }
    return dict_element
    # except Exception as ex:
    #     print('Error in element_to_dict:', ex, id_element)
    #     time.sleep(1)
    #     element_to_dict(int(id_element))


def update_registry_element(id_element: int or str, new_element=None, new_deal=None):
    try:
        """Функция обновляющая элемент списка 'Регистрация писем'.
         Дополнительная возможность привязать новые данные о связанных сделках и связанных элементах в текущую запись"""
        webhook_url = BITRIX_ADMIN_7 + 'lists.element.update'
        old_data = element_to_dict(id_element=id_element)
        try:
            chain_element_old_data = old_data['chain_element']
            if new_element is None:
                chain_element = chain_element_old_data
            else:
                try:
                    if list(chain_element_old_data.values())[0] is None:
                        chain_element = {'n0': new_element}
                    else:
                        chain_element = {**{'n0': new_element}, **chain_element_old_data}
                except:
                    chain_element = {'n0': new_element}
        except:
            chain_element = None
        try:
            deal_old_data = old_data['chain_deal']
            if new_deal is None:
                chain_deal = connect_type_tag(clear_dict_deal(deal_old_data))
            else:
                try:
                    if list(deal_old_data.values())[0] is None:
                        chain_deal = connect_type_tag(clear_dict_deal({'n0': new_deal}))
                    else:
                        chain_deal = connect_type_tag(clear_dict_deal({**{'n0': new_deal}, **deal_old_data}))
                except:
                    chain_deal = connect_type_tag(clear_dict_deal({'n0': new_deal}))
        except:
            chain_deal = None
        # chain_deal = new_deal
        # chain_element = new_element
        data = {
            'IBLOCK_TYPE_ID': 'lists',
            'IBLOCK_ID': '29',
            'ELEMENT_ID': id_element,
            'FIELDS': {'NAME': old_data['name_element'],
                       'PROPERTY_107': old_data['data_element'],
                       'PROPERTY_109': old_data['add_to'],
                       'PROPERTY_111': old_data['from_to'],
                       'PROPERTY_113': old_data['responsible_employee'],
                       'PROPERTY_115': old_data['name_company'],
                       'PROPERTY_117': old_data['mail_add_to'],
                       'PROPERTY_119': old_data['other_text'],
                       'PROPERTY_121': chain_deal,
                       'PROPERTY_123': chain_element,
                       'PROPERTY_125': old_data['file'],
                       'PROPERTY_137': old_data['mail_from_to'],
                       'PROPERTY_225': old_data['type_element'],
                       'PROPERTY_227': old_data['executor_other_organization'],
                       'PROPERTY_229': old_data['number_other_organization'],
                       'PROPERTY_237': old_data['where'],
                       'PROPERTY_249': old_data['mail_theme']
                       }
        }
        return requests.post(url=webhook_url, json=data).json()
    except Exception as ex:
        print('Error in update_registry_element:', ex, id_element)
        time.sleep(1)
        update_registry_element(int(id_element), new_deal, new_element)


def mirror_chain_element(id_element: int or str or list):
    """Функция возвращающая id связанных элементов текущей записи"""
    try:
        if type(id_element) == int or type(id_element) == str:
            chain_element = element_to_dict(id_element=id_element)['chain_element']
            result = list(chain_element.values())
            return result
        elif type(id_element) == list:
            for one_element in id_element:
                mirror_chain_element(id_element=one_element)
        else:
            return []
    except:
        return []


def search_mirror_element(id_element: int or str):
    """Функция, которая находит вся связанные элементы"""
    all_list_element = clear_id_list(mirror_chain_element(id_element=int(id_element)))
    exam_list_element = []
    if all_list_element is not None:
        if len(all_list_element) > 0:
            for unit_element in all_list_element:
                if type(unit_element) is list:
                    for one_element in unit_element:
                        if one_element in exam_list_element:
                            pass
                        else:
                            if one_element in ALL_MAIL_ID:
                                exam_list_element.append(one_element)
                elif type(unit_element) is str or type(unit_element) is int:
                    if unit_element in exam_list_element:
                        pass
                    else:
                        if unit_element in ALL_MAIL_ID:
                            exam_list_element.append(unit_element)
                            prepare_element = clear_id_list(mirror_chain_element(unit_element))
                            if prepare_element is not None:
                                if type(prepare_element) is list:
                                    for unit_prepare_element in prepare_element:
                                        if unit_prepare_element in ALL_MAIL_ID:
                                            all_list_element.append(prepare_element)
                                else:
                                    if prepare_element in ALL_MAIL_ID:
                                        all_list_element.append(prepare_element)
                else:
                    print('search_mirror_element', ' Неизвестный тип элемента')
            return exam_list_element
        else:
            pass
    else:
        return []


def unpack_list(list_element: list):
    """Функция распаковывающая списки. Превращает список вложенный в список и т.д. в один единый список"""
    finish_list = list()
    for element in list_element:
        if type(element) is list:
            try:
                finish_list += element
            except:
                finish_list.append(unpack_list(element))
        else:
            finish_list.append(element)
    return finish_list


def deal_in_element(id_element):
    """Функция возвращающая ID сделок по ID элемента"""
    try:
        deal_info = clear_id_list(list(element_to_dict(id_element=id_element)['chain_deal'].values()))
    except AttributeError:
        deal_info = None
    return deal_info


def chain_deal(start_list: list):
    """Функция запускающая процесс поиска и добавления связанных элементов в основной элемент"""
    all_deal_id = list()
    for element in start_list:
        deal_info = deal_in_element(id_element=element)
        if deal_info is None:
            pass
        else:
            if type(deal_info) is list:
                for deal_info_element in deal_info:
                    if str(deal_info_element).lstrip('D_') in ID_ALL_DEAL:
                        all_deal_id.append(deal_info_element)
            else:
                if str(deal_info).lstrip('D_') in ID_ALL_DEAL:
                    all_deal_id.append(deal_info)
    if clear_id_list(all_deal_id) is None:
        return None
    else:
        all_deal_id = list(set(unpack_list(all_deal_id)))
        return all_deal_id


def start_mirror_element(id_element: int):
    """Функция запускающая процесс поиска и добавления связанных элементов в основной элемент"""
    start_list = search_mirror_element(id_element=int(id_element))
    print(start_list)
    all_chain_deal = chain_deal(start_list=start_list)
    print(all_chain_deal)
    clear_start_list = start_list.copy()
    try:
        clear_start_list.remove(str(id_element))
    except:
        pass
    update_registry_element(id_element=id_element, new_element=clear_start_list, new_deal=all_chain_deal)
    for mirror_element in clear_start_list:
        mirror_list = start_list.copy()
        mirror_list.remove(mirror_element)
        mirror_list.append(id_element)
        update_registry_element(id_element=int(mirror_element),
                                new_element=mirror_list, new_deal=all_chain_deal)


def clear_dict_deal(dict_deal: dict):
    """Функция убирающая дубли сделок"""
    old_all_deal = list(dict_deal.values())
    new_all_deal = list()
    for id_old_deal in old_all_deal:
        if type(id_old_deal) is str or type(id_old_deal) is int:
            if id_old_deal in new_all_deal:
                pass
            else:
                new_all_deal.append(id_old_deal)
        elif type(id_old_deal) is list:
            for point_id_deal in id_old_deal:
                if point_id_deal in new_all_deal:
                    pass
                else:
                    new_all_deal.append(point_id_deal)
        elif type(id_old_deal) is dict:
            id_old_deal_values = list(id_old_deal.values())
            for old_deal_values in id_old_deal_values:
                if old_deal_values in new_all_deal:
                    pass
                else:
                    new_all_deal.append(old_deal_values)
            pass
        else:
            print('Неизвестный тип данных')
    return new_all_deal


def connect_type_tag(new_all_deal: list, tags: str = 'D_'):
    """Функция добавляющая тэг сущности к ID сделки"""
    new_deal_tags = list()
    for id_new_deal in new_all_deal:
        if id_new_deal[:2] != tags:
            new_deal_tags.append(tags + id_new_deal)
        else:
            new_deal_tags.append(id_new_deal)
    if len(new_deal_tags) == 1:
        return {'n0': new_deal_tags[0]}
    else:
        return {'n0': new_deal_tags}


def main():
    number_weekday = datetime.datetime.today().isoweekday()
    days = datetime.datetime.today() - datetime.timedelta(days=1)
    if number_weekday != 0:
        for element in last_day_mail_element(need_days=days.strftime("%d.%m.%Y")):
            time.sleep(3)
            start_mirror_element(id_element=element)
    else:
        for element in ALL_MAIL_ID:
            time.sleep(3)
            start_mirror_element(id_element=element)


if __name__ == '__main__':
    main()
