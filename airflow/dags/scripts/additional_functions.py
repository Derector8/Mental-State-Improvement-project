from datetime import datetime

restricted_dates = [
    datetime(2024, 6, 11).strftime("%Y-%m-%d"),
    datetime(2024, 6, 13).strftime("%Y-%m-%d"),
    datetime(2024, 6, 15).strftime("%Y-%m-%d"),
    datetime(2024, 6, 25).strftime("%Y-%m-%d"),
]


def check_restricted_dates(**kwargs):
    date_now = kwargs["logical_date"].strftime("%Y-%m-%d")
    if date_now in restricted_dates:
        return "skip_message"
    return "check_wednesday"


def check_wednesday(**kwargs):
    date_now = kwargs["logical_date"].weekday()
    if date_now == 2:
        return ["get_quote_toads", "get_image_toads"]
    return ["get_quote", "get_image"]