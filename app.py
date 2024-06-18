import timeit
from bitrix_mail_registration import main

start = timeit.default_timer()
print(f"Скрипт проверки регистрации писем запущен: {start}")
main()
finish = timeit.default_timer() - start
print(f"Скрипт завершен за {finish} секунд")