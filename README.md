# Kid Stats
Kid Stats (aka ABC Tracker) is a hackathon project completely unrelated to Backstop, whatsoever.

## Create index

    $ curl -XPOST localhost:9200/kid-stats -d @index.json

## Put randomized stats in index

    $ pip install requests
    $ python gen_random_data.py
