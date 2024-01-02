import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from requests import get
from bs4 import BeautifulSoup
import re
import matplotlib
import matplotlib.pyplot as plt

def find_string(s):
    regex_pattern = ">(.*?)<"
    result = re.findall(regex_pattern, str(s))
    t = str(result[0]).replace(",","")
    return int(t) if t.isdigit() else t

base_url = 'https://battlecats-db.com/unit/status_r_all.html'

response = get(f"{base_url}")
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find_all('tbody')

tmp_list = []
ans = []

target_cnt = 50

for tbl in table:
    tr = tbl.find_all('tr')
    n = 0
    for t_r in tr:
        n = n + 1
        if (n % 3 != 0):
            continue
        if (n > target_cnt * 3):
            break
        td = t_r.find_all('td', class_="R")
        cnt = 0
        tmp_list.clear()
        for t_d in td:
            tag_R = t_d.find_all('font')
            if len(tag_R) == 0:
                tmp_list.append(find_string(t_d))
            else:
                for f in tag_R:
                    tmp_list.append(find_string(f))
                    break
            cnt = cnt + 1
        ans.append(tmp_list.copy())

# print(ans)

matplotlib.rcParams['font.family'] = 'Malgun Gothic'

df = pd.DataFrame(ans, columns=["체력", "히트백", "속도", "공격력", "DPS", "공격타입", "공격 빈도(f)", "공격 간격(f)", "사정거리", "코스트", "재생산"],
                  index=[f"" for x in range(1, target_cnt + 1)])
df.sort_values("체력", inplace=True)

df_hp = df.loc[:, '체력']
df_dmg = df.loc[:, '공격력']
df_range = df.loc[:, '사정거리']
df_reproduction = df.loc[:, '재생산']

fig, axes = plt.subplots(nrows=2, ncols=2)

# axes[0,0]에는 체력만 표시
df_hp.plot(kind='bar', ax=axes[0,0], color='red')
axes[0,0].tick_params(axis='y')
axes[0,0].set_ylabel('체력', color='red')
axes[0,0].set_title('체력')

# axes[0,1]에는 체력과 재생산을 표시
df_hp.plot(kind='bar', ax=axes[0,1], color='red')
axes[0,1].tick_params(axis='y')
axes[0,1].set_ylabel('체력', color='red')

df_reproduction.plot(kind='line', ax=axes[0,1], color='orange', secondary_y=True)
axes[0,1].tick_params(axis='y')
axes[0,1].set_title('체력 대비 재생산')

#axes[1,0]에는 체력과 사거리를 표시
df_hp.plot(kind='bar', ax=axes[1,0], color='red')
axes[1,0].tick_params(axis='y')
axes[1,0].set_ylabel('체력', color='red')

df_range.plot(kind='line', ax=axes[1,0], color='green', secondary_y=True)
axes[1,0].tick_params(axis='y')
axes[1,0].set_title('체력 대비 사거리')

# axes[1,1]에는 체력과 공격력을 표시
df_hp.plot(kind='bar', ax=axes[1,1], color='red')
axes[1,1].tick_params(axis='y')
axes[1,1].set_ylabel('체력', color='red')

# set second y-axis label
df_dmg.plot(kind='line', ax=axes[1,1], secondary_y=True)
axes[1,1].set_title('체력 대비 공격력')

plt.show()