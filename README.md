# aiocrossref

Asynchronous client for CrossRef API

## Example

```python
import asyncio

from aiocrossref import CrossrefClient

async def works(doi):
    client = CrossrefClient()
    return await client.works(doi)

response = asyncio.get_event_loop().run_until_complete(works('10.21100/compass.v11i2.812'))
assert(response == { 
  'DOI': '10.21100/compass.v11i2.812',
  'ISSN': ['2044-0081', '2044-0073'],
  'URL': 'http://dx.doi.org/10.21100/compass.v11i2.812',
  'abstract': '<jats:p>Abstract: Educational policy and provision is '
              'ever-changing; but how does pedagogy need to adapt to respond '
              'to transhumanism? This opinion piece discusses transhumanism, '
              'questions what it will mean to be posthuman, and considers the '
              'implications of this on the future of education.</jats:p>',
  'author': [ { 'affiliation': [],
                'family': 'Gibson',
                'given': 'Poppy Frances',
                'sequence': 'first'}],
  'container-title': ['Compass: Journal of Learning and Teaching'],
  'content-domain': {'crossmark-restriction': False, 'domain': []},
  'created': { 'date-parts': [[2018, 12, 17]],
               'date-time': '2018-12-17T09:42:26Z',
               'timestamp': 1545039746000},
  'deposited': { 'date-parts': [[2019, 6, 11]],
                 'date-time': '2019-06-11T10:29:57Z',
                 'timestamp': 1560248997000},
  'indexed': { 'date-parts': [[2020, 4, 14]],
               'date-time': '2020-04-14T14:52:16Z',
               'timestamp': 1586875936184},
  'is-referenced-by-count': 0,
  'issn-type': [ {'type': 'print', 'value': '2044-0073'},
                 {'type': 'electronic', 'value': '2044-0081'}],
  'issue': '2',
  'issued': {'date-parts': [[2018, 12, 10]]},
  'journal-issue': { 'issue': '2',
                     'published-online': {'date-parts': [[2018, 12, 10]]}},
  'link': [ { 'URL': 'https://journals.gre.ac.uk/index.php/compass/article/viewFile/812/pdf',
              'content-type': 'application/pdf',
              'content-version': 'vor',
              'intended-application': 'text-mining'},
            { 'URL': 'https://journals.gre.ac.uk/index.php/compass/article/viewFile/812/pdf',
              'content-type': 'unspecified',
              'content-version': 'vor',
              'intended-application': 'similarity-checking'}],
  'member': '8854',
  'original-title': [],
  'prefix': '10.21100',
  'published-online': {'date-parts': [[2018, 12, 10]]},
  'publisher': 'Educational Development Unit, University of Greenwich',
  'reference-count': 0,
  'references-count': 0,
  'relation': {},
  'score': 1.0,
  'short-container-title': ['Compass'],
  'short-title': [],
  'source': 'Crossref',
  'subtitle': [],
  'title': [ 'From Humanities to Metahumanities: Transhumanism and the Future '
             'of Education'],
  'type': 'journal-article',
  'volume': '11'})
```