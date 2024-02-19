import pandas as pd
import requests

from bs4 import BeautifulSoup as bs4
from bs4 import BeautifulSoup

# CSV 파일 불러오기
file_path = './data/validPlayerId.csv'
player_data = pd.read_csv(file_path)

i=0

# 새로운 데이터를 저장할 빈 리스트 생성
new_data_list = []

# playerId 리스트 가져오기
player_ids = player_data['playerid']

# playerId를 기반으로 데이터 수집
for player_id in player_ids:
    i = i+1
    url = f'https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId={player_id}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.select_one('#contents > div.sub-content > div.player_info > div.player_basic')
    else:
        print(f"Failed to retrieve the webpage for playerId {player_id}. Status code: {response.status_code}")
        continue

    data = {}
    for li in table.find_all('li'):
        strong_text = li.find('strong').text
        span_text = li.find('span').text
        data[strong_text] = span_text

    new_data_list.append(data)

    if(i%10)==0:
        print(i)

# 리스트를 DataFrame으로 변환
new_data = pd.DataFrame(new_data_list)

# player_data와 new_data를 playerId를 기준으로 병합
final_data = pd.merge(player_data, new_data, left_index=True, right_index=True)

# 최종 결과 확인
print(final_data)


final_data.to_excel('./data/playerInfo.xlsx', index=False, engine='openpyxl')