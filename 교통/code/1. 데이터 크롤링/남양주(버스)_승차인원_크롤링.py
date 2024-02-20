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

# 연월일 형식 만들기
date = datetime.now().strftime("%Y%m%d")

# @@@ 주의할 점 @@@@ -> 꼭 사용자화 하기!!
# 1) 원하는 시 선택
# 2) month_list 확인할 것!
# 3) bus_list 확인할 것!(저처럼 여러개로 나눠도 좋고, 한 개로 하셔도 상관 없습니다! 대신 여러개일 땐 for문에서 bus가 들어갈 리스트만 바꿔주시면 됩니다!)
# 4) 다운로드 받는 경로 알려주기! -> 파일 이름 바꾸는 거 때문

# 사용자화
# --------------------------------------------------------------------------------------------------------------------#
# 원하는 시에 맞는 value 쓰기
# 남양주 : '41360' / 수원 : '41117_41111_41113_41110_41115' /
# 고양 : '41280_41285_41287_41281' / 용인 : '41460_41463_41461_41465'
city = '41360'

# 원하는 달 고르기
month_list = [1,4,5,7,11]

# 총 64개 -> 이 중 1115-6, 1650, 1680번 버스가 모든 달에 없지만 구리 노선.
bus = ['M2316', 'M2323', 'M2341', 'M2344', 'M2352', 'M2353', '11', '100', '105', '105-1', # 10개
       '1000', '1001', '1003', '1006', '1100', '1115-6', '1200', '1650', '1660', '1670', # 10개
       '1680', '1700', '2000', '2000-1', '8001', '8002', '8012', '1000-1', '1200-1', '1330-2', # 10개
       '1330-3', '1330-44', '1403', '1670-1', '8002-1', '3006', '7001', '7000', '7002', # 9개
       '7007', '8005', '8109', '8401', '8409', # 5개
       'G1200', 'G1300', 'G1300N', 'G6000', 'G6000N', 'G6100', 'G6100N', 'G9311' # 8개
       'P9701','P9401', 'P9402 ', 'P9404', 'P9601', 'P9602'] # 출근, 퇴근 2개씩 12개.





# 처음 다운로드 받는 곳 경로 알려주기
download_path = "/Users/bagtaejeong/Downloads"
# --------------------------------------------------------------------------------------------------------------------#

for month in month_list:
    for i in bus: # 버스 리스트 바꿀 곳!
        try:
            url = 'https://stcis.go.kr/pivotIndi/wpsPivotIndicator.do?siteGb=P&indiClss=IC03&indiSel=IC0301'

            options = Options()
            options.add_argument("--start-maximized")
            options.add_experimental_option("detach", True)

            driver = webdriver.Chrome(options=options)

            driver.get(url)

            time.sleep(1.3)

            # '월' 선택
            driver.find_element(By.XPATH, '//*[@id="divRdoDate"]/li[2]').click()
            time.sleep(random.uniform(0.2, 0.3))
            driver.find_element(By.XPATH, '//*[@id="date2"]/li[1]/img').click()
            time.sleep(random.uniform(0.1, 0.2))


            # 달력에서 월 선택 <select>
            select_element = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[2]')
            select = Select(select_element)
            time.sleep(random.uniform(0.3,0.4))

            # 1월 ~ 12월 value : 0 ~ 11
            select.select_by_value(f'{month - 1}') # 원하는 월에서 1빼기
            time.sleep(random.uniform(0.5,0.7))

            # 확인
            driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/button').click()
            time.sleep(0.2)
            # 시군구 선택이 디폴트값이라 따로 선택 안 해도 됨.

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
            time.sleep(random.uniform(0.2, 0.4))

            # 노선 선택
            driver.find_element(By.XPATH, '//*[@id="popupSearchRouteNo"]').send_keys(i)

            # 노선 '검색' 클릭
            driver.find_element(By.XPATH, '//*[@id="route_space1"]/li[1]/button').click()

            # 창 뜰 때까지 기다리기
            element = WebDriverWait(driver, 150).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="divBusLineList"]/div[1]'))
            )
            time.sleep(random.uniform(0.5,0.8))

            # 노선 클릭
            driver.find_element(By.XPATH, '//*[@id="divBusLineList"]/div[1]/table/tbody/tr/td[1]/div/label/div').click()
            time.sleep(random.uniform(0.1, 0.2))

            # # 'P버스(퇴근) 을 위한 코드 / P버스는 같은 노선에 대해 출근, 퇴근이 두개라서 다르게 접근해야함.
            # driver.find_element(By.XPATH, '//*[@id="divBusLineList"]/div[1]/table/tbody/tr[2]/td[1]/div/label/div').click()
            # time.sleep(random.uniform(0.1, 0.2))

            # 노선 '선택' 버튼 클릭
            driver.find_element(By.XPATH, '//*[@id="popupBusLine"]/div[2]/button').click()
            time.sleep(random.uniform(0.4, 0.7))

            # '검색결과조회' 클릭
            driver.find_element(By.XPATH, '//*[@id="btnSearch"]/button').click()


            # Alert창 대비
            wait = WebDriverWait(driver, 10)
            message_alert = wait.until(EC.alert_is_present())
            message_alert.accept()

            # 다운로드 창 뜰 때까지 기다리기
            element = WebDriverWait(driver, 150).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="pivotGrid"]/div/div[6]/div/div/div[1]/div'))
            )
            time.sleep(4)

            # '다운로드' 클릭
            driver.find_element(By.XPATH, '// *[ @ id = "btnExport"]').click()
            time.sleep(5)

            # 다운로드된 파일의 경로 얻기
            # download_path = "/Users/bagtaejeong/Downloads"
            file_name = f"노선·정류장 지표(노선별 이용량)_{date}.xlsx" # 날짜 바뀌면 바꿔줘야함!!
            original_file_path = os.path.join(download_path, file_name)

            # 변경할 파일 이름 설정
            new_file_name = f"남양주_{i}_{month}.xlsx" # 출근, 퇴근은 P버스 일때만!
            new_file_path = os.path.join(download_path, new_file_name)

            # 파일 이동 및 이름 변경
            shutil.move(original_file_path, new_file_path)

            driver.quit()

        except:
            print(f'{month}월 {i}번 버스 조회 안 됨')
            # driver.quit()