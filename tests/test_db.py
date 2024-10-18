import pytest

from def_to_db import add_id_deal, get_all_id_deal_db, add_id_deals


@pytest.mark.usefixtures("create_db")
@pytest.mark.parametrize("test_deals", [[1, 3, 4, 5, 6, 7]])  # Используем список вместо кортежей
def test_add_id_deal(test_deals):
    add_id_deals(test_deals)  # Передаем список напрямую
    all_deals_in_db = get_all_id_deal_db()
    assert sorted(all_deals_in_db) == sorted(test_deals), "Данные не совпадают с ожидаемыми значениями."
    assert len(all_deals_in_db) == len(test_deals), "Количество сделок не совпадает."