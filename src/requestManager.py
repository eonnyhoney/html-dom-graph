import requests

# requests library manager
# work same as requests
class RequestManager():

    # temporary url
    url = 'https://www.naver.com/'

    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # Accept-Encoding: gzip, deflate, br
        # Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
        # Cache-Control: max-age=0
        # Connection: keep-alive
        # Cookie: webid=e70c256bb2fb418681da50f14d29543b; _TI_NID=iok9mjEFfnWoNqMjDA5hhbM2ZL7dedahV9CJfnMgClE7GbyPy28rlxjoERcM5zfS/O27ySUEM+ttMCozzhF3og==; webid_ts=1590975728613; ssab=; webid_sync=1592966752980; TIARA=dfRVBcGREbVFpSlOK8YW_L5H1iIa6JpD5_RI4zWUsxmAk4ENwix37l2bbs7rY9tNL2kEomc_M5SXI.2t-jAtP1VbERO5THlp; sf_ck_tst=test
        # Host: news.daum.net
        # Sec-Fetch-Dest: document
        # Sec-Fetch-Mode: navigate
        # Sec-Fetch-Site: none
        # Sec-Fetch-User: ?1
        # Upgrade-Insecure-Requests: 1
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
    }

    # 현재는 url에 parameter값이 들어가있음.
    params = {}

    def __init__(self, url):
        self.url = url

    # requests 함수와 동일한 역할.
    def requests(self):
        res = requests.get(self.url, headers=self.headers, params=self.params)
        print('request status code is ', res.status_code)
        return res
