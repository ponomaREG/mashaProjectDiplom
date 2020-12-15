import time
import datetime
from dateutil.relativedelta import relativedelta
import calendar



def getTimeStampNow():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def getTimeStampWithOffsetMonths(months):
    future = datetime.datetime.utcnow() + relativedelta(months=months)
    timestamp = calendar.timegm(future.timetuple())
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def getTimeStampWithOffsetMinutes(minutes):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    timestamp = calendar.timegm(future.timetuple())
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

