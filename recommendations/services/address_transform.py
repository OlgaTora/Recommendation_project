from address_book.models import Streets, StreetType, StreetsBook
from services.address_parser.street_types_dict import street_types_dict


def address_transform(address: str):
    address = str(address)
    """Function for check user address in address book"""
    street_type = ''
    # если адрес - одно слово
    if len(address.split(',')) != 1:
        address = address.split(',')[1].strip()
        # если можно выделить улицу и дом
        if len(address.split()) != 1:
            tmp = address.split()
            for word in tmp:
                for key, value in street_types_dict.items():
                    if word in value:
                        street_type = key
                        tmp.remove(word)
                        address = (' '.join(tmp))
    if street_type:
        street_names = Streets.objects.filter(
            street_name=address,
            street_type=StreetType.objects.get(street_type=street_type))
        user_address = StreetsBook.objects.filter(
            street_name__in=street_names,
            street_type=StreetType.objects.get(street_type=street_type)
        )
    else:
        street_names = Streets.objects.filter(street_name=address)
        user_address = StreetsBook.objects.filter(street_name__in=street_names)
    return user_address


def admin_districts_transform(address: str) -> list:
    # адрес пользователя: так как нет инфо по району пользователя, берем все улицы с таким названием
    user_address = list(address_transform(address))
    admin_districts = list(set([i.admin_district.admin_district_name for i in user_address]))
    return admin_districts
