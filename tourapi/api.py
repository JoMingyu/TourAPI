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
            'firstimage': ('img_big_url', None),
            'firstimage2': ('img_small_url', None)
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

        data['homepage'] = re.findall('http\w?://[\w|.]+', data.pop('homepage'))[0] if 'homepage' in data else None

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
            keychain = {
                'chkbabycarriage': ('baby_carriage', None),
                'chkcreditcard': ('credit_card', None),
                'chkpet': ('pet', None),
                'opendate': ('open_date', None),
                'restdate': ('rest_date', None),
                'usetime': ('use_time', None),
                'accomcount': ('capacity', None),
                'expguide': ('guide', None),
                'infocenter': ('info_center', None),
                'parking': ('parking', None),
                'expagerange': ('age_range', None),
                'useseason': ('season', None)
            }
            _dict_key_changer(data, keychain)

            data['cultural_heritage'] = data.pop('heritage1') == 1 if 'heritage1' in data else None
            data['natural_heritage'] = data.pop('heritage2') == 1 if 'heritage2' in data else None
            data['archival_heritage'] = data.pop('heritage3') == 1 if 'heritage3' in data else None
        elif content_type_id == 14:
            data['baby_carriage'] = data.pop('chkbabycarriageculture') if 'chkbabycarriageculture' in data else None
            data['credit_card'] = data.pop('chkcreditcardculture') if 'chkcreditcardculture' in data else None
            data['pet'] = data.pop('chkpetculture') if 'chkpetculture' in data else None
            data['rest_date'] = data.pop('restdateculture') if 'restdateculture' in data else None
            data['use_time'] = data.pop('usetimeculture') if 'usetimeculture' in data else None
            # 이용시간
            data['spend_time'] = data.pop('spendtime') if 'spendtime' in data else None
            # 관람 소요시간
            data['parking'] = data.pop('parkingculture') if 'parkingculture' in data else None
            data['parking_fee'] = data.pop('parkingfee') if 'parkingfee' in data else None
            data['use_fee'] = data.pop('usefee') if 'usefee' in data else None
            data['capacity'] = data.pop('accomcount') if 'accomcount' in data else None
            data['discount'] = data.pop('discount') if 'discount' in data else None
            data['scale'] = data.pop('scale') if 'scale' in data else None
            data['info_center'] = data.pop('infocenterculture') if 'infocenterculture' in data else None
        elif content_type_id == 15:
            data['age_limit'] = data.pop('agelimit') if 'agelimit' in data else None
            data['reservation_place'] = data.pop('bookingplace') if 'bookingplace' in data else None
            data['start_date'] = data.pop('eventstartdate') if 'eventstartdate' in data else None
            data['end_date'] = data.pop('eventenddate') if 'eventenddate' in data else None
            data['place'] = data.pop('eventplace') if 'eventplace' in data else None
            data['place_guide'] = data.pop('placeinfo') if 'placeinfo' in data else None
            data['festival_grade'] = data.pop('festivalgrade') if 'festivalgrade' in data else None
            data['spend_time'] = data.pop('spendtimefestival') if 'spendtimefestival' in data else None
            data['organizer'] = data.pop('sponsor1') if 'sponsor1' in data else None
            # 주최자
            data['host'] = data.pop('sponsor2') if 'sponsor2' in data else None
            # 주관자
            data['sub_event'] = data.pop('subevent') if 'subevent' in data else None
            data['use_fee'] = data.pop('usetimefestival') if 'usetimefestival' in data else None

            del data['eventhomepage']
        elif content_type_id == 25:
            data['distance'] = data.pop('distance') if 'distance' in data else None
            data['info_center'] = data.pop('infocentertourcourse') if 'infocentertourcourse' in data else None
            data['schedule'] = data.pop('schedule') if 'schedule' in data else None
            data['spend_time'] = data.pop('taketime') if 'taketime' in data else None
            data['theme'] = data.pop('theme') if 'theme' in data else None
        elif content_type_id == 28:
            data['baby_carriage'] = data.pop('chkbabycarriageleports') if 'chkbabycarriageleports' in data else None
            data['credit_card'] = data.pop('chkcreditcardleports') if 'chkcreditcardleports' in data else None
            data['pet'] = data.pop('chkpetleports') if 'chkpetleports' in data else None
            data['capacity'] = data.pop('accomcountleports') if 'accomcountleports' in data else None
            data['age_range'] = data.pop('expagerangeleports') if 'expagerangeleports' in data else None
            data['info_center'] = data.pop('infocenterleports') if 'infocenterleports' in data else None
            data['open_period'] = data.pop('openperiod') if 'openperiod' in data else None
            data['parking'] = data.pop('parkingleports') if 'parkingleports' in data else None
            data['parking_fee'] = data.pop('parkingfeeleports') if 'parkingfeeleports' in data else None
            data['reservation_info'] = data.pop('reservation') if 'reservation' in data else None
            data['rest_date'] = data.pop('restdateleports') if 'restdateleports' in data else None
            data['scale'] = data.pop('scaleleports') if 'scaleleports' in data else None
            data['use_time'] = data.pop('usetimeleports') if 'usetimeleports' in data else None
            data['use_fee'] = data.pop('use_fee') if 'use_fee' in data else None
        elif content_type_id == 32:
            data['capacity'] = data.pop('accomcountlodging') if 'accomcountlodging' in data else None
            data['checkin_time'] = data.pop('checkintime') if 'checkintime' in data else None
            data['checkout_time'] = data.pop('checkouttime') if 'checkouttime' in data else None
            data['benikia'] = data.pop('benikia') == 1 if 'benikia' in data else False
            data['cooking'] = data.pop('cooking') == 1if 'chkcooking' in data else False
            data['food_field'] = data.pop('foodplace') if 'foodplace' in data else None
            data['goodstay'] = data.pop('goodstay') == 1 if 'goodstay' in data else False
            data['korean_house'] = data.pop('hanok') == 1 if 'hanok' in data else False
            data['info_center'] = data.pop('info_center') if 'infocenterlodging' in data else None
            data['parking'] = data.pop('parkinglodging') if 'parkinglodging' in data else None
            data['pickup_service'] = data.pop('pickup') if 'pickup' in data else None
            data['reservation_info'] = data.pop('reservationlodging') if 'reservationlodging' in data else None
            data['room_type'] = data.pop('roomtype') if 'roomtype' in data else None
            data['scale'] = data.pop('scalelodging') if 'scalelodging' in data else None
            data['sub_facility'] = data.pop('subfacility') if 'subfacility' in data else None
            data['barbecue'] = data.pop('barbecue') == 1 if 'barbecue' in data else False
            data['beauty'] = data.pop('beauty') == 1 if 'beauty' in data else False
            data['beverage'] = data.pop('beverage') == 1 if 'beverage' in data else False
            data['bicycle'] = data.pop('bicycle') == 1 if 'bicycle' in data else False
            data['campfire'] = data.pop('campfire') == 1 if 'campfire' in data else False
            data['fitness'] = data.pop('fitness') == 1 if 'fitness' in data else False
            data['karaoke'] = data.pop('karaoke') == 1 if 'karaoke' in data else False
            data['public_bath'] = data.pop('publicpath') == 1 if 'publicbath' in data else False
            data['public_path'] = data.pop('publicpc') == 1 if 'publicpc' in data else False
            data['sauna'] = data.pop('sauna') == 1 if 'sauna' in data else False
            data['seminar'] = data.pop('seminar') == 1 if 'seminar' in data else False
            data['sports'] = data.pop('sports') == 1 if 'sports' in data else False
        elif content_type_id == 38:
            data['baby_carriage'] = data.pop('chkbabycarriageshopping') if 'chkbabycarriageshopping' in data else None
            data['credit_card'] = data.pop('chkcreditcardshopping') if 'chkcreditcardshopping' in data else None
            data['pet'] = data.pop('chkpetshopping') if 'chkpetshopping' in data else None
            data['fair_day'] = data.pop('fairday') if 'fairday' in data else None
            data['open_date'] = data.pop('opendateshopping') if 'opendateshopping' in data else None
            data['open_time']
        elif content_type_id == 39:
            pass

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
    # print(api.get_detail_intro(1928589))
    for tour in api.get_tour_list():
        if tour['content_type_id'] == 12:
            print(api.get_detail_intro(tour['content_id']))
