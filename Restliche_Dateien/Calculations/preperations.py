import datetime as dt


def create_date_order():
    start_date_str = '01/01/2019'
    end_date_str = '31/03/2019'

    start_date = dt.datetime.strptime(start_date_str, '%d/%m/%Y')
    end_date = dt.datetime.strptime(end_date_str, '%d/%m/%Y')

    # Create an empty list to store the dates
    date_list = []

    # Loop to generate dates and append them to the list
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime('%d/%m/%Y'))
        current_date += dt.timedelta(days=1)

    return date_list
