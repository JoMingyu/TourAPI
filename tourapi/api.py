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


class TourAPI:
    def __init__(self, area_code, service_key, mobile_os='ETC', app_name='PlanB'):
        """
        :param area_code: Area code to initialize API
        :param service_key: Service code from data.go.kr
        :param mobile_os: Application os(AND, IOS, ETC)
        :param app_name: Service name
        :type area_code: int
        :type service_key: str
        :type mobile_os: str
        :type app_name: str
        """
        self.tour_list_url = _URLS['tour_list'].format(area_code, service_key, mobile_os, app_name) + '&numOfRows={0}'
        self.detail_common_url = _URLS['detail_common'].format(area_code, service_key, mobile_os, app_name) + '&contentId={0}'
        self.detail_intro_url = _URLS['detail_intro'].format(area_code, service_key, mobile_os, app_name) + '&contentId={0}&contentTypeId={1}'
        self.additional_images_url = _URLS['additional_images'].format(area_code, service_key, mobile_os, app_name) + '&contentId={0}&numOfRows={1}'
