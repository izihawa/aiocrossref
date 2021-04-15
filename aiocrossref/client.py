import asyncio
import time
import typing
import urllib.parse

import orjson as json
from aiobaseclient import BaseClient
from aiocrossref.exceptions import (
    ClientError,
    NotFoundError,
    ServiceUnavailableError,
    TooManyRequestsError,
    WrongContentTypeError,
)
from izihawa_types.safecast import safe_int


class CrossrefClient(BaseClient):
    def __init__(
        self,
        base_url: str = 'https://api.crossref.org/',
        user_agent: str = None,
        delay: float = 1.0 / 50.0,
        timeout: float = None,
        max_retries=2,
        retry_delay=0.5,
        proxy_url=None,
    ):
        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
        super().__init__(
            base_url=base_url,
            default_headers=headers,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            proxy_url=proxy_url,
        )
        self.delay = delay
        self.last_query_time = 0.0

    def set_limits(self, headers):
        interval = safe_int(headers.get('X-Rate-Limit-Interval', '0').rstrip('s')) or 0
        limit = safe_int(headers.get('X-Rate-Limit-Limit', '1')) or 1
        self.delay = float(interval / limit)

    async def pre_request_hook(self):
        t = time.time()
        if t - self.last_query_time < self.delay:
            await asyncio.sleep(t - self.last_query_time)
        self.last_query_time = t

    async def works(self, doi='', **params):
        r = await self.get(f'/works/{urllib.parse.quote(doi)}', params=params)
        return r['message']

    async def works_cursor(self, doi='', **params):
        params['cursor'] = '*'
        while True:
            response = await self.works(doi, **params)
            if len(response['items']) == 0:
                break
            yield response
            params['cursor'] = response['next-cursor']

    async def response_processor(self, response):
        self.set_limits(response.headers)
        data = await response.text()
        content_type = response.headers.get('Content-Type', '').lower()
        if not response.headers.get('Content-Type', '').lower().startswith('application/json'):
            if response.status == 404:
                raise NotFoundError(data=data, status=response.status, url=str(response.url))
            elif response.status == 429:
                raise TooManyRequestsError(status=response.status, url=str(response.url))
            elif response.status == 503:
                raise ServiceUnavailableError(status=response.status, url=str(response.url))
            raise WrongContentTypeError(content_type=content_type, data=data, status=response.status)
        data = json.loads(data)
        if isinstance(data, typing.Dict) and (data.get('status') == 'error' or data.get('status') == 'failed'):
            if (
                data.get('message', {}).get('name') in (
                    'class org.apache.solr.client.solrj.impl.HttpSolrClient$RemoteSolrException',
                    'class com.mongodb.MongoTimeoutException',
                )
            ):
                raise NotFoundError(data=data, status=response.status, url=str(response.url))
            raise ClientError(**data)
        return data
