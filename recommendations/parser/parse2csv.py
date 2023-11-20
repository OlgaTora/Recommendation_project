from parser import Parser

parser = Parser()
data = parser.take_all_pages()
data.to_csv('/home/olgatorres/PycharmProjects/Diplom_project/recommendations/files/moscow_streets.csv', index=False)


# import os
# from sqlalchemy import create_engine

# db = os.environ.get('DATABASE')
# user = os.environ.get('USER')
# password = os.environ.get('PASSWORD')
# host = 'localhost'
#
# engine = create_engine('mysql+mysqldb://user:password@localhost:3306/db', echo=False)
# data.to_sql(name='Moscow streets', con=engine, if_exists='replace', index=False)


