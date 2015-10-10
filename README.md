# ubergraph
Log Uber surge rate for a location to mysql and graph data via matplotlib

Bare working version. Hardcoded (but easily changed): location and use of uberx.

Mysql schema: create table uberx(type varchar(30), date timestamp, surge double);

To run:

./ubergraph.py # to log to mysql

./createGraphMat.py # to output graph to disk

Example graph:

![alt tag](http://i.imgur.com/k66JjAG.jpg)
