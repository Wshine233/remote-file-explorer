import os
from datetime import datetime


def filter_keyword(files, keyword):
    result = []
    for file in files:
        if keyword in file['name']:
            result.append(file)
    return result


def filter_type(files, type):
    result = []
    for file in files:
        if file['type'] in type:
            result.append(file)
    return result


def filter_extention(files, extention, keep_dir, black_list):
    result = []
    extentions = extention.split(';')
    for file in files:
        if file['type'] == 0:
            if keep_dir:
                result.append(file)
            continue
        if black_list and file['name'].split('.')[-1] in extentions:
            continue
        if not black_list and file['name'].split('.')[-1] not in extentions:
            continue
        result.append(file)
    return result
            


def filter_modified_time(files, timeFrom, timeTo):
    result = []
    timeFrom = timeFrom.split('.')[0]
    timeTo = timeTo.split('.')[0]
    timeFrom = datetime.strptime(timeFrom, '%Y-%m-%dT%H:%M:%S').timestamp()
    timeTo = datetime.strptime(timeTo, '%Y-%m-%dT%H:%M:%S').timestamp()
    for file in files:
        if file['time_modified'] >= timeFrom and file['time_modified'] <= timeTo:
            result.append(file)
    return result


def filter_created_time(files, timeFrom, timeTo):
    result = []
    timeFrom = timeFrom.split('.')[0]
    timeTo = timeTo.split('.')[0]
    timeFrom = datetime.strptime(timeFrom, '%Y-%m-%dT%H:%M:%S').timestamp()
    timeTo = datetime.strptime(timeTo, '%Y-%m-%dT%H:%M:%S').timestamp()
    for file in files:
        if file['time_created'] >= timeFrom and file['time_created'] <= timeTo:
            result.append(file)
    return result