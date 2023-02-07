from datetime import date

class NegativeTitleError(Exception):
    ...

class InvalidYearCupError(Exception):
    ...


class ImpossibleTitlesError(Exception):
    ...

def data_processing(data: dict):
    today = date.today()
    
    first_cup = data["first_cup"]
    first_cup = int(first_cup[0:4])

    year_toverify = today.year - first_cup
    
    verifyYear = first_cup - 1930

    if data["titles"] < 0:
        raise NegativeTitleError("titles cannot be negative")

    if not (verifyYear % 4) == 0 :
        raise InvalidYearCupError("there was no world cup this year")

    if verifyYear < 0 :
        raise InvalidYearCupError("there was no world cup this year")

    if (year_toverify/4) < data["titles"]:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
    