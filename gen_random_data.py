import argparse
import datetime
from json import JSONEncoder, dumps
from collections import namedtuple
from random import randint, normalvariate, choice

Activity = namedtuple('Activity', ['name', 'start', 'end', 'behavior', 'purposefully_bad', 'notes'])


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


def generate_name(option_count=6):
    return 'Activity {}'.format(randint(0, option_count))

def inc_time(avg_time=40, std_time=5):
    return datetime.timedelta(0, 0, 0, 0, normalvariate(avg_time, std_time))

def generate_behavior():
    b = choice(['Positive', 'Neutral', 'Negative'])
    if b == 'Negative':
        pb = choice([True, False])
    else:
        pb = None
    return b, pb

def generate_records(num_days, per_day=8):
    records = []
    day = datetime.date(2013, 1, 1)
    for i in range(num_days):
        time = datetime.time(9)
        for j in range(per_day):
            name = generate_name()
            start = datetime.datetime.combine(day, time)
            end = start + inc_time()
            time = end.time()
            behavior, purposefully_bad = generate_behavior()
            records.append(Activity(name, start, end, behavior, purposefully_bad, None))
        day += datetime.timedelta(1)
    return records

def main():
    parser = argparse.ArgumentParser(description='Generate random data for kid-stats')
    parser.add_argument('--num_days', type=int, default=365)

    args = parser.parse_args()

    records = [dumps(r, cls=MyEncoder) for r in generate_records(args.num_days)]

    for r in records:
        print r

if __name__ == '__main__':
    main()
