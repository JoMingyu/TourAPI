from urllib.request import urlopen
import json
import re

_API_ENDPOINT = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService'
_PARAMS = 'areaCode={0}&ServiceKey={1}&MobileOS={2}&MobileApp={3}&_type=json'

_URLS = {
    'tour_list': _API_ENDPOINT + '/areaBasedList?' + _PARAMS,
    'detail_common': _API_ENDPOINT + '/detailCommon?defaultYN=Y&overviewYN=Y&' + _PARAMS,
    'detail_intro': _API_ENDPOINT + '/detailIntro?' + _PARAMS,
    'additional_images': _API_ENDPOINT + '/detailImage?imageYN=Y&' + _PARAMS
}


class AreaCodes:
    SEOUL = 1
    INCHEON = 2
    DAEJEON = 3
    DAEGU = 4
    GWANGJU = 5
    BUSAN = 6
    ULSAN = 7
    SEJONG = 8
    GYEONGGI = 31
    KANGWON = 32
    CHUNGBUK = 33
    CHUNGNAM = 34
    GYUNGBUK = 35
    GYUNGNAM = 36
    JEONBUK = 37
    JEONNAM = 38
    JEJU = 39
