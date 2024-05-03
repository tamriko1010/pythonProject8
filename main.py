import csv
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

# Функция получения информации с сайта
def write_cmc_top(path):
    # считываем данные с сайта
    response = requests.get(path)
    if response.status_code == 200:
        html_doc = BeautifulSoup(response.text, features='html.parser')
        list_of_values = html_doc.find_all('span', {'class': 'sc-7bc56c81-1 bCdPBp'})
        list_of_names = html_doc.find_all('p', {'class': 'sc-4984dd93-0 kKpPOn'})
        #print(len(list_of_names))
        i = 0      # количество строк
        summa = 0     #  общая сумма капитализации по всем прочитанным строкам
        result = []     #  результирующий файл
        # паттерн для выделения числа капитализации:
        pat = r'[^$]\S+'
        # перебираем полученную информацию
        for names, values in zip(list_of_names, list_of_values):
            # если больше 100 строк - выходим
            if i == 100:
                break
            # преобразуем данные для занесения в результат
            matched = re.search(pat, values.text)
            val_res = matched.group()
            val = int(val_res.replace(',', ''))
            i += 1
            summa += val
            result.append(({
                'Name': names.text,
                'MC': val_res,
                'MP': val,
            }))
            # расчет и занесение процента
        for item in result:
            m = item['MP']
            procent = round((m / summa) * 100)
            item['MP'] = (f'{procent}%')
        # формируем имя файла
        now = datetime.now()
        formatted_date = f"{now.hour:02d}.{now.minute:02d} {now.day:02d}.{now.month:02d}.{now.year}"
        # запись результата в файл
        with open(f'{formatted_date}.csv', 'w', newline='', encoding='utf-8') as out_file:
            writer = csv.DictWriter(out_file, delimiter=' ', fieldnames=['Name', 'MC', 'MP'])
            writer.writeheader()
            writer.writerows(result)
# Вызывыем функцию
write_cmc_top('https://coinmarketcap.com')






