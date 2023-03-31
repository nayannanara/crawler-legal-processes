def format_date(string_date: str) -> str:
    datetime_split = string_date.replace('/', '-').split()
    date = datetime_split[0]
    hour = datetime_split[1]
    date_split = date.split('-')
    new_date = f'{date_split[2]}-{date_split[1]}-{date_split[0]} {hour}'

    return new_date
