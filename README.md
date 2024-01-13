# roshtein_data_crawl

Having lots of scripts doing lots of different things with bonushunt data
I'm trying to collect and sort them into a single package.


# Boogers
Notes for myself to fix

- crawler.py
Filenames is incorrect not giving correct names for bonushunts.
self.slug_name = int(data_json['response']['stats']['bonushunt_slug']) in connect() should fix it
maybe self.slug_name += 1 in download() is the problem?
 - Seem to be when first download, after success it says it already exists and skips +1