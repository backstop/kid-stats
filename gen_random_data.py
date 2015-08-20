import argparse
import datetime
import requests
from itertools import count, islice
from json import JSONEncoder, dumps
from collections import namedtuple
from random import randint, normalvariate, choice, sample


Activity = namedtuple('Activity', ['name', 'start', 'end', 'dow_index', 'behavior', 'behavior_index', 'behavior_mixed_index', 'purposefully_bad', 'notes'])


class MyEncoder(JSONEncoder):
    def iterencode(self, obj, **kwargs):
        if isinstance(obj, tuple) and hasattr(obj, '_asdict'):
            gen = self.iterencode(obj._asdict(), **kwargs)
        else:
            gen = super(MyEncoder, self).iterencode(obj, **kwargs)
        for chunk in gen:
            yield chunk

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

def generate_names():
    for i in count(1):
        yield 'Activity {}'.format(i)

def inc_time(avg_time=40, std_time=5):
    return datetime.timedelta(0, 0, 0, 0, normalvariate(avg_time, std_time))

def generate_behavior():
    behaviors = ['Negative', 'Neutral', 'Positive']
    bi = randint(- 1, len(behaviors) - 2)
    b = behaviors[bi + 1]
    if b == 'Negative':
        pb = choice([True, False])
        bmi = bi - (1 if pb else 0)
    else:
        pb = None
        bmi = bi
    return b, bi, pb, bmi

def generate_records(num_days, per_day=8, activity_count=12):
    records = []
    all_activities = list(islice(generate_names(), activity_count))
    day = datetime.date(2013, 1, 1)
    for i in range(num_days):
        time = datetime.time(9)
        dow_index = day.weekday()
        for activity_name in sample(all_activities, per_day):
            start = datetime.datetime.combine(day, time)
            end = start + inc_time()
            time = end.time()
            behavior, behavior_index, purposefully_bad, behavior_mixed_index = generate_behavior()
            records.append(Activity(activity_name, start, end, dow_index, behavior, behavior_index, behavior_mixed_index, purposefully_bad, None))
        day += datetime.timedelta(1)
    return records

def main():
    parser = argparse.ArgumentParser(description='Generate random data for kid-stats')
    parser.add_argument('--num_days', type=int, default=365)
    parser.add_argument('--dump', action='store_true')

    args = parser.parse_args()

    records = [dumps(r, cls=MyEncoder) for r in generate_records(args.num_days)]

    if args.dump:
        for r in records:
            print r
    else:
        for r in records:
           resp = requests.post('http://localhost:9200/kid-stats/activity', data=r)
           print resp.json()

if __name__ == '__main__':
    main()
