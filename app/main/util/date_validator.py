import calendar
import datetime
from datetime import date

PYTHON_DATE_FORMAT = "%d/%m/%Y"
DB_DATE_FORMAT = "%Y-%m-%d"


def validate_dates(args, consignment_browse=False):
    errors = {}

    date_filter_field = args.get("date_filter_field", "")

    if consignment_browse and date_filter_field not in [
        "record_date",
        "record_opening_date",
    ]:
        errors["date_filter_field"] = (
            "Select either ‘Record date’ or ‘Record opening date’"
        )
        return None, None, errors

    check_future_date = date_filter_field != "opening_date"

    from_day, from_month, from_year, date_from_errs = validate_date(
        args.get("date_from_day"),
        args.get("date_from_month"),
        args.get("date_from_year"),
        "`Date from`",
        check_future_date,
    )
    if not date_from_errs and (from_day or from_month or from_year):
        from_day, from_month, from_year = complete_date(
            from_day, from_month, from_year, "from", check_future_date
        )

    to_day, to_month, to_year, date_to_errs = validate_date(
        args.get("date_to_day"),
        args.get("date_to_month"),
        args.get("date_to_year"),
        "`Date to`",
        check_future_date,
    )
    if not date_to_errs and (to_day or to_month or to_year):
        to_day, to_month, to_year = complete_date(
            to_day, to_month, to_year, "to", check_future_date
        )

    errors["date_from"] = date_from_errs
    errors["date_to"] = date_to_errs

    if not (date_from_errs or date_to_errs):
        date_from = None
        date_to = None
        if from_day and from_month and from_year:
            date_from = date(from_year, from_month, from_day)
        if to_day and to_month and to_year:
            date_to = date(to_year, to_month, to_day)
        if date_from and date_to and date_from > date_to:
            formatted_date_to = date_to.strftime(PYTHON_DATE_FORMAT)
            err_str = (
                f"Date from must be the same as or before ‘{formatted_date_to}’"
            )
            errors["date_from"].append(err_str)

    return from_day, from_month, from_year, to_day, to_month, to_year, errors


def complete_date(day, month, year, from_or_to, check_future_date):
    if not (day and month) and year:
        month = 1 if from_or_to == "from" else 12
        day, month, year = _complete_day_for_month_and_year(
            month, year, from_or_to, check_future_date
        )

    if not day and month and year:
        day, month, year = _complete_day_for_month_and_year(
            month, year, from_or_to, check_future_date
        )

    return day, month, year


def _complete_day_for_month_and_year(
    month, year, from_or_to, check_future_date
):
    day = calendar.monthrange(year, month)[0 if from_or_to == "from" else -1]
    new_date = date(year, month, day)
    if check_future_date:
        today = date.today()
        if today > new_date:
            day, month, year = today.day, today.month, today.year
    return day, month, year


def validate_date(
    day,
    month,
    year,
    date_field_name,
    check_future_date=True,
):
    errors = []
    if not year:
        if day or month:
            errors = [f"{date_field_name} must include a valid date"]
        return (
            day,
            month,
            year,
            errors,
        )

    try:
        year = int(year)
    except (TypeError, ValueError):
        return (
            day,
            month,
            year,
            [f"{date_field_name} must include a valid month"],
        )
    if not _valid_year(year):
        return (
            day,
            month,
            year,
            [(f"{date_field_name} must include a valid year")],
        )

    if not month:
        if day:
            errors = [f"{date_field_name} must include a valid date"]
        return (
            day,
            month,
            year,
            errors,
        )
    try:
        month = int(month)
    except (TypeError, ValueError):
        return (
            day,
            month,
            year,
            [f"{date_field_name} must include a valid month"],
        )
    if not _valid_month(month):
        return (
            day,
            month,
            year,
            [f"{date_field_name} must include a valid month"],
        )

    if not day:
        return day, month, year, errors

    try:
        day = int(day)
    except (TypeError, ValueError):
        return (
            day,
            month,
            year,
            [f"{date_field_name} must include a valid month"],
        )
    if not _valid_day(day, month, year):
        return (
            day,
            month,
            year,
            [f"{date_field_name} must be a real date"],
        )

    if check_future_date and day and month and year:
        input_date = date(year, month, day)
        if input_date > date.today():
            errors = [f"{date_field_name} must be in the past"]

    return day, month, year, errors


def _valid_year(year):
    return 1900 <= year <= datetime.date.today().year


def _valid_day(day, month, year):
    last_day = _get_last_day_of_month(month, year)
    return 1 <= day <= last_day


def _valid_month(month):
    return 1 <= month <= 12


def _get_last_day_of_month(month, year):
    if month == 2:
        if year % 4 == 0 or year % 100 == 0 or year % 400 == 0:
            last_day = 29
        else:
            last_day = 28
    elif month in (1, 3, 5, 7, 8, 10, 12):
        last_day = 31
    else:
        last_day = 30

    return last_day


# def format_date_elements_to_have_trailing_zeros_for_ui(day, month, year):
#     day_var = int(
#         day.rjust(2, "0") if len(str(day)) == 1 else day if day else 0 * 2
#     )
#     month_var = int(
#         month.rjust(2, "0")
#         if len(str(month)) == 1
#         else month if month else 0 * 2
#     )
#     year_var = int(year.ljust(4, "0") if year and len(str(year)) > 0 else 0 * 4)