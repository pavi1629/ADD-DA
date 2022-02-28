import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import csv



# Keep this part commented Students
'''
http_proxy  = "http://r1dpopr:Nrsc%40123@proxy6.nrsc.gov.in:8080"
https_proxy = "http://r1dpopr:Nrsc%40123@proxy6.nrsc.gov.in:8080"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
            }
'''


URL = 'https://www.emdat.be/'

# TODO : Use Request API to fetch the data stored in URL
r = requests.get(URL)
soup = BS(r.content, 'html5lib') # Using Beautiful Soup Library to parse the received data



# TODO : Use the soup, functionality 'find' to locate the 'div' where 'class' attribute is 'my-dow-title'
week_str = soup.find('div', attrs={'class':'my-dow-title'}).decode_contents()

# TODO : Extract the week number and year from the extracted string
week = int(week_str.split(':')[0].split('-')[0].split(' ')[1])
year = int(week_str.split(':')[0].split('-')[1])

disasters_of_week = soup.find('div', attrs = {'class':'views-field views-field-field-dow-natural-disasters'})

# TODO : Use decode_contents() to decode the <p> element of the above extracted div
dow_str = disasters_of_week.div.p.decode_contents()

events = dow_str.split('<br/>')

def extract_info(x):
    '''
    TODO: Fill in expression blocks with the required expression as directed by 
        the TODO statement. The ultimate aim of this function is to return 3 
        parameters, the Disaster ID, the Type of Disaster and Location for every
        line that is passed to it. We need to use string format based extraction.

    Parameters
    ----------
    x : The input is each element of events list, or the line containing event

    Returns
    -------
    Var-1
        Disaster_ID of the format <YYYY-DNO> 
    Var-2
        The type of Disaster, flood etc
    Var-3
        Location of the disaster

    '''
    # TODO : You must have seen that each element of event is riddled with '\n'\
    #    using the strip function remove all preceeding and succeeding '\n'
    x = events
    if ';' in x:
        # TODO : Explain the Logic(s) used to separate the 3 Variables as defined in the function definition in the comment below this line
        return x.split('\xa0')[0].strip()[:8], x.split('\xa0\xa0')[-1].strip().split(';')[0], x.split('\xa0\xa0')[-1].strip().split(';')[1].strip()
        # Answer here
        #   Var-1
           # DisasterID
        #   Var-2
           #DisasterType
        #   Var-3
           #Location
    else:
        return x.split('\xa0')[0].strip()[:8], ', '.join(x.split('\xa0\xa0')[-1].strip().split(',')[:-1]), x.split('\xa0\xa0')[-1].strip().split(',')[-1].strip()

# TODO : Write a list comprehension to apply the function extract_info() on all elements of list events
info = [extract_info(x) for x in events]

disaster_df = pd.DataFrame(info, columns=['DisasterID', 'DisasterType', 'Location'])
disaster_df['Week'] = [week]*len(disaster_df)
disaster_df['Year'] = [year]*len(disaster_df)

# TODO : Use Right-Click + Inspect method to locate the next button as shown in the slides
next_button = soup.find()

next_page = URL[:-1]+next_button.a.attrs['href']

page=2

def get_disasters(url, page):
    '''
    TODO: Fill the function definition after understanding what this function is trying to do
        This block uses the concept of recursion, in such a case when will the function stop
        calling itself

    Parameters
    ----------
    url : TYPE
        DESCRIPTION.
    page : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    global disaster_df
    
    r= requests.get(url)
    soup = BS(r.content, 'html5lib')
    week_str = soup.find('div', attrs={'class':'my-dow-title'}).decode_contents()
    
    week = int(week_str.split(':')[0].split('-')[0].split(' ')[1])
    year = int(week_str.split(':')[0].split('-')[1])
    
    print('Parsing : %d : %d week of %d year'%(page, week, year))
    
    disasters_of_week = soup.find('div', attrs = {'class':'views-field views-field-field-dow-natural-disasters'})

    dow_str = disasters_of_week.div.p.decode_contents()

    events = dow_str.split('<br/>')
    
    info = [extract_info(x) for x in events]

    disaster_sub_df = pd.DataFrame(info, columns=['DisasterID', 'DisasterType', 'Location'])
    disaster_sub_df['Week'] = [week]*len(disaster_sub_df)
    disaster_sub_df['Year'] = [year]*len(disaster_sub_df)
    
    disaster_df = pd.concat([disaster_df, disaster_sub_df])
    print(disaster_df)
    next_button = soup.find('li', attrs={'class':'pager-next last'})
    
    if type(next_button)==type(None):
        next_page = URL[:-1]+next_button.a.attrs['href']
        get_disasters(next_page, page+1)
        get_disasters(next_page, page)
disaster_df.index = disaster_df.DisasterID

# REQUIRED : Call the function you have just created above (Hint : Line 138 of the function just needs to alter scope to accomplish this task)

# REQUIRED : Answer the following questions in the comment line
# Q1 : What does the keyword global do in the function line 109?
    # answer : The global keyword is used to create global variables inside a function.
    #          The global variables can be modified outside the function also.

# Q2 : Which of the following concepts are demonstrated in implementation of the above function and why?: Overloading, Polymorphism, Recursion
   #answer : Recursion concept is used in this program. The function is called repeatedly to retrieve the data when the next button is pressed.

# TODO : save the pandas DataFrame disaster_df to csv 'Disaster_webScraped.csv'
print(disaster_df)

filename = 'Disaster_webScraped.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['DisasterID', 'DisasterType', 'Location'])
    w.writeheader()
   
disaster_df.to_csv('Disaster_webScraped.csv')

    
'''  
# OPTIONAL : The above part of code accomplishes the given TODO, however I would like you to learn about 'to_csv' function in pandas framework
#            Kindly implement it using the same.
disaster_df_Updated.py
Displaying disaster_df_Updated.py.
'''