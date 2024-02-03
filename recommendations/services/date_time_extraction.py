def extract_time_weekday(elem: list) -> dict:
    weeksdays_list = ['Пн.', 'Вт.', 'Ср.', 'Чт.', 'Пт.', 'Сб.', 'Вс.']
    times = []
    weeksdays = []
    schedule_dict = {}
    for j in elem:
        if j in weeksdays_list:
            weeksdays.append(j[:-1])
        if '-' in j:
            times.append(j)
    if len(weeksdays) == len(times):
        schedule_dict = dict(zip(weeksdays, times))
    elif len(weeksdays) > len(times):
        for i in weeksdays:
            schedule_dict[i] = times[0]
    else:
        for i in times:
            times[i] = weeksdays
    if schedule_dict:
        return schedule_dict


def clean_str(s: str) -> str:
    str_clean = (s.replace('c', '')
                 .replace('по', '')
                 .replace('без перерыва', '')
                 .replace(',', '')).strip()
    return str_clean


def case_one_time(s: str) -> list:
    """
    обработка случая 'c 31.03.2023 по 31.12.2023, Пн., Ср. 17:00-19:00, без перерыва'
    """
    str_clean = clean_str(s)
    spl = [i for i in str_clean.split(' ')]
    lst = []
    schedule_dict = extract_time_weekday(spl)
    if schedule_dict:
        for day, times in schedule_dict.items():
            lst.append([spl[0], spl[2], day, times])
    return lst


def case_two_dates_two_time(s: str) -> list:
    """
    обработка случая 'c 31.03.2023 по 31.12.2023, Вт. 17:00-19:00, без перерыва, Пт. 13:00-15:00, без перерыва'
    """
    str_split = s.split('без перерыва')
    str_clean = clean_str(str_split[0])
    spl = [i for i in str_clean.split(' ')]
    lst = []
    schedule_dict = extract_time_weekday(spl)
    if schedule_dict:
        for day, times in schedule_dict.items():
            lst.append([spl[0], spl[2], day, times])
    for i in range(1, len(str_split)):
        new_str_split = [i for i in clean_str(str_split[i]).split(' ')]
        schedule_dict_ = extract_time_weekday(new_str_split)
        if schedule_dict_:
            for day_, times_ in schedule_dict_.items():
                lst.append([spl[0], spl[2], day_, times_])
    return lst


def case_two_dates_one_time(s: str) -> list:
    """
    обработка случая 'c 01.06.2022 по 11.08.2022, Пн., Ср. 12:05-13:05, без перерыва;
    c 01.01.2022 по 31.05.2022, Пн., Ср. 12:15-13:15, без перерыва;
    """
    result = []
    spl = [i.strip() for i in s.split(';')]
    for lst in spl:
        if lst.count('перерыв') > 1:
            lst = case_two_dates_two_time(lst)
            result += lst
        else:
            lst = case_one_time(lst)
            result += lst
    return result
