from datetime import datetime, timedelta

# 1. Subtract five days from the current date
def subtract_days(days):
    return datetime.now() - timedelta(days=days)

# 2. Print yesterday, today, tomorrow
def print_yesterday_today_tomorrow():
    today = datetime.now().date()
    return today - timedelta(days=1), today, today + timedelta(days=1)

# 3. Drop microseconds from datetime
def drop_microseconds():
    return datetime.now().replace(microsecond=0)

# 4. Calculate two date difference in seconds
def date_difference_in_seconds(date1, date2):
    return abs((date2 - date1).total_seconds())


print(subtract_days(5))
print(print_yesterday_today_tomorrow())
print(drop_microseconds())

d1 = datetime(2024, 2, 15, 12, 0, 0)
d2 = datetime(2024, 2, 20, 14, 30, 0)
print(date_difference_in_seconds(d1, d2))
