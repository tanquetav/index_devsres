# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from urllib.parse import quote
import json
from datetime import datetime
API = 'YOURAPIKEY'
user_accounts = ['marcelo_devsres'] 


def get_url(url):
    return url


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    custom_settings = {'CONCURRENT_REQUESTS_PER_DOMAIN': 5}

    def start_requests(self):
        self.fd = open("data/out.md","w")
        for username in user_accounts:
            url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'
            yield scrapy.http.JsonRequest(get_url(url), headers={"x-ig-app-id": "936619743392459"}, callback=self.parse2)

    def parse2(self, response):
        #open_in_browser(response)
        js = json.loads(response.body)
        self.id = js['data']['user']['id']
        #print(id)
        ss={"id":self.id,"first":12,"after":None}
        vvv = quote(json.dumps(ss))
        #vvv = '%7B%22id%22%3A%22'+id+'%22%2C%22first%22%3A%2012%7D'
        url = 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables='+vvv
        yield scrapy.http.JsonRequest(get_url(url), headers={"x-ig-app-id": "936619743392459"}, callback=self.parse3)

    def parse3(self, response):
        # open_in_browser(response)
        js = json.loads(response.body)
        posts = js["data"]["user"]["edge_owner_to_timeline_media"]
        page_info = posts["page_info"]
        for post in posts["edges"]:
            short = post['node']['shortcode']
            text = ""
            edges = post['node']['edge_media_to_caption']['edges']
            if (len(edges)>0):
                text = edges[0]['node']['text']
            display_url=post['node']['display_url']
            self.fd.write("# Post \n")
            lnk = "https://www.instagram.com/p/"+short

            self.fd.write(f"[{lnk}]({lnk})\n\n")
            self.fd.write(f"![]({short}.jpg)\n")
            self.fd.write(f"\n\n{text}\n\n\n")
            yield scrapy.Request(get_url(display_url),
                    headers={"x-ig-app-id": "936619743392459","Short":short},
                    callback=self.downImage)
        if page_info["has_next_page"]:
            ss={"id":self.id,"first":12,"after":page_info["end_cursor"]}
            vvv = quote(json.dumps(ss))
            url = 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables='+vvv
            yield scrapy.http.JsonRequest(get_url(url), headers={"x-ig-app-id": "936619743392459"}, callback=self.parse3)
    def downImage(self, response):
        shortb=response.request.headers['Short']
        f = open('data/'+shortb.decode('utf-8')+".jpg", "wb")
        f.write(response.body)
        f.close()
        