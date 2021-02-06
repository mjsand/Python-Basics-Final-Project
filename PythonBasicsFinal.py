import bs4
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

links=['https://en.wikipedia.org/wiki/Michael_Jordan'\
       ,'https://en.wikipedia.org/wiki/Kobe_Bryant'\
      ,'https://en.wikipedia.org/wiki/LeBron_James'\
      ,'https://en.wikipedia.org/wiki/Stephen_Curry']
names=['Michael Jordan','Kobe Bryant','Lebron James','Stephen Curry']

def get_basketball_stats(link='https://en.wikipedia.org/wiki/Michael_Jordan'):
    # read the webpage 
    response = requests.get(link)
    # create a BeautifulSoup object to parse the HTML  
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # the player stats are defined  with the attribute CSS class set to 'wikitable sortable'; 
    #therefore we create a tag object "table"
    table=soup.find(class_='wikitable sortable')

    #the headers of the table are the first table row (tr) we create a tag object that has the first row  
    headers=table.tr
    #the table column names are displayed as an abbreviation; therefore we find all the abbr tags and return an Iterator
    titles=headers.find_all("abbr")
    #we create a dictionary  and pass the table headers as the keys 
    data = {title['title']:[] for title in titles}
   #we will store each column as a list in a dictionary. the header of the column will be the dictionary key 

    #we iterate over each table row by finding each table tag tr and assign it to the object
    for row in table.find_all('tr')[1:]:
    
        #we iterate over each cell in the table, as each cell corresponds to a different column. we obtain the corresponding key for the column n 
        for key,a in zip(data.keys(),row.find_all("td")[2:]):
            # we append each elment and strip any extra HTML contnet 
            data[key].append(''.join(c for c in a.text if (c.isdigit() or c == ".")))

    # we remove extra rows by finding the smallest list     
    Min=min([len(x)  for x in data.values()])
    #we convert the elements in the key to floats 
    for key in data.keys():
    
        data[key]=list(map(lambda x: float(x), data[key][:Min]))
       
    return data

# creating dictionaries for each player's stats
michael_jordan_dict = get_basketball_stats(links[0])
kobe_bryant_dict = get_basketball_stats(links[1])
lebron_james_dict = get_basketball_stats(links[2])
steph_curry_dict = get_basketball_stats(links[3])

#creating dataframes for each player's dictionary
michael_jordan_df = pd.DataFrame(michael_jordan_dict)
kobe_bryant_df = pd.DataFrame(kobe_bryant_dict)
lebron_james_df = pd.DataFrame(lebron_james_dict)
steph_curry_df = pd.DataFrame(steph_curry_dict)

#displaying dataframes 
#print('Michael Jordan\n', michael_jordan_df.head()) 
#print('Kobe Bryant\n', kobe_bryant_df.head())
#print('Lebron James\n', lebron_james_df.head())
#print('Steph Curry\n', steph_curry_df.head())
y = np.linspace(0,14,15).astype(int)


#plotting each player's points per game for every year
plt.scatter(y, michael_jordan_df[['Points per game']], label=names[0])
#plt.plot(kobe_bryant_df[['Points per game']], label=names[1])
#plt.scatter(lebron_james_df[['Points per game']], label=names[2])
#plt.scatter(steph_curry_df[['Points per game']], label=names[3])
plt.legend()
plt.xlabel('years')
plt.ylabel('Points per game')
















