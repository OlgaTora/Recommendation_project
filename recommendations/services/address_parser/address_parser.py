import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'http://округа-районы.москва/все_улицы_москвы'


class AddressParser:

    def __init__(self):
        self.df = pd.DataFrame(columns=['Наименование', 'Тип', 'Индекс', 'Административный округ', 'Район'])

    def get_data(self, page_number):
        response = requests.get(f'{URL}?page={page_number}')
        soup = BeautifulSoup(response.text, features='html.address_parser')
        all_items = soup.find('table', {'class': 'table table-striped table-bordered'})
        for j in all_items.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(self.df)
            if row[0]:
                self.df.loc[length] = row
        return self.df

    def take_all_pages(self):
        page_number = 1
        data = self.df
        while page_number <= 309:
            print(page_number)
            data = self.get_data(page_number)
            if data is None:
                break
            page_number += 1
        return data
