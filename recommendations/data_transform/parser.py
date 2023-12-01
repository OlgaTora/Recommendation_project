import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'http://округа-районы.москва/все_улицы_москвы'


class Parser:

    def __init__(self):
        self.df = pd.DataFrame(columns=['Наименование', 'Тип', 'Индекс', 'Административный округ', 'Район'])

    #
    # def create_dataframe(self):
    #     response = requests.get(f'{URL}.html')
    #     soup = BeautifulSoup(response.text)
    #     table = soup.find('table', {'class': 'table table-striped table-bordered'})
    #     headers = []
    #     for i in table.find_all('th'):
    #         title = i.text
    #         headers.append(title)
    #     df = pd.DataFrame(columns=headers)
    #     return df

    def get_data(self, page_number):
        response = requests.get(f'{URL}?page={page_number}')
        # response = requests.get(f'{URL}')
        soup = BeautifulSoup(response.text, features='html.parser')
        all_items = soup.find('table', {'class': 'table table-striped table-bordered'})
        for j in all_items.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(self.df)
            # if not self.df['Наименование'].isin(row).any() and row[0]:
            if row[0]:
                self.df.loc[length] = row
        return self.df

    def take_all_pages(self):
        # buf = []
        page_number = 1
        data = self.df
        while page_number <= 309:
            print(page_number)
            data = self.get_data(page_number)
            if data is None:
                break
            # buf.append(data)
            page_number += 1
        # full_data = pd.concat(buf)
        # full_data = full_data.drop(axis=0, index=0)
        return data
