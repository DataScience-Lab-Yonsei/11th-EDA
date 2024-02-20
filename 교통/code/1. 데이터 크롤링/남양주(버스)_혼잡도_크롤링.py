from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import random
import os
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.keys import Keys

# 초기 설정!!
# --------------------------------------------------------------------------------------------------------------------#
# 1) 원하는 시 선택 : 원하는 시에 맞는 value 쓰기(문자열로)
# 남양주 : '41360' / 수원 : '41117_41111_41113_41110_41115' /
# 고양 : '41280_41285_41287_41281' / 용인 : '41460_41463_41461_41465'
city = '41360'

# 2) month 선택 -> 이걸 for문으로 돌릴까 하는데 월별로 노선이 살짝 다른게 걱정돼서 수동으로 두었습니다.
month_list = [1, 5, 7, 11]
month = 11 # 이 값을 수정할 것!!

# 3) bus List 바꿀 것!! P버스는 없으면 지우면 됨!
# 총 61개
bus = ['M2316', 'M2323', 'M2341', 'M2344', 'M2352', 'M2353', '11', '100', '105', '105-1', # 10개
       '1000', '1001', '1003', '1006', '1100', '1200', '1660', '1670', '1700', '2000', # 10개
       '2000-1', '8001', '8002', '8012', '1000-1', '1200-1', '1330-2', '1330-3', '1330-44', '1403', # 10개
       '1670-1', '8002-1', '3006', '7001', '7000', '7002', '7007', '8005', '8109', '8401', '8409', # 11개
       'G1200', 'G1300', 'G1300N', 'G6000', 'G6000N', 'G6100', 'G6100N', 'G9311'] # 8개

# 출근, 퇴근 2개씩 존재(P버스는 다른 버스들처럼 P9701(출근) 이렇게 검색을 하면 안 나와서 그냥 전체선택 하는 게 최선!
# 만약 P버스가 출,퇴근 합쳐서 10개를 넘어가면 time.sleep(15) 안의 시간을 적절히 수정해서 쉬고 있을 때 후다닥 2페이지 전체선택을 하면 됨.
P_bus = ['P9701','P9401', 'P9402 ', 'P9404', 'P9601', 'P9602']


# 4) 젤 처음 사이트에서 다운로드 받을 때 경로 알려주기
# 처음 다운로드 받는 곳 경로 알려주기
download_path = "/Users/bagtaejeong/Downloads"

# @@ 5번 중요!!
# 5) 코드 231, 232 for문에 month_1에서 숫자 부분을 알맞은 월로 수정하기!

# 6) 검색결과조회를 눌렀는데 확인을 눌러야하는 경고창이 뜨면 242번째 줄에 Alert()부분의 주석을 해제할 것!
# --------------------------------------------------------------------------------------------------------------------#


# 기본값
# --------------------------------------------------------------------------------------------------------------------#
# 연월일 형식 만들기
date = datetime.now().strftime("%Y%m%d")

# 1월, 4월, 5월, 7월, 11월 평일을 가리키는 딕셔너리
month_1 = {'tr[1]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 1월 1주차
           'tr[2]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 1월 2주차
           'tr[3]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 1월 3주차
           'tr[4]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 1월 4주차
           'tr[5]': ['td[2]', 'td[3]']}                           # 1월 5주차

month_4 = {'tr[2]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 4월 1주차
           'tr[3]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 4월 2주차
           'tr[4]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 4월 3주차
           'tr[5]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]']} # 4월 4주차

month_5 = {'tr[1]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 5월 1주차
           'tr[2]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 5월 2주차
           'tr[3]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 5월 3주차
           'tr[4]': ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 5월 4주차
           'tr[5]': ['td[2]', 'td[3]', 'td[4]']}                  # 5월 5주차

month_7 = {'tr[2]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 7월 1주차
           'tr[3]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 7월 2주차
           'tr[4]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 7월 3주차
           'tr[5]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 7월 4주차
           'tr[6]' : ['td[2]']}                                    # 7월 5주차

month_11 = {'tr[1]' : ['td[4]', 'td[5]', 'td[6]'],                   # 11월 1주차
            'tr[2]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 11월 2주차
            'tr[3]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 11월 3주차
            'tr[4]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]'], # 11월 4주차
            'tr[5]' : ['td[2]', 'td[3]', 'td[4]', 'td[5]']}         # 11월 5주차
# --------------------------------------------------------------------------------------------------------------------#
# 창 접속
url = 'https://stcis.go.kr/pivotIndi/wpsPivotIndicator.do?siteGb=P&indiClss=IC03&indiSel=IC0301'

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

driver.get(url)

time.sleep(1.3)

# 노선별 혼잡도 클릭
driver.find_element(By.XPATH, '//*[@id="ulListIndiSel"]/li[5]').click()
time.sleep(random.uniform(0.4, 0.8))

# '달력' 이미지 선택
driver.find_element(By.XPATH, '//*[@id="date3"]/li[1]/img').click()
time.sleep(random.uniform(0.3, 0.4))

# 달력에서 '년' 선택
select_element = driver.find_element(By.XPATH, '// *[ @ id = "ui-datepicker-div"] / div / div / select[1]')
select = Select(select_element)
time.sleep(random.uniform(0.3, 0.4))
select.select_by_value('2023')
time.sleep(random.uniform(0.2, 0.3))

# 달력에서 월 선택 <select>
select_element = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[2]')
select = Select(select_element)
time.sleep(random.uniform(0.3,0.4))

# 1월 ~ 12월 value : 0 ~ 11
select.select_by_value(f'{month - 1}') # 일단 1월로 설정 -> 나중에 다시 바꿀 것
time.sleep(random.uniform(0.5,0.7))

# 달력에서 일 선택 (여기선 임의의 수를 선택 -> 나중에 다시 바꿀 것)
driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[3]/a').click()
time.sleep(0.6)

# '경기도' 선택
select_element = driver.find_element(By.XPATH, '//*[@id="searchPopZoneSd"]')
select = Select(select_element)
time.sleep(random.uniform(0.2,0.3))

select.select_by_value('41') # 경기도 : 41
time.sleep(random.uniform(0.5,0.8))

# 시군구 선택
select_element = driver.find_element(By.XPATH, '//*[@id="searchPopZoneSgg"]')
select = Select(select_element)
time.sleep(random.uniform(0.5, 0.7))

# '원하는 곳 선택' 남양주 : 41360 / 수원 : 41117_41111_41113_41110_41115 /
# 고양 : 41280_41285_41287_41281 / 용인 : 41460_41463_41461_41465
select.select_by_value(city)
time.sleep(random.uniform(0.4, 0.6))

# P버스 노선에 담기
try:
    # 검색창에 노선 입력
    driver.find_element(By.XPATH, '//*[@id="popupSearchRouteNo"]').send_keys('P')

    # 노선 '검색' 클릭
    driver.find_element(By.XPATH, '//*[@id="route_space1"]/li[1]/button').click()

    # 창 뜰 때까지 기다리기
    element = WebDriverWait(driver, 150).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="divBusLineList"]/div[1]'))
    )
    time.sleep(random.uniform(0.5, 0.8))

    # 전체선택 클릭
    driver.find_element(By.XPATH, '//*[@id="divBusLineList"]/div[1]/table/thead/tr/th[1]/div/label/div').click()
    time.sleep(random.uniform(0.1, 0.2))

    # 노선 '선택' 버튼 클릭(팝업창 부분)
    driver.find_element(By.XPATH, '//*[@id="popupBusLine"]/div[2]/button').click()
    time.sleep(random.uniform(0.8, 1))

except:
    # Alert창 대비
    wait = WebDriverWait(driver, 10)
    message_alert = wait.until(EC.alert_is_present())
    message_alert.accept()
    print(f'P_Bus 확인해볼 것')

    # 전체 선택 후 지우기
    driver.find_element(By.XPATH, '//*[@id="route_space1"]/li[1]/button').send_keys(Keys.CONTROL + "a")  # 전체 선택
    driver.find_element(By.XPATH, '//*[@id="route_space1"]/li[1]/button').send_keys(Keys.BACKSPACE)  # 지우기

time.sleep(15)  # P버스가 만약 1페이지가 넘어가면 수동으로 20초만에 더 담을 것!

# 일반버스 노선에 담기
for b in bus:
    # 전체 선택 후 지우기
    element = WebDriverWait(driver, 500).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="popupSearchRouteNo"]'))
    )
    element.send_keys(Keys.COMMAND + 'a')

    element = WebDriverWait(driver, 500).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="popupSearchRouteNo"]'))
    )
    element.send_keys(Keys.DELETE)
    time.sleep(0.4)

    # 검색창에 노선 입력
    driver.find_element(By.XPATH, '//*[@id="popupSearchRouteNo"]').send_keys(b)

    # 노선 '검색' 클릭
    driver.find_element(By.XPATH, '//*[@id="route_space1"]/li[1]/button').click()

    # 창 뜰 때까지 기다리기
    element = WebDriverWait(driver, 150).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="divBusLineList"]/div[1]'))
    )
    time.sleep(random.uniform(0.5,0.8))

    # 첫번째 거 클릭
    driver.find_element(By.XPATH, '//*[@id="divBusLineList"]/div[1]/table/tbody/tr/td[1]/div/label/div').click()
    time.sleep(random.uniform(0.3, 0.4))

    # 노선 '선택' 버튼 클릭(팝업창 부분)
    driver.find_element(By.XPATH, '//*[@id="popupBusLine"]/div[2]/button').click()
    time.sleep(random.uniform(1, 1.5))

    time.sleep(0.8)


# 1월
# 반복문으로 월별 재차인원 데이터 가져오기
for key in month_11: # 1월 : month_1 / 4월이면 month_4 / 같이 각 월에 맞는 딕셔너리를 골라야함!
    for value in month_11[key]: # 여기 month_1도 같이 바꿔주세요!
        # '달력' 이미지 선택
        driver.find_element(By.XPATH, '//*[@id="date3"]/li[1]/img').click()
        time.sleep(random.uniform(0.2, 0.3))

        # 달력에서 일 선택
        driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/{key}/{value}/a').click()
        time.sleep(0.4)

        # '검색결과조회' 클릭
        driver.find_element(By.XPATH, '//*[@id="btnSearch"]/button').click()

        # 다운로드 창 뜰 때까지 기다리기
        element = WebDriverWait(driver, 150).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rgrstyReportResult"]/table/tbody/tr[1]/td[1]/table/tbody/tr/td[4]'))
        )
        time.sleep(2.3)

        # 다운로드 완료 되었는지 확인하기 위한 변수 할당
        len_download = len(os.listdir('/Users/bagtaejeong/Downloads'))

        # '다운로드' 클릭
        element_xpath = '/html/body/div[1]/div[2]/form/div[3]/div[2]/div[2]/div[2]/div[2]/div[3]/div/h2/p/span[1]/a'

        # JavaScript 코드를 사용하여 엘리먼트 클릭(위에가 가려져서 대안!)
        driver.execute_script(
            f"document.evaluate('{element_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")

        # Alert창 대비
        wait = WebDriverWait(driver, 10)
        message_alert = wait.until(EC.alert_is_present())
        message_alert.accept()

        # 파일이 다운로드될 때까지 대기
        times = 0
        while times < 30:
            if len(os.listdir('/Users/bagtaejeong/Downloads')) == len_download + 1:
                break
            else:
                times += 1
                time.sleep(0.5)

        time.sleep(3)
        # 다운로드된 파일의 경로 얻기
        # download_path = "/Users/bagtaejeong/Downloads"
        file_name = f'노선·정류장 지표(노선별 혼잡도)_{date}.csv'
        original_file_path = os.path.join(download_path, file_name)

        city_name = {'41360' : '남양주', '41117_41111_41113_41110_41115':'수원',
                     '41280_41285_41287_41281':'고양', '41460_41463_41461_41465':'용인'}

        # 변경할 파일 이름 설정
        new_file_name = f"{city_name[city]}_{month}월_{key}_{value}일_혼잡도.csv"
        new_file_path = os.path.join(download_path, new_file_name)

        # 파일 이동 및 이름 변경
        shutil.move(original_file_path, new_file_path)
        time.sleep(random.uniform(0.8,1.2))

        # 뒤로가기 클릭
        driver.find_element(By.XPATH, '//*[@id="tab1"]/div[2]/div[3]/button').click()
        time.sleep(random.uniform(3,4))

