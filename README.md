# TourAPI
한국관광공사의 공공데이터 사업인 TourAPI의 사용성을 개선하기 위한 라이브러리입니다.

현재 TourAPI는 문서에 명시되어 있더라도 데이터가 아예 오지 않거나, 웹 태그들(br 등)이 조잡하게 붙어있는 등의 문제가 많습니다. version 1.0이 릴리즈되는 시점에 라이브러리 단에서 모두 해결토록 하겠습니다.

## How to use
TourAPI 서비스 키가 필요합니다. 공공데이터포털에서 '국문 관광정보 서비스'에 개발계정을 신청한 후 서비스 키를 확보하시기 바랍니다.

https://data.go.kr
### PyPI
~~~
pip install tourapi
~~~

~~~
from coinapi import TourAPI, AreaCodes
api = TourAPI(area_code=AreaCodes.DAEJEON, service_key='bb%2FPPi9Iy...', mobile_os='AND', app_name='Test')
~~~
#### get_tour_list
해당 area에 있는 모든 여행지를 불러옵니다.
~~~
print(api.get_tour_list())
~~~
[{'addr1': '대전광역시 유성구 신성로84번길 49', 'addr2': '(신성동)', 'areacode': 3, 'cat1': 'A05', 'cat2': 'A0502', 'cat3': 'A05020100', 'contentid': 1928589, 'contenttypeid': 39, 'createdtime': '20140627', 'mapx': 127.3512699993, 'mapy': 36.3890411631, 'mlevel': 6, 'modifiedtime': '20161205', 'readcount': 3088, 'sigungucode': 4, 'tel': '042-862-9288', 'title': '가나샤브샤브', 'zipcode': 34116},  
{'addr1': '대전광역시 유성구 대덕대로 588', 'addr2': '(도룡동)', 'areacode': 3, 'cat1': 'A05', 'cat2': 'A0502', 'cat3': 'A05020500', 'contentid': 250577, 'contenttypeid': 39, 'createdtime': '20071023', 'mapx': 127.3788787365, 'mapy': 36.3854587295, 'mlevel': 4, 'modifiedtime': '20160831', 'readcount': 31802, 'sigungucode': 4, 'tel': '042-861-7557', 'title': '가남지', 'zipcode': 34121}, ...]

#### get_detail_common(content_id)
모든 여행지 종류가 공통적으로 가지고 있는 세부 정보를 조회합니다.
~~~
print(api.get_detail_common(1928589))
~~~
{'contenttypeid': 39, 'createdtime': '20140627', 'modifiedtime': '20161205', 'overview': '[대전광역시 유성구 신성동에 있는 샤브샤브 전문점 가나샤브샤브] 샤브샤브 전문 음식점 가나샤브샤브의 한우암소 생등심 샤브샤브는 무, 양파, 다시마 등 10여 가지 재료를 끓여 낸 육수를 이용해 신선한 야채와 버섯, 우리 밀을 밀어 직접 뽑아낸 국수의 맛이 일품이다. 담백하고 깔끔한 맛의 영양죽도 가나샤브샤브의 특미 중 하나이다.', 'tel': '042-862-9288', 'telname': '가나샤브샤브', 'title': '가나샤브샤브'}

#### get_detail_intro(content_id)
여행지의 세부 정보를 조회합니다. 여행지 type마다 리턴이 다릅니다.
~~~
print(api.get_detail_intro(1928589))
~~~
{'chkcreditcardfood': '가능', 'firstmenu': '한우암소고기, 생등심 샤브샤브', 'infocenterfood': '042-862-9288', 'kidsfacility': 0, 'opentimefood': '점심 11:30 ~ 14:30 저녁 17:30 ~ 21:00 * 매주 일요일은 저녁만 운영', 'parkingfood': '가게 인근 주차', 'reservationfood': '전화 예약 가능 (042-862-9288)', 'restdatefood': '토요일', 'smoking': '모두 금연석', 'treatmenu': '샤브샤브 / 한우탕 / 한우수육 / 한우암소구이'}
