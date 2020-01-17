# #-*- coding : utf-8
# from flask import Flask, make_response, request
# import requests
# import pprint
#
# app = Flask(__name__)
# #웹 서버 주소 설정, '/aaa'설정시 -> 'http://127/0/0/1"5001/aaa' 로 서버 접속
# @app.route('/', methods=['POST', 'GET'])
# def process_webhook():
#
#     request_json = request.json
#
#     query = request_json['queryResult']
#     query_outputContexts = request_json['queryResult']['parameters']['book']
#     #인증 정보
#     client_id = ""
#     client_secret = ""
#
#     #기본 url 정보
#     url = "https://openapi.naver.com/v1/search/book.json"
#     #url호출 시 전달할 요청 변수 정보
#     params = {"query":query,
#               "display" : 3,
#               "sort":"count"}
#     #requests 라이브러리를 이용한 책 검색 api호출
#     #get방식으로 호출(url)/요청변수 전달(params)/인증 정보 및 인코딩 정보 전달(header)
#     response = requests.get(url=url, params=params, headers={"X-Naver-Client-Id":client_id,
#                                                              "X-Naver-Client-Secret":client_secret,
#                                                              "Content-Type":"application/json; charset=utf-8"})
#     #호출 처리 상태 정보 recode 변수에 할당
#     rescode = response.status_code
#
#     if(rescode == 200):
#         #호출 처리 상태가 정상 일 경우 리턴 받은 책 조회 정보 출력
#         pprint.pprint(response.json())
#         data = response.json()
#     else:
#         print("ErrorCode:", rescode)
#     item_list = data["items"]
#     pprint.pprint(item_list)
#
#     #Dialogflow로 응답되는 최종 문자열 데이터 구성
#     book_list = ""
#     for item in item_list :
#         book_list += item["title"]
#         book_list += " "
#
#     #Dialogflow로 응답되는 최종 데이터 확인
#     print(book_list)
#     return {"fullfillmentText": book_list}
#
#     # t = "메뉴:{menu}{beverage}, 수량:{sooryang}, 주소:{jooso}"
#     # print(t.format(menu=query_outputContexts['pizza_menu'], sooryang=query_outputContexts['number'],
#     #                                                     jooso=query_outputContexts['address'], beverage=query_ouputContexts['beverage']))
#     # print("주문 정보 :" + "주소("+query_address+")"+"사이즈("+query_size+")"+"색상("+query_color+")")
#     # #전체 json데이터 출력
#     # #pprint.pprint(body)
#     # print("\n\n\n")
#
# def index():
#     return "Hello World!"
#
# if __name__ == '__main__':
#     app.run(debug=True, port='5000')#default portnumber : 5000

from flask import Flask, request
import pprint
import requests
import re
from bs4 import BeautifulSoup
app = Flask(__name__)

main_url = 'https://programmers.co.kr/learn/challenges'
page = requests.get(main_url)
soup = BeautifulSoup(page.content, 'lxml')
base_url = 'https://programmers.co.kr'
all_divs = soup.find_all('div', class_='card card-preparation')
all_links = [base_url + div.a['href'] for div in all_divs]
all_catagories = soup.find_all('h4', class_='card-title')
all_catagories_string =[categories_name for categories_name in all_catagories]

data1 = []
link_data1 = []

def remove(content):
    clearnr = re.compile('<.*?>')
    cleantext = re.sub(clearnr, '', content)
    return cleantext

for contents in all_catagories_string:
    data1 += [remove(str(contents))]
for contents in all_links:
    link_data1 += [str(contents)]


@app.route('/webhook', methods=['GET', 'POST'])
def process_webhook():
    request_json = request.json
    # naver-book 인텐트 중 book 파라미터 데이터 추출
    query = request_json["queryResult"]["parameters"]["catagory"]

    #rjsgh1232
    #query1 = request_json["queryResult"]["parameters"]["level"]
    #dialogflow 고치기
    # 인증 정보
    client_id = "6xSK3DafLlDE1knfqjw9"
    client_secret = "VXTFOkwlO0"

    # 기본 url 정보
    url = "https://openapi.naver.com/v1/search/book.json"

    # url 호출 시 전달할 요청 변수 정보
    params = {"query": query,
              "display": 3,
              "sort": "count"}

    # requests 라이브러리를 이용한 책 검색 api 호출
    # get 방식으로 호출(url)/ 요청 변수 전달(params)/ 인증 정보 및 인코딩 정보 전달(header)
    response = requests.get(url=url, params=params,
                            headers={"X-Naver-Client-Id": client_id,
                                     "X-Naver-Client-Secret": client_secret,
                                     "Content-Type": "application/json; charset=utf-8"})
    # 호출 처리 상태 정보 recode 변수에 할당
    rescode = response.status_code

    if (rescode == 200):
        # 호출 처리 상태가 정상(200) 일 경우리턴 받은 책 조회 정보 출력
        #pprint.pprint(response.json())
        data = response.json()

    else:
        print("Error Code:", rescode)

    # Naver 책 검색 API 응답 중 실제 책 아이템 데이터 추출 및 출력
    item_list = data["items"]
    pprint.pprint(item_list)
    def remove_tag(content):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', content)
        return cleantext
    # Dialogflow로 응답되는 최종 문자열 데이터 구성
    book_list = ""
    n = 1
    for item in item_list:
        #book_list += remove_tag(item["title"])
        #print(str(n)+". "+remove_tag(item['title']))
        book_list += str(n)+". "+remove_tag(item['title'])
        book_list += "\n"
        n+=1
    #print(type(book_list))

    # Dialogflow로 응답되는 최종 데이터 확인
    if (query == "해시"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[0]}
    elif (query == "스택/큐"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[1]}
    elif (query == "힙"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[2]}
    elif (query == "정렬"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[3]}
    elif (query == "완전탐색"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[4]}
    elif (query == "탐욕법"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[5]}
    elif (query == "동적계획법"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[6]}
    elif (query == "깊이너비우선탐색"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[7]}
    elif (query == "이분탐색"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[8]}
    elif (query == "그래프"):
        return {"fulfillmentText": "적합한 "+'"'+query+'"'+"문제 추천해드릴게요.\n"+link_data1[9]}

    return {"fulfillmentText": data1}


if __name__ == '__main__':
    app.run(debug=True)