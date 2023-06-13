#!/usr/bin/env python
from bs4 import BeautifulSoup
from Frisbee.modules.base import Base
from Frisbee.utils import extract_emails


class Module(Base):

    """Custom search module."""

    def __init__(self, domain=None, modifier=None, engine="bing", greedy=False,
                 fuzzy=False, limit=500):
        """Setup the primary client instance."""
        super(Base, self).__init__()
        self.name = "Bing"
        self.host = "https://www.bing.com"
        self.domain = domain
        self.modifier = modifier
        self.limit = limit
        self.greedy = greedy
        self.fuzzy = fuzzy

        self.results = list()
        self.data = list()

        self._start_time = None
        self._end_time = None
        self._duration = None

    def _format(self):
        """Format search queries to perform in bulk.

        Build up the URLs to call for the search engine. These will be ran
        through a bulk processor and returned to a detailer.
        """
        items = list()
        for i in range(0, self.limit, 10):
            query = '"%s" %s' % (self.domain, self.modifier)
            url = self.host + "/search?q=" + query + "&first=" + str(i)
            items.append(url)
        return items

    def _process(self, responses):
        """Process search engine results for detailed analysis.

        Search engine result pages (SERPs) come back with each request and will
        need to be extracted in order to crawl the actual hits.
        """
        items = list()
        for response in responses:
            try:
                soup = BeautifulSoup(response.content, 'html.parser',
                                     from_encoding="iso-8859-1")
            except:
                continue
            else:
                listings = soup.findAll('li', {'class': 'b_algo'})
                items.extend([l.find('a')['href'] for l in listings])
        return items

    def _fetch(self, urls):
        """Perform bulk collection of data and return the content.

        Gathering responses is handled by the base class and uses futures to
        speed up the processing. Response data is saved inside a local variable
        to be used later in extraction.
        """
        responses = self._request_bulk(urls)
        for response in responses:
            if len(response.content) > 3000000:
                continue
            try:
                soup = BeautifulSoup(response.content, 'html.parser',
                                     from_encoding="iso-8859-1")
                text = soup.get_text()  # This will result in errors at times as it smashes text together with the email address
            except Exception:
                text = response.text
            self.data.append(text) # Opportunistic findings
        return responses

    def _extract(self):
        """Extract email addresses from results.

        Text content from all crawled pages are ran through a simple email
        extractor. Data is cleaned prior to running pattern expressions.
        """
        for item in self.data:
            emails = extract_emails(item, self.domain, self.fuzzy)
            self.results.extend(emails)
        return list(set(self.results))

    def search(self):
        """Run the full search process.

        Simple public method to abstract the steps needed to produce a full
        search using the engine.
        """
        requests = self._format()
        serps = self._fetch(requests)
        urls = self._process(serps)
        details = self._fetch(urls)
        emails = self._extract()
        return {'emails': emails, 'processed': len(self.data)}
