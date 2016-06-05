import time
from datetime import datetime

def get_time():
    m_time = time.localtime()
    timestamp = {'year': m_time[0],
                 'month':m_time[1],
                 'day':  m_time[2],
                 'hour': m_time[3],
                 'minutes':m_time[4],
                 'seconds':m_time[5]
                }
    return timestamp

def string2time(string):
    values = string.split(',')
    fields = ['year', 'month', 'day', 'hour', 'minutes', 'seconds']
    timestamp = {}

    for index in range(len(fields)):
        timestamp[fields[index]] = int(values[index])

    return timestamp

def time2string(timestamp):
    time_string = ''

    time_string += str(timestamp['year']) + ','
    time_string += str(timestamp['month']) + ','
    time_string += str(timestamp['day']) + ','
    time_string += str(timestamp['hour']) + ','
    time_string += str(timestamp['minutes']) + ','
    time_string += str(timestamp['seconds'])

    return time_string

def getTime():
    t = get_time()
    return time2string(t)

def diff_time(old_time, new_time=None, unit='sec'):
    old_date = datetime.strptime(old_time, "%Y,%m,%d,%H,%M,%S")
    new_date = datetime.strptime(new_time, "%Y,%m,%d,%H,%M,%S")

    diff = new_date - old_date # it gives you two deltas

    if unit is 'min': # alternative is minutes.
        return diff.seconds / 60
    return diff.seconds # defaults to seconds
