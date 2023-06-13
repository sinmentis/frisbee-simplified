Frisbee
=======
Frisbee is a small utility to collect email addresses from search engines and
other free-form text sources. Frisbee makes it simple to find email addresses
posted on the web by taking user-fed input and translating it into an
automated search query. Users can extend frisbee by adding modules for new
search engines or other obscure data sources.

Changes done to this repo
-----------
In order to integrate into [MassEmailSender](https://github.com/sinmentis/MassEmailSender), I "clean up" the code a bit to keep the basically functionality of searching and return.
* Removed the printout log.
* Removed save to local.
* Removed all the beautiful doc and makefile.

If you are looking for other simplified version of email parser, try [this](https://github.com/sinmentis/EmailAll-simplified/)

**Please visit original repo in [here](https://github.com/9b/frisbee)**

Features
--------
* Ability to search for email addresses from search engine results
* Modular design that can be extended easily to include new sources
* Modifier options that can filter or target search query
* Limit option to reduce the number of results parsed
* Greedy option to learn from collected results and fuzzy to find related
* Save output describing job request and results
* Individual or bulk look-ups using the command line utility