from scrapy import signals
from scrapy.core.downloader import Slot
from random import random



class CustomDownloadDelayMiddleware:
    _CUSTOM_DOWNLOAD_SLOT = "__custom_download_slot_{}__"

    def __init__(self, crawler):
        self.crawler = crawler
        crawler.signals.connect(
            self._request_scheduled, signal=signals.request_scheduled
        )
        crawler.signals.connect(
            self._request_reached_downloader, signal=signals.request_reached_downloader
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _request_reached_downloader(self, request, spider):
        delay =  2 * random() # request.meta.get("custom_download_delay")
        if delay:
            slot_name = self._CUSTOM_DOWNLOAD_SLOT.format(delay)
            self.crawler.engine.downloader.slots[slot_name].delay = delay

    def _request_scheduled(self, request, spider):
        delay = 2 * random()   # request.meta.get("custom_download_delay")
        if delay:
            slot_name = self._CUSTOM_DOWNLOAD_SLOT.format(delay)
            request.meta.setdefault("download_slot", slot_name)
