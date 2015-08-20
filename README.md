# Kid Stats


## Create index

    $ curl -XPOST localhost:9200/kid-stats -d @index.json

## Put randomized stats in index

    $ pip install requests
    $ python gen_random_data.py
