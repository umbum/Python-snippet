import requests
from time import sleep
from urllib.parse import urlencode



target_date = '20241109'
time_after = '100000'  # 10시 이후면, 10 + 0000 이 시간을 잘못 설정하면 대상 item이 안보일 수도.
departures = '광주송정'
arrivals = '수서'

def train_filter_condition(trainInfo):
    return trainInfo['dptTm'] in ('101800', '104300', '111300', '125600', '134300')

def is_satisfied(trainInfo):
    return trainInfo['sprmRsvPsbStr'] != '매진' or trainInfo['gnrmRsvPsbStr'] != '매진' or (trainInfo['rsvWaitPsbCdNm'] != '매진' and trainInfo['rsvWaitPsbCdNm'] != '-')

#################################################################

STATION_CODE = {
    '수서': '0551',
    '동탄': '0552',
    '광주송정': '0036',
}

HOST = "https://app.srail.or.kr/ara/selectListAra10007_n.do"

HEADERS = {
    # 'Cookie' : '''srailSID=SRAIL_VJch0mQ3gf8nfHu; WMONID=jBDPV0aY0gy; wcCookieV2=211.234.205.230_T_138906_WC; deviceKey=E52DB8E2F7BB9CFE; gs_loginEmailNo=umbum7601@naver.com; srail_type8=N; srail_type10=rTGERyzDRtKWigTuQEhCXEMFQNBu4Acbf9yjy/Lq/+R78t+A/NTkMWTeZKkH2leJ1CMSD22BhkDTODpJKTVVzaUCc45sD0JdlUnxnW/r8UfGxo512nSLiJQqlzJ1HPrdSQMaUxQe6sMGpKn2QyMxn2QhhI0WdN/gVKmftZkARcs=; JSESSIONID_XEBEC=aa2Rc2rpYDSVAFalfG6LyT2a3IbsFlx8xayuBifJLqa1scmGvXiVDWl4AzcBbilI.YXBwL0FQUENPTjAzLTM=''',
    'User-Agent': '''Mozilla/5.0 (Linux; Android 14; SM-S911N Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36SRT-APP-Android V.2.0.30''',
    'Content-Type': '''application/x-www-form-urlencoded; charset=UTF-8''',
    'Accept-Encoding': '''gzip, deflate, br, zstd''',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'sec-ch-ua-platform': "Android",
    'X-Requested-With': "XMLHttpRequest",
}

DATA = {
    "chtnDvCd": '1',
    "dptDt": target_date,
    "dptTm": time_after,    
    "dptDt1": target_date,
    "dptTm1": time_after,
    "dptRsStnCd": STATION_CODE[departures],
    "arvRsStnCd": STATION_CODE[arrivals],
    "stlbTrnClsfCd": '05',
    "trnGpCd": '109',
    "trnNo":  '',        
    "psgNum": '1',
    "seatAttCd": '015',
    "arriveTime": 'N',
    "tkDptDt":  '',
    "tkDptTm":  '',
    "tkTrnNo":  '',
    "tkTripChgFlg":  '',
    "dlayTnumAplFlg": 'Y',
}

#################################################################

NOTI_ACCESS_TOKEN = 'mF8dG9OERxGye5Ticv7Sj8yi6lz3xqPudivs0Co89Lx'

def notify(msg):
    headers = {
        "Authorization": f"Bearer {NOTI_ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    }
    data = {
        "message": msg
    }
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=urlencode(data).encode('utf-8'))
    print(r.text)


def request():
    r = requests.post(f"{HOST}", headers=HEADERS, data=DATA)
    # print(f"{r.text}")

    trainList = r.json()['trainListMap']
    target_items = list(filter(train_filter_condition, trainList))
    if not target_items:
        notify("target_items is empty.\n뭔가 설정이 잘못 됨.")
    
    # print(list(target_items))
    satisfied_items = list(filter(is_satisfied, target_items))

    for item in satisfied_items:
        msg = f"[예약 가능]\n{departures}>{arrivals}\n{target_date}\n{item['dptTm'][:4]} > {item['arvTm'][:4]}"
        print(msg)
        notify(msg)
        

if __name__ == '__main__':
    while True:
        request()
        sleep(1.4)








# request
'''
POST /ara/selectListAra10007_n.do HTTP/1.1
Host: app.srail.or.kr
Connection: keep-alive
Content-Length: 230
Pragma: no-cache
Cache-Control: no-cache
sec-ch-ua-platform: "Android"
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Linux; Android 14; SM-S911N Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36SRT-APP-Android V.2.0.30
Accept: application/json, text/javascript, */*; q=0.01
sec-ch-ua: "Chromium";v="130", "Android WebView";v="130", "Not?A_Brand";v="99"
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
sec-ch-ua-mobile: ?1
Origin: https://app.srail.or.kr
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://app.srail.or.kr/ara/selectListAra10007_n.do?jobId=1101&jrnyTpCd=11&jrnyCnt=1&grpDv=0&rtnDv=0&stlbTrnClsfCd1=05&stndFlg=N&jrnySqno1=001&jrnySqno2=&trnGpCd1=109&trnGpCd2=&trnGpNm1=%EC%A0%84%EC%B2%B4&trnGpNm2=&dptRsStnCd1=0551&dptRsStnCd2=&dptRsStnCdNm1=%EC%88%98%EC%84%9C&dptRsStnCdNm2=&arvRsStnCd1=0036&arvRsStnCd2=&arvRsStnCdNm1=%EA%B4%91%EC%A3%BC%EC%86%A1%EC%A0%95&arvRsStnCdNm2=&dptDt1=20241109&dptTm1=000000&dptTm2=&arvDt1=&arvTm1=&dptDtTmNm1=2024%EB%85%84+11%EC%9B%94+9%EC%9D%BC%28%ED%86%A0%29&dptDtTmName1=%3Cspan+class%3D%22txt-act%22%3E00%EC%8B%9C%3C%2Fspan%3E%3Cspan%3E%EC%9D%B4%ED%9B%84%3C%2Fspan%3E&back_dptDt1=20241116&back_dptTm1=000000&back_dptDtTmNm1=2024%EB%85%84+11%EC%9B%94+9%EC%9D%BC%28%ED%86%A0%29&back_dptDtTmName1=%3Cspan+class%3D%22txt-act%22%3E19%EC%8B%9C%3C%2Fspan%3E%3Cspan%3E%EC%9D%B4%ED%9B%84%3C%2Fspan%3E&totPrnb=1&totPrnbNm=1%EB%AA%85&psgGridcnt=1&psgTpCd1=1&psgInfoPerPrnb1=1&psgTpCd2=&psgInfoPerPrnb2=0&psgTpCd3=&psgInfoPerPrnb3=0&psgTpCd4=&psgInfoPerPrnb4=0&psgTpCd5=&psgInfoPerPrnb5=0&infantCnt=0&psgTpCd6=&psgInfoPerPrnb6=0&smkSeatAttCd1=000&dirSeatAttCd1=009&locSeatAttCd1=000&rqSeatAttCd1=015&etcSeatAttCd1=000&seatAttNm1=%EC%9D%BC%EB%B0%98%2F%EA%B8%B0%EB%B3%B8&smkSeatAttCd2=000&dirSeatAttCd2=009&locSeatAttCd2=000&rqSeatAttCd2=015&etcSeatAttCd2=000&seatAttNm2=%EC%9D%BC%EB%B0%98%2F%EA%B8%B0%EB%B3%B8&go_baseDsXml=&go_seatDsXml=&seatNo1_1=&seatNo1_2=&seatNo1_3=&seatNo1_4=&seatNo1_5=&seatNo1_6=&seatNo1_7=&seatNo1_8=&seatNo1_9=&seatNo2_1=&seatNo2_2=&seatNo2_3=&seatNo2_4=&seatNo2_5=&seatNo2_6=&seatNo2_7=&seatNo2_8=&seatNo2_9=&scarGridcnt1=&scarGridcnt2=&trnNo1=&trnNo2=&runDt1=&runDt2=&scarNo1=&scarNo2=&psrmClCd1=&psrmClCd2=&seatAttCd=&dptStnConsOrdr1=&dptStnConsOrdr2=&arvStnConsOrdr1=&arvStnConsOrdr2=&dptStnRunOrdr1=&dptStnRunOrdr2=&arvStnRunOrdr1=&arvStnRunOrdr2=&choiceSeatCount=&pnrNo=&jrnySqno=&JRNYLIST_KEY=&arvDt=&arvRsStnCd=&arvTm=&dlayAcptFlg=&dptDt=&dptRsStnCd=&dptTm=000000&lumpStlTgtNo=&proyStlTgtFlg=&stlbTrnClsfCd=&totSeatNum=&trnGpCd=109&trnNo=&rcvdAmt=&tmpJobSqno1=&tmpJobSqno2=&dcntKndCd=&seatNo1=&seatNo2=&scarNo1=&scarNo2=&chtnDvCd=&type=page&typeNo=1&toKrailFlag=&mutMrkVrfCd=&actkey=0DDCF18DA4772FD8D4F15361FA07FE91E82F18CF2B7CCDB3814C77B08092B7D1818E1F0DC12F2E3683AD8862B4027843D10A0271802C903D129B5AD96BFE473A1CB26617D87CAABDD2E6E64F417DED7D96A9D5FEF277A253926FE94B0277D1F0C0F0773E7C9EFA090878424A20C20FDA332C312C352C30
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: srailSID=SRAIL_VJch0mQ3gf8nfHu; WMONID=jBDPV0aY0gy; wcCookieV2=211.234.205.230_T_138906_WC; deviceKey=E52DB8E2F7BB9CFE; gs_loginEmailNo=umbum7601@naver.com; srail_type8=N; srail_type10=rTGERyzDRtKWigTuQEhCXEMFQNBu4Acbf9yjy/Lq/+R78t+A/NTkMWTeZKkH2leJ1CMSD22BhkDTODpJKTVVzaUCc45sD0JdlUnxnW/r8UfGxo512nSLiJQqlzJ1HPrdSQMaUxQe6sMGpKn2QyMxn2QhhI0WdN/gVKmftZkARcs=; JSESSIONID_XEBEC=aa2Rc2rpYDSVAFalfG6LyT2a3IbsFlx8xayuBifJLqa1scmGvXiVDWl4AzcBbilI.YXBwL0FQUENPTjAzLTM=

chtnDvCd=1&dptDt=20241109&dptTm=000000&dptDt1=20241109&dptTm1=000000&dptRsStnCd=0551&arvRsStnCd=0036&stlbTrnClsfCd=05&trnGpCd=109&trnNo=&psgNum=1&seatAttCd=015&arriveTime=N&tkDptDt=&tkDptTm=&tkTrnNo=&tkTripChgFlg=&dlayTnumAplFlg=Y
'''

# response - r.json()['trainListMap'][0]
'''
{
    "etcRsvPsbCdNm": "-",
    "rcvdAmt": "00000000040900",
    "sprmRsvPsbStr": "매진",
    "trnOrdrNo": 9,
    "gnrmRsvPsbStr": "매진",
    "gnrmRsvPsbColor": "#ffffffff",
    "runTm": "0146",
    "sprmRsvPsbColor": "#ffffffff",
    "arvTm": "145500",
    "fresRsvPsbCdNm": null,
    "runDt": "20241109",
    "stlbDturDvCd": "",
    "ocurDlayTnum": 0,
    "dlaySaleFlg": "N",
    "seatAttCd": "015",
    "rcvdFare": "00000000018400",
    "arvStnConsOrdr": "000017",
    "sprmRsvPsbImg": "IMAGE::grd_WF_Soldout.png",
    "rsvWaitPsbCdNm": "매진",
    "chtnDvCd": "1",
    "rsvWaitPsbCd": " 0",
    "seatSelect": "",
    "dptStnRunOrdr": "000001",
    "stlbTrnClsfCd": "17",
    "trainDiscGenRt": "0000.00",
    "dptTm": "130900",
    "stmpRsvPsbFlgCd": "YY",
    "trnNstpLeadInfo": "",
    "arvDt": "20241109",
    "gnrmRsvPsbCdNm": "좌석매진",
    "gnrmRsvPsbImg": "IMAGE::grd_WF_Soldout.png",
    "trnGpCd": "300",
    "sprmRsvPsbCdNm": "좌석매진",
    "payTable": "",
    "dptRsStnCd": "0551",
    "ymsAplFlg": "Y",
    "fresOprCno": 0,
    "doReserv": "",
    "timeTable": "",
    "stndRsvPsbCdNm": "역발매중",
    "dptStnConsOrdr": "000001",
    "arvRsStnCd": "0036",
    "dptDt": "20241109",
    "trnNo": "659",
    "arvStnRunOrdr": "000006",
    "trnCpsCd5": "",
    "expnDptDlayTnum": "00000",
    "trnCpsCd3": "",
    "trnCpsCd4": "",
    "trnCpsCd1": "X",
    "trnCpsCd2": ""
}
'''