#!/bin/sh
for i in `seq 0 5`
do
  start=`expr $i \* 1000`
  curl 'https://data.overheid.nl/data/api/3/action/package_search' -d '{"q": "", "start": '$start', "rows": 6000}' >"data-overheid-dump-$i.json"
done
