from datetime import datetime


def convert_date(date: str) -> str:
    """This function converts YYYY-MM-DD to MMM DD, YYYY

    Args:
        date (str): [description]

    Returns:
        str: [description]
    """
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    return date_time_obj.strftime('%b %d, %Y')
