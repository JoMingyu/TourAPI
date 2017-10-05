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

    def get_tour_list(self):
        resp = json.loads(urlopen(self.tour_list_url.format(1)).read().decode('utf-8'))
        total_count = resp['response']['body']['totalCount']
        # Get total count

        resp = json.loads(urlopen(self.tour_list_url.format(total_count)).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data list

        for tour in data:
            tour['createdtime'] = str(tour['createdtime'])[:8]
            tour['modifiedtime'] = str(tour['modifiedtime'])[:8]
            # Manufacture

        return data

    def get_detail_common(self, content_id):
        resp = json.loads(urlopen(self.detail_common_url.format(str(content_id))).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data list

        data['homepage'] = re.findall('[\w\s]+', data['homepage'])[0]
        data['createdtime'] = str(data['createdtime'])[:8]
        data['modifiedtime'] = str(data['modifiedtime'])[:8]
        del data['contentid']
        # Manufacture

        return data

    def get_detail_intro(self, content_id):
        content_type_id = self.get_detail_common(content_id)['contenttypeid']
        resp = json.loads(urlopen(self.detail_intro_url.format(content_id, content_type_id)).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']

        data['infocenter'] = [infocenter.strip() for infocenter in data['infocenter'].split('\n <br /> \n')]
        del data['contentid']
        del data['contenttypeid']
        # Manufacture

        return resp['response']['body']['items']['item']

    def get_detail_images(self, content_id):
        resp = json.loads(urlopen(self.additional_images_url.format(content_id, 1)).read().decode('utf-8'))
        total_count = resp['response']['body']['totalCount']
        # Get total count

        resp = json.loads(urlopen(self.additional_images_url.format(content_id, total_count)).read().decode('utf-8'))
        print(resp)
        try:
            data = resp['response']['body']['items']['item']
            # Extract data list
            for img in data:
                del img['contentid']
                del img['serialnum']
                img['origin'] = img.pop('originimgurl')
                img['small'] = img.pop('smallimageurl')

            return data
        except TypeError:
            return None

if __name__ == '__main__':
    api = TourAPI(AreaCodes.DAEJEON, 'bb%2FPPi9Iy9rNdmIN7PIdb4doQ8PCwL725OFZndZ7DS%2FbP8%2Bzr9T3rpoD%2B083JYDwg5YJyi3HQ3UZ5%2Fp0e6ER8Q%3D%3D')
    print(api.get_tour_list())
    print(api.get_detail_images(1851001))
