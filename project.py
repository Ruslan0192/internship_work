import os
import csv


FNAME = 'out_html/output.html'
FILE_PATH = 'pricelist'
NAME_PRODUCT = ["название", "продукт", "товар", "наименование"]
PRICE_PRODUCT = ["цена", "розница"]
WEIGHT_PRODUCT = ["фасовка", "масса", "вес"]

class PriceMachine():
    
    def __init__(self):
        self.data = []
        self.result = []
        self.name_length = 0
    
    def load_prices(self, file_path=FILE_PATH):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

        with os.scandir(file_path) as find_file:
            for entry in find_file:
                if entry.name.startswith('price') and entry.is_file():
                    # чтение файла и сохранение в список
                    with open(entry.path, newline='', encoding='UTF-8') as csvfile:
                        reader_csv = csv.DictReader(csvfile)
                        # определение столбцов
                        fieldnames = self._search_product_price_weight(reader_csv)
                        # заполняю список для всех файлов
                        for row in reader_csv:
                            name_file = entry.name
                            price_for_kg = round(float(row[fieldnames[1]])/float(row[fieldnames[2]]), 2)
                            self.data.append([row[fieldnames[0]], row[fieldnames[1]], row[fieldnames[2]], name_file, price_for_kg])
                            if self.name_length < len(row[fieldnames[0]]):
                                self.name_length = len(row[fieldnames[0]])

        self.data.sort(key=lambda x: x[4])
        return self.data


    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        read_head = headers.fieldnames
        fieldnames = []
        # поиск Название
        for fieldname in read_head:
            for name_prod in NAME_PRODUCT:
                if fieldname == name_prod:
                    fieldnames.append(fieldname)
        # поиск Цена
        for fieldname in read_head:
            for name_prod in PRICE_PRODUCT:
                if fieldname == name_prod:
                    fieldnames.append(fieldname)
        # поиск Фасовка
        for fieldname in read_head:
            for name_prod in WEIGHT_PRODUCT:
                if fieldname == name_prod:
                    fieldnames.append(fieldname)
        return fieldnames


    def export_to_html(self, fname=FNAME):
        if len(self.result) == 0:
            return

        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        for number, name, price, weight, file, price_for_kg in self.result:
            result += f'<tr><td>{number}</td><td>{name}</td><td>{price}</td><td>{weight}</td><td>{file}</td><td>{price_for_kg}</td></tr>\n'
        result += '</tbody></table>'

        html_file = open(fname, "w")
        html_file.write(result)
        html_file.close()
        return result

    
    def find_text(self, text):
        self.result = []
        count_result = 0
        no_find_text =True

        for name, price, weight, file, price_for_kg in self.data:
            if text.lower() in name.lower():
                if no_find_text:
                    no_find_text = False
                    print('№     Наименование                           цена     вес      файл     цена за кг.')
                count_result += 1
                self.result.append([count_result, name, price, weight, file, price_for_kg])

                # вывод на экран с выравниванием
                if count_result < 10:
                    count_result_pr =' '+ str(count_result)
                else:
                    count_result_pr = str(count_result)


                count = self.name_length - len(name)
                name += count*' '

                count = 5 - len(price)
                price += count*' '
                print(f'{count_result_pr}  {name} {price}    {weight}    {file}   {price_for_kg}')
        if no_find_text:
            print('Данное наименование отсутствует')


    
pm = PriceMachine()
print(pm.load_prices(FILE_PATH))

'''
    Логика работы программы
'''
while True:
    text = input("Введите наименование товара или его часть: ")
    if text == 'exit':
        break
    pm.find_text(text)

print('the end')
print(pm.export_to_html())
