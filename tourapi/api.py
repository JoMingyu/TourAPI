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


def _dict_key_changer(_dict, keychains):
    # _dict - 타겟 딕셔너리
    for k, v in keychains.items():
        # k - 바꿔야 할 legacy key
        # v - (바꿀 key, default 값)
        _dict[v[0]] = _dict.pop(k) if k in _dict else v[1]
        # legacy key가 딕셔너리에 있으면 pop, 없으면 default 값


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
        """
        Inquire all tour list

        :rtype: list
        """
        resp = json.loads(urlopen(self.tour_list_url.format(1)).read().decode('utf-8'))
        total_count = resp['response']['body']['totalCount']
        # Get total count

        resp = json.loads(urlopen(self.tour_list_url.format(total_count)).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data list

        keychain = {
            'contentid': ('content_id', None),
            'contenttypeid': ('content_type_id', None),
            'title': ('title', None),
            'addr1': ('address', None),
            'zipcode': ('zipcode', None),
            'sigungucode': ('municipality', None),
            'mapx': ('x', None),
            'mapy': ('y', None),
            'cat1': ('main_category', None),
            'cat2': ('middle_category', None),
            'cat3': ('small_category', None),
            'readcount': ('views', 0),
            'tel': ('tel', None),
            'firstimage': ('image', None),
        }

        for tour in data:
            _dict_key_changer(tour, keychain)

            tour['creation_date'] = str(tour.pop('createdtime'))[:8] if 'createdtime' in tour else None
            tour['modified_date'] = str(tour.pop('modifiedtime'))[:8] if 'modifiedtime' in tour else None

            tour.pop('areacode') if 'areacode' in tour else None
            tour.pop('addr2') if 'addr2' in tour else None
            tour.pop('mlevel') if 'mlevel' in tour else None
            # Manufacture

        return data

    def get_detail_common(self, content_id):
        """
        Inquire common detail data

        :param content_id: Content ID to inquire
        :type content_id: str

        :rtype: dict
        """
        resp = json.loads(urlopen(self.detail_common_url.format(str(content_id))).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data

        keychain = {
            'contenttypeid': ('content_type_id', None),
            'overview': ('overview', None),
            'tel': ('tel', None),
            'telname': ('tel_owner', None),
            'booktour': ('in_book', 0)
        }
        _dict_key_changer(data, keychain)

        try:
            data['homepage'] = re.findall('http\w?://[\w|.]+', data.pop('homepage'))[0] if 'homepage' in data else None
        except IndexError:
            data['homepage'] = None

        data.pop('contentid') if 'contentid' in data else None
        data.pop('title') if 'title' in data else None
        data.pop('createdtime') if 'createdtime' in data else None
        data.pop('modifiedtime') if 'modifiedtime' in data else None
        # Manufacture

        return data

    def get_detail_intro(self, content_id):
        """
        Inquire detail introduction

        :param content_id: Content ID to inquire
        :type content_id: str

        :rtype: dict
        """
        content_type_id = self.get_detail_common(content_id)['content_type_id']
        # Get content type id

        resp = json.loads(urlopen(self.detail_intro_url.format(content_id, content_type_id)).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data

        del data['contentid']
        del data['contenttypeid']

        if content_type_id == 12:
            # 관광지
            keychain = {
                'accomcount': ('capacity', None),
                'chkbabycarriage': ('baby_carriage', None),
                'chkcreditcard': ('credit_card', None),
                'chkpet': ('pet', None),
                'expagerange': ('age_range', None),
                'expguide': ('guide', None),
                'infocenter': ('info_center', None),
                'opendate': ('open_date', None),
                'parking': ('parking', None),
                'restdate': ('rest_date', None),
                'useseason': ('season', None),
                'usetime': ('use_time', None)
            }
            _dict_key_changer(data, keychain)

            data['cultural_heritage'] = data.pop('heritage1') == 1 if 'heritage1' in data else None
            data['natural_heritage'] = data.pop('heritage2') == 1 if 'heritage2' in data else None
            data['archival_heritage'] = data.pop('heritage3') == 1 if 'heritage3' in data else None
        elif content_type_id == 14:
            # 문화시설
            keychain = {
                'accomcountculture': ('capacity', None),
                'chkbabycarriageculture': ('baby_carriage', None),
                'chkcreditcardculture': ('credit_card', None),
                'chkpetculture': ('pet', None),
                'discountinfo': ('discount_info', None),
                'infocenterculture': ('info_center', None),
                'parkingculture': ('parking', None),
                'parkingfee': ('parking_fee', None),
                'restdateculture': ('rest_date', None),
                'usefee': ('use_fee', None),
                'usetimeculture': ('use_time', None),
                # 이용시간
                'scale': ('scale', None),
                'spendtime': ('spend_time', None)
                # 관람 소요시간
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 15:
            # 축제/공연/행사
            keychain = {
                'agelimit': ('age_limit', None),
                'bookingplace': ('reservation_place', None),
                'eventstartdate': ('start_date', None),
                'eventenddate': ('end_date', None),
                'eventplace': ('place', None),
                'festivalgrade': ('festival_grade', None),
                'placeinfo': ('place_guide', None),
                'spendtimefestival': ('spend_time', None),
                'sponsor1': ('organizer', None),
                'sponsor2': ('host', None),
                'subevent': ('sub_event', None),
                'usetimefestival': ('use_fee', None)
            }
            _dict_key_changer(data, keychain)

            data.pop('eventhomepage') if 'eventhomepage' in data else None
        elif content_type_id == 25:
            # 여행코스
            keychain = {
                'distance': ('distance', None),
                'infocentertourcourse': ('info_center', None),
                'schedule': ('schedule', None),
                'taketime': ('spend_time', None),
                'theme': ('theme', None)
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 28:
            # 레포츠
            keychain = {
                'accomcountleports': ('capacity', None),
                'chkbabycarriageleports': ('baby_carriage', None),
                'chkcreditcardleports': ('credit_card', None),
                'chkpetleports': ('pet', None),
                'expagerangeleports': ('age_range', None),
                'infocenterleports': ('info_center', None),
                'openperiod': ('open_period', None),
                'parkingleports': ('parking', None),
                'parkingfeeleports': ('parking_fee', None),
                'reservation': ('reservation_info', None),
                'restdateleports': ('rest_date', None),
                'scaleleports': ('scale', None),
                'usetimeleports': ('use_time', None),
                'usefeeleports': ('use_fee', None),
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 32:
            # 숙박
            keychain = {
                'accomcountlodging': ('capacity', None),
                'checkintime': ('checkin_time', None),
                'checkouttime': ('checkout_time', None),
                'foodplace': ('food_field', None),
                'infocenterlodging': ('info_center', None),
                'parkinglodging': ('parking', None),
                'pickup': ('pickup_service', None),
                'reservationlodging': ('reservation_info', None),
                'roomtype': ('room_type', None),
                'scalelodging': ('scale', None),
                'subfacility': ('sub_facility', None)
            }
            _dict_key_changer(data, keychain)

            data['benikia'] = data.pop('benikia') == 1 if 'benikia' in data else False
            data['cooking'] = data.pop('chkcooking') == 1 if 'chkcooking' in data else False
            data['goodstay'] = data.pop('goodstay') == 1 if 'goodstay' in data else False
            data['korean_house'] = data.pop('hanok') == 1 if 'hanok' in data else False
            data['barbecue'] = data.pop('barbecue') == 1 if 'barbecue' in data else False
            data['beauty'] = data.pop('beauty') == 1 if 'beauty' in data else False
            data['beverage'] = data.pop('beverage') == 1 if 'beverage' in data else False
            data['bicycle'] = data.pop('bicycle') == 1 if 'bicycle' in data else False
            data['campfire'] = data.pop('campfire') == 1 if 'campfire' in data else False
            data['fitness'] = data.pop('fitness') == 1 if 'fitness' in data else False
            data['karaoke'] = data.pop('karaoke') == 1 if 'karaoke' in data else False
            data['public_bath'] = data.pop('publicbath') == 1 if 'publicbath' in data else False
            data['public_pc'] = data.pop('publicpc') == 1 if 'publicpc' in data else False
            data['sauna'] = data.pop('sauna') == 1 if 'sauna' in data else False
            data['seminar'] = data.pop('seminar') == 1 if 'seminar' in data else False
            data['sports'] = data.pop('sports') == 1 if 'sports' in data else False
        elif content_type_id == 38:
            # 쇼핑
            keychain = {
                'chkbabycarriageshopping': ('baby_carriage', None),
                'chkcreditcardshopping': ('credit_card', None),
                'chkpetshopping': ('pet', None),
                'fairday': ('fair_day', None),
                'infocentershopping': ('info_center', None),
                'opendateshopping': ('open_date', None),
                'opentime': ('use_time', None),
                'parkingshopping': ('parking', None),
                'restdateshopping': ('rest_date', None),
                'restroom': ('restroom_info', None),
                'saleitem': ('sale_item', None),
                'saleitemcost': ('sale_item_cost', None),
                'scaleshopping': ('scale', None),
                'shopguide': ('guide', None)
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 39:
            # 음식
            keychain = {
                'chkcreditcardfood': ('credit_card', None),
                'discountinfofodd': ('discount_info', None),
                'firstmenu': ('rep_menu', None),
                'infocenterfood': ('info_center', None),
                'kidsfacility': ('kids_facility', None),
                'opendatefood': ('open_date', None),
                'opentimefood': ('open_time', None),
                'packing': ('packing', None),
                'parkingfood': ('parking', None),
                'reservationfood': ('reservation_info', None),
                'restdatefood': ('rest_date', None),
                'scalefood': ('scale', None),
                'seat': ('seat', None),
                'smoking': ('smoking', None),
                'treatmenu': ('treat_menus', None)
            }
            _dict_key_changer(data, keychain)

            data['kids_facility'] = data.pop('kidsfacility') == 1 if 'kidsfacility' in data else False

        return data

    def get_detail_images(self, content_id):
        """
        Inquire detail images

        :param content_id: Content ID to inquire
        :type content_id: str

        :rtype: list
        """
        resp = json.loads(urlopen(self.additional_images_url.format(content_id, 1)).read().decode('utf-8'))
        total_count = resp['response']['body']['totalCount']
        # Get total count

        resp = json.loads(urlopen(self.additional_images_url.format(content_id, total_count)).read().decode('utf-8'))
        try:
            data = resp['response']['body']['items']['item']
            # Extract data list
            for img in data:
                del img['contentid']
                del img['serialnum']
                img['origin'] = img.pop('originimgurl')
                img['small'] = img.pop('smallimageurl')
                # Manufacture

            return data
        except TypeError:
            return None

if __name__ == '__main__':
    api = TourAPI(AreaCodes.DAEJEON, 'bb%2FPPi9Iy9rNdmIN7PIdb4doQ8PCwL725OFZndZ7DS%2FbP8%2Bzr9T3rpoD%2B083JYDwg5YJyi3HQ3UZ5%2Fp0e6ER8Q%3D%3D')
    print(api.get_tour_list())
    for tour in api.get_tour_list():
        print(api.get_detail_common(tour['content_id']))
        print(api.get_detail_intro(tour['content_id']))
        print(api.get_detail_images(tour['content_id']))
