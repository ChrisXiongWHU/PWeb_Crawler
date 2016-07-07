import logging


from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from twisted.python.failure import Failure

from scrapy.utils.response import response_status_message
from scrapy.xlib.tx import ResponseFailed

from PWebCrawler.url_storage import global_quited_url_queue



logger = logging.getLogger(__name__)


class RetryMiddleware(object):
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,Failure,
                           IOError)

    def __init__(self,settings):
        self.max_retry_times = settings.getint('CUSTOM_RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('CUSTOM_RETRY_HTTP_CODES'))

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)

    def process_response(self,request,response,spider):
        if response.status != 200:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider)
        return response


    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self._retry(request, exception, spider)

    def _retry(self,request,reason,spider):
        pages_types = ['api_page','followers_page','developers_page','api_summary','user_page_f','user_page_d']

        retries = request.meta.get('retry_times',0) + 1

        types = request.meta.get('type',0)

        max_retry_times = self.max_retry_times

        if types in pages_types:
            max_retry_times = self.max_retry_times * 3

        if retries <= max_retry_times:
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            if retries > 8:
                retryreq.priority = request.priority - 1
            logger.debug(msg="retrying " + retryreq.url + "  %d times" %(retryreq.meta["retry_times"]))
            return retryreq
        else:
            quited_request = {
                "url":request.url,
                "type":request.meta.get('type',None),
                "item":request.meta.get('item',None),
                "need_access":request.meta.get('need_access',[])
            }
            global_quited_url_queue.append(quited_request)

