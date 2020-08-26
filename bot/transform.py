def transform_number(phone):
    return f"+7 {phone[2:5]}{phone[5:8]}-{phone[8:10]}-{phone[10:12]}"


def transform_date(date):
    return f"{date[6:10]}-{date[0:2]}-{date[3:5]}"
