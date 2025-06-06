import datetime
from services.supabase_client import supabase_client


def add_separator(number):
    """
    Used to add a thousand separator in a number
    :param number:
    :return new number with separator:
    """
    number = str(number)[::-1]
    result = ""
    for i, index in enumerate(number, 1):
        formatted_number = index + " ," if i % 3 == 0 and i != len(number) else index
        result += formatted_number

    return result[::-1]


def make_object_date(my_date: str):
    my_year = int(my_date[0: 4])
    my_month = int(my_date[5: 7])
    my_day = int(my_date[8:10]
                 )
    return datetime.date(my_year, my_month, my_day)


def convert_date(my_date: str):
    my_year = my_date[0: 4]
    my_month = my_date[5: 7]
    my_day = my_date[8::]

    return f"{my_day}-{my_month}-{my_year}"


def write_date(string_date: str):
    """This function writes the _date of the day"""

    def find_month_name(month_number):
        year_months = [
            'janvier', "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]
        return year_months[month_number - 1]

    the_year = string_date[0: 4]
    the_month = string_date[5: 7]
    the_day = string_date[8:10]
    month_name = find_month_name(int(the_month))
    return str(the_day) + " " + month_name + " " + str(the_year)


def find_facture_number():
    resp = supabase_client.table('factures').select("date").execute()
    result = resp.data
    counter = 0
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year

    if len(result) > 0:
        final = []
        for row in result:
            final.append(
                (make_object_date(row['date'][0:10]).month, make_object_date(row['date'][0:10]).year)
            )

        for item in final:
            if item[0] == current_month and item[1] == current_year:
                counter += 1

        if counter == 0:
            prefix = "001"
        elif 1 <= counter < 9:
            prefix = f"00{counter + 1}"
        elif 9 <= counter < 99:
            prefix = f"0{counter + 1}"
        else:
            prefix = f"{counter + 1}"

        return f"{prefix}-{current_month}-{current_year}"
    else:
        return f"001-{current_month}-{current_year}"

