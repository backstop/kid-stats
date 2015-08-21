# Kid Stats
Kid Stats (aka ABC Tracker) is a hackathon project completely unrelated to Backstop, whatsoever.

## Start vagrant

Make sure you have vagrant and virtualbox installed.

    $ vagrant up

## Create index
(change # to a number)

    $ curl -XPOST localhost:9200/kid-stats-# -d @index.json
    $ curl -XPOST localhost:9200/_aliases' -d '
      {
          "actions": [
              { "add": { "index": "kid-stats-#", "alias": "kid-stats" } }
          ]
      }'

## Delete index
(change # to a number)

    $ curl -XDELETE localhost:9200/kid-stats-#

## Adding a new or modifying a field

You can always add more fields to an elasticsearch type by adding data to
your index requests. However if you want to change the mappings you will
need to do a migration.

### Doing a full index migration

1. Make the desired field changes to `index.json` (see the [elasticsearch guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html) for more info).
2. Test the changes by making a new index. (# should be a new number for the index)

    $ curl -XPOST localhost:9200/kid-stats-# -d @index.json

3. Add data to the new index. You will need to either determine what value
   for the new field each old entry should have, create a sensible default
   or leave it blank. You can migrate the data from the old data by reading
   the entires from the old index and inserting them into the new index.
   How to do that is outside of the scope of this guide. See this
   [elasticsearch guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/reindex.html)
   for more information.
4. Ensure your data is in the new index.
5. Delete the old index. (# should be the number for the old index)

    $ curl -XDELETE localhost:9200/kid-stats-#

6. Add the alias to point your new index to `kid-stats`

    $ curl -XPOST localhost:9200/_aliases' -d '
      {
          "actions": [
              { "add": { "index": "kid-stats-#", "alias": "kid-stats" } }
          ]
      }'

## Put randomized stats in index

    $ pip install requests
    $ python gen_random_data.py
