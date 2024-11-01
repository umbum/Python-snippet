import requests

HOST = "https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000"
HEADERS = {
    'Cookie' : '''WMONID=GjLIkbkSJjH; JSESSIONID_ETK=BnhEX2wYBMau8HyooHONaaeRtKvHIDLvxGhImF1KQC7tRfJTvHZ9WZAPzvZVJZda.ZXRrcC9IRVRLQ09OMDI=; PCID=17304577829056096585193; RC_COLOR=30; wcCookieV2=1.227.112.105_T_662401_WC; RC_RESOLUTION=1470*956''',
    'User-Agent': '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Whale/3.27.254.15 Safari/537.36''',
    'Content-Type': '''application/x-www-form-urlencoded''',
    'Accept-Encoding': '''gzip, deflate, br, zstd''',

}
DATA = {
    "key": "E0C43F87BB683D70E085955D5A03F4601921E6C1B80BA69FCDAB7C53177C1A3DA7212EC26BB35F685225E7C54E59570E66CBA3C204452B473B8CBCC4D5967D26164EBDFA76313BB167C20C40CF83B9D55E152CBDF7930FE982F90BACF475B79DE6CCCF67E40643DA8657C5AAFA595C692C302C30",
    "dptRsStnCd": "0552",
    "arvRsStnCd": "0036",
    "stlbTrnClsfCd": "05",
    "psgNum": "1",
    "seatAttCd": "015",
    "isRequest": "Y",
    "dptRsStnCdNm": "동탄",
    "arvRsStnCdNm": "광주송정",
    "dptDt": "20241109",
    "dptTm": "000000",
    "chtnDvCd": "1",
    "psgInfoPerPrnb1": "1",
    "psgInfoPerPrnb5": "0",
    "psgInfoPerPrnb4": "0",
    "psgInfoPerPrnb2": "0",
    "psgInfoPerPrnb3": "0",
    "locSeatAttCd1": "000",
    "rqSeatAttCd1": "015",
    "trnGpCd": "109",
    "dlayTnumAplFlg": "Y",
}

def request():
    r = requests.post(f"{HOST}", headers=HEADERS, data=DATA)
    print(f"{r.text}")

if __name__ == '__main__':
    request()
