import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
from time import sleep

# For greatplacetowork --------------------------------------------------------
url = 'https://www.greatplacetowork.com/best-workplaces/100-best/2018'
response = requests.get(url)
content = response.content
page = BS(content)

table = page.find('div', attrs={'id':'list-detail-left-column'})
div_list = table.find_all('div', attrs={'class':'col-md-5 col-xs-12 company-text'})

df = pd.DataFrame(columns=['rank', 'coname'], index=range(100))
for i_div, div in enumerate(div_list):
    coname = div.find('a', attrs={'class':'link h5'}).text.strip()
    df.loc[i_div, 'coname'] = coname

df['rank'] = range(1,101)
df.to_excel('Data_Reputation/Data_Fortune100Rank_2018.xlsx', index=False)


# For CNN --------------------------------------------------------------------------
for year in range(2008, 2014):
    url = f'https://money.cnn.com/magazines/fortune/bestcompanies/{year}/full_list/'
    response = requests.get(url)
    
    content = response.content
    page = BS(content)
    
    tr_list = page.find_all('tr')
    tr_len = len(tr_list)
    
    df = pd.DataFrame(index=range(tr_len), columns=[ 'rank', 'coname', 'growth', 'workers'])
    
    for i_tr, tr in enumerate(tr_list):
        td_list = tr.find_all('td')
        if len(td_list) != 4: continue
        df.loc[i_tr, ['coname', 'growth', 'workers']] = [item.text.strip() for item in td_list[1:]]
    
    df.dropna(subset=['coname'], inplace=True)
    df = df[['%' in row for row in  df['growth'].values]]
    df['rank'] = range(1,len(df)+1)
    
    df.to_excel(f'Data_Reputation/Data_Fortune100Rank_{year}.xlsx', index=False)
    sleep(30)


# For rankingthebrands --------------------------------------------------------
url = 'https://www.rankingthebrands.com/The-Brand-Rankings.aspx?rankingID=100&year=1442'
response = requests.get(url)

content = response.content
page = BS(content)
print(response.status_code)

df = pd.DataFrame(columns=['rank', 'coname'], index=range(100))
div_list = page.find_all('div', attrs={'class':'top100row'})
for i_div, div in enumerate(div_list): 
    coname = div.find('div', attrs={'class':'name'}).text
    df.loc[i_div, 'coname'] = coname
df['rank'] = range(1,101)

df.to_excel('Data_Reputation/Data_Fortune100Rank_2023.xlsx', index=False)
