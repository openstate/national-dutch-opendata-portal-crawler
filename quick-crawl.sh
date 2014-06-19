#!/bin/sh
for i in `seq 0 600`
do
  start=`expr $i \* 10`
  curl 'https://data.overheid.nl/data/api/3/action/package_search' -d '{"q": "", "start": '$start', "rows": 10}' >"data-overheid-dump-$i.json"
done
