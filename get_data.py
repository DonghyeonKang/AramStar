from bs4 import BeautifulSoup   # selenium으로 스크래핑한 것을 1차 가공
from selenium import webdriver  # google webdriver를 사용할거임
from pyvirtualdisplay import Display # 가상 디스플레이
import subprocess   # OS 명령어 연동

display = Display(visible=0, size=(1920, 1080))
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
path='/home/opc/arambyeol/chromedriver'
driver = webdriver.Chrome(path, chrome_options=chrome_options)
driver.get('https://www.gnu.ac.kr/dorm/ad/fm/foodmenu/selectFoodMenuView.do') # 스크래핑할 동적 웹사이트 주소
html = driver.page_source   # 드라이버로 긁어온 정보를 html에 담음
driver.close()
display.stop()
subprocess.call("pkill -9 chrome", shell=True) # chrome driver 제대로 안꺼지면 꺼야함
soup = BeautifulSoup(html, 'html.parser') # Beautifulsoup로 1차 가공
#br태그를 공백문자로 바꾸어 준다.
for elem in soup.find_all(["br"]):
    elem.append('\n')

# days : 날짜 및 요일, morning : 아침, lunch : 점심, dinner : 저녁
days = soup.select_one('#detailForm > div > table > thead > tr').text.strip().replace(" ", "").split('\n')      # NoneType 이면 IP 차단 되었을 가능성 있음
morning = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(1)').text.strip().split('\n')
lunch = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(2)').text.strip().split('\n')
dinner = soup.select_one('#detailForm > div > table > tbody > tr:nth-child(3)').text.strip().split('\n')
def first_index_del(arg, repeat=1):   # 첫번째 인덱스를 삭제. ('아침', '점심', '저녁')
        for i in range(repeat):
            del arg[0]

def double_quorts_del(arg): # 각각의 인덱스 속 쌍따옴표를 찾아서 모두 삭제.
        search = '"'
        for i, word in enumerate(arg):
            arg[i] = word.strip() # 공백도 덤으로 삭제!
            if search in word:
               arg[i] = word.strip(search).strip() # 쌍따옴표 제거하고 공백 제거
        return arg


first_index_del(days)
if len(morning) > 1:
    first_index_del(morning,3)
else:
    first_index_del(morning,1)

if len(lunch) > 1:
    first_index_del(lunch,3)
else:
    first_index_del(lunch,1)

if len(dinner) > 1:
    first_index_del(dinner,3)
else:
    first_index_del(dinner,1)

double_quorts_del(morning)
double_quorts_del(lunch)
double_quorts_del(dinner)

    # 메뉴 데이터를 가공할거임. 2차 가공. 요일 별로 나눔.
def split_menu_data(args):
        count = 0
        day=[]
        day.append([])
        day_count = 0   # 요일 카운트 [요일][메뉴]

        for element in args:
            if count >= 4 and element != '' in element:  # 공백 개수가 연속으로 4 이상이고, 5번째가 공백이 아니라면
                day.append([])  # 요일 바뀜
                day_count += 1  # 요일 바꾸기
                count = 0   # 공백 개수 초기화
        
            if element == '': # 공백 인덱스면
                count += 1  # 공백 개수를 세고
            else:
                day[day_count].append(element)
                count = 0   # 공백 개수 초기화
        return day

def data_blocking(args):
    data = []
    blockingList = ["공지", "어플연동시", "당일 메뉴 오류가 빈번하게 발생합니다. 학생생활관 홈페이지에서 메뉴를 확인해주세요"]
    for i in args:
        if i not in blockingList:
            data.append(i)
    return data

morning = data_blocking(morning)
lunch = data_blocking(lunch)
dinner = data_blocking(dinner)

day_mornings = split_menu_data(morning)
day_lunchs = split_menu_data(lunch)
day_dinners = split_menu_data(dinner)