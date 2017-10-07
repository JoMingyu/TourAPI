# TourAPI
한국관광공사의 공공데이터 사업인 TourAPI의 사용성을 개선하기 위한 라이브러리입니다.

## 공공데이터를 직접 사용하며 겪었던 TourAPI의 문제
1. 문서에 명시되어 있더라도, 데이터가 없으면 반환되는 JSON 데이터에 key조차 오지 않는 경우  
ex) 어떤 여행지에서는 'infocenter'라는 key로 전화번호가 오는데, 또 다른 여행지에서는 'infocenter'라는 key 자체가 없음.  

2. JSON 데이터의 key 네이밍이 조잡함  
ex) 시군구코드 : sigungucode, 문화재 여부 : heritage1/2/3  
ex) 주최자 : sponsor1, 주관자 : sponsor2  
ex) 한옥 여부 : hanok

3. JSON 데이터의 key 네이밍에 일관성이 없음  
ex1) '관광지' 타입에서의 유모차 대여 여부 :  chkbabycarriage  
ex1) '문화시설' 타입에서의 유모차 대여 여부 : chkbabycarriage**culture**  
ex1) '쇼핑' 타입에서의 유모차 대여 여부 : chkbabycarriage**shopping**  
ex2) '문화시설' 타입에서의 관람 소요 시간 : spendtime  
ex2) '축제/공연/행사' 타입에서의 소요 시간 : spendtime**festival**

4. 뭔가 이상한데?  
'축제/공연/행사' 타입의 이용요금 : use**time**festival

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
[{'content_id': 1939307, 'content_type_id': 39, 'title': '김삿갓', 'address': '대전광역시 유성구 신성로 139', 'zipcode': 34109, 'municipality': 4, 'x': '127.3528002580', 'y': 36.3949238503, 'main_category': 'A05', 'middle_category': 'A0502', 'small_category': 'A05020100', 'views': 3962, 'tel': '042-863-6076~7', 'img_big_url': None, 'img_small_url': None, 'creation_date': '20140805', 'modified_date': '20170215'}, {'content_id': 1126556, 'content_type_id': 12, 'title': '김정선생묘소일원', 'address': '대전광역시 동구 회남로 117', 'zipcode': 34501, 'municipality': 2, 'x': 127.4994798085, 'y': 36.3580751206, 'main_category': 'A02', 'middle_category': 'A0201', 'small_category': 'A02010700', 'views': 34090, 'tel': None, 'img_big_url': 'http://tong.visitkorea.or.kr/cms/resource/32/1585532_image2_1.jpg', 'img_small_url': 'http://tong.visitkorea.or.kr/cms/resource/32/1585532_image3_1.jpg', 'creation_date': '20101111', 'modified_date': '20160302'}, ...]

#### get_detail_common(content_id)
모든 여행지 종류가 공통적으로 가지고 있는 세부 정보를 조회합니다.
~~~
print(api.get_detail_common(1928589))
~~~
{'content_type_id': 38, 'overview': '대전광역시 중구에 위치한 갤러리아백화점 동백점은 2000년 7월에 처음 오픈했다. 고급 백화점으로 그 브랜드 이미지를 확고히 하고 있을 뿐 아니라 국내외 유명 브랜드와 패션 잡화, 생활용품에 이르기까지 다양한 품목을 갖추고 있다. <br>', 'tel': '042-480-5000', 'tel_owner': '갤러리아 백화점 (타임월드점)', 'in_book': 0, 'homepage': 'http://branch.galleria.co.kr'}

#### get_detail_intro(content_id)
여행지의 세부 정보를 조회합니다. 여행지 type마다 리턴이 다릅니다.
~~~
print(api.get_detail_intro(1928589))
~~~
{'baby_carriage': '없음', 'credit_card': '가능', 'pet': '불가', 'fair_day': None, 'info_center': '042-480-5000', 'open_date': '2000년 7월 7일 전관 리뉴얼(Renewal)을 거쳐 갤러리아 백화점 동백점으로 그랜드 오픈', 'open_time': '10:30 ~ 20:00', 'parking': '주차가능', 'rest_date': '영업계획에 의해 휴무', 'restroom_info': '화장실완비', 'sale_item': '종합', 'sale_item_cost': '', 'scale': '매장면적 145,345㎡ (4,642평)', 'guide': ''}

#### get_detail_images(content_id)
여행지의 추가 이미지를 조회합니다.
~~~
print(api.get_detail_images(1928589))
~~~
[{'origin': 'http://tong.visitkorea.or.kr/cms/resource/95/1023895_image2_1.jpg', 'small': 'http://tong.visitkorea.or.kr/cms/resource/95/1023895_image3_1.jpg'},  
{'origin': 'http://tong.visitkorea.or.kr/cms/resource/97/1023897_image2_1.jpg', 'small': 'http://tong.visitkorea.or.kr/cms/resource/97/1023897_image3_1.jpg'},  
{'origin': 'http://tong.visitkorea.or.kr/cms/resource/98/1023898_image2_1.jpg', 'small': 'http://tong.visitkorea.or.kr/cms/resource/98/1023898_image3_1.jpg'}]
