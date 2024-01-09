from recommendations.data_transform.parser import Parser

parser = Parser()
data = parser.take_all_pages()
data.to_csv(
    '/recommendations/files/moscow_streets.csv',
    index=False,
)


