from address_parser import AddressParser

parser = AddressParser()
data = parser.take_all_pages()
data.to_csv(
    '/recommendations/files/moscow_streets.csv',
    index=False,
)

