from datetime import datetime


def convert_date(date: str):
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    return date_time_obj.strftime('%b %d, %Y')

