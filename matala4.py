import requests
import json
from urllib.parse import urlparse
from urllib.parse import urlencode


def read_file(file):
    '''Reads Whatsapp text file into a list of strings'''
    x = open(file,'r', encoding = 'utf-8') #Opens the text file into variable x but the variable cannot be explored yet
    y = x.read() #By now it becomes a huge chunk of string that we need to separate line by line
    content = y.splitlines() #The splitline method converts the chunk of string into a list of strings
    return content

#Creating a list of cities dictianory
def find_city(dest:list):
    response = []
    for city in dest:
        parms = {}
        parms2 = {}
        parms['origins'] = 'תל אביב'
        parms['destinations'] = city
        parms['key'] = api_key
        url = Serviceurl + urlencode(parms)
        response.append(requests.get(url).json())
        parms2['address'] = city
        parms2['key'] = api_key
        url2 = Serviceurl2 + urlencode(parms2)
        response.append(requests.get(url2).json())
    return response

#Final dictianory
def dest_info(response:list):
    result = []
    i=0
    j=1
    respons = find_city(dest)
    for city in response:
        dest_name = response[i]['destination_addresses'][0]
        mydict = {dest_name:""}
        mydict[dest_name] = {'distance': "" , 'time': ""}
        mydict[dest_name]['distance'] = response[i]['rows'][0]['elements'][0]['distance']['text']
        mydict[dest_name]['time'] = response[i]['rows'][0]['elements'][0]['duration']['text']
        mydict[dest_name]['longitude'] = response[j]['results'][0]['geometry']['location']['lng']
        mydict[dest_name]['latitude'] = response[j]['results'][0]['geometry']['location']['lat']  
        result.append(mydict)
        i = i+2
        j = j+2
        if i>8 and j>9:
            break
    return result

#Sorting by decrease distance
def Sort_Tuple(max_dist): 
    # getting length of list of tuples
    lst = len(max_dist) 
    for i in range(0, lst): 
          
        for j in range(0, lst-i-1): 
            if (max_dist[j][1] < max_dist[j + 1][1]): 
                temp = max_dist[j] 
                max_dist[j]= max_dist[j + 1] 
                max_dist[j + 1]= temp 
    return max_dist 


Serviceurl ='https://maps.googleapis.com/maps/api/distancematrix/json?'
Serviceurl2 ='https://maps.googleapis.com/maps/api/geocode/json?'
api_key = 'API KEY'
dest = read_file('dests.txt')
response = find_city(dest)
result = dest_info(response)
dist = {}
max_dist = []

#Print more readable 
i = 0
for item in result:
    for (key,value) in result[i].items():
        print('\n',key,'\n')
        for key1,value2 in value.items():
            print(key1,':',value2)
    i = i+1

#Create the max distance list of dictianory
i = 0
for item in result:
    for (key,value) in result[i].items():
        dist = (key, value['distance'])
    i = i+1
    max_dist.append(dist)
    
print('\n','\n','3 Farthest cities are: ','\n', Sort_Tuple(max_dist)[:3])    
    
