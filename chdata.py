import time


def date_import():
    second = time.time()
    local_time = time.localtime(second)
    date = []
    date.append(local_time.tm_mday)
    date.append(local_time.tm_mon)
    date.append(local_time.tm_year)

    return date
