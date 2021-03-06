__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Smith, Steven", "Tinker, Paul",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

# Import libraries 
import pandas as pd
import requests
import time
import socket
import re

# The function to generate the VirusTotal scan result
def VT_scan (json_data):
    
    VT_scan_result = 1
    
    for scan_result in json_data['scans']:
        for result in json_data['scans'][scan_result]:
            if json_data['scans'][scan_result][result] == True:
                VT_scan_result = 2
    
    return VT_scan_result

# Get the NXDomain verification
def isNXDomain (url):
    try:
        socket.getaddrinfo(url,0,0,0,0)
        return 1        
    except:
        return 0

# Compute % of numerical characters
def numericCharacters (url):
    numeric_count = 0
    for char in url:
        if ord(char) >= 48 and ord(char) <= 57:
            numeric_count += 1
        else:
            continue
    
    return ((numeric_count * 100)/len(url))

# Compute Vowel to Consonant ratio
def VowelToConsonant (url):
    vowel_count = 0
    consonant_count = 0
    for char in url:
        if ord(char) == 97: # decimal ascii code for a
            vowel_count += 1
            continue
        elif ord(char) == 101: # decimal ascii code for e
            vowel_count += 1
            continue
        elif ord(char) == 105: # decimal ascii code for i
            vowel_count += 1
            continue
        elif ord(char) == 111: # decimal ascii code for o
            vowel_count += 1
            continue
        elif ord(char) == 117: # decimal ascii code for u
            vowel_count += 1
            continue
        elif ord(char) >= 97 and ord(char) <= 122:
            consonant_count += 1
            continue
        else:   # for all the non-alphabetic letters
            continue
    
    if consonant_count != 0:    
        return ((vowel_count * 100)/consonant_count)
    else:
        return 100

# Compute Symbol to Character ratio
def SymboltoCharacter (url):
    symbol_count = 0
    char_count = 0
    for char in url:
        if ord(char) >= 48 and ord(char) <= 57:
            continue
        elif ord(char) >= 97 and ord(char) <= 122:
            char_count += 1
        else:
            symbol_count += 1
        
    if char_count != 0:
        return ((symbol_count * 100)/char_count)
    else:
        return 100
    
# Retrieve the Top Level Domains
def retrieveTLD (url):
    url = re.sub('[.]', ' ', url)
    url = url.split()

    return url[-1]

# initialize list of lists 
processedData = []

#importing the data set
dataset = pd.read_csv('../../majestic_million.csv')
print(dataset.head())

family_id = 0
class_id = 0

# VirusTotal API request URL
url = 'https://www.virustotal.com/vtapi/v2/url/report'

# Generating the processed dataset
#for i in range(3740,4740):
for i in range(125000):
    scan_url = dataset['domain'][i]
    scan_url = scan_url.lower()
    print(scan_url , "\t",  i)
    params = {'apikey': 'api_key', 'resource':scan_url}
    
    processedData.append([scan_url, 1, 1, round(numericCharacters(scan_url)), round(VowelToConsonant(scan_url)), len(scan_url), round(SymboltoCharacter(scan_url)), retrieveTLD(scan_url), family_id, class_id])
   
    try:
        response = requests.get(url, params=params)
    
        #the request was correctly handled by the server and no errors were produced
        if response.status_code == 200:    
            json_data = response.json()
            
            # If the item you searched for was not present in VirusTotal's dataset this result will be 0
            if json_data['response_code'] == 0:
                processedData.append([scan_url, 0, isNXDomain(scan_url), round(numericCharacters(scan_url)), round(VowelToConsonant(scan_url)), len(scan_url), round(SymboltoCharacter(scan_url)), retrieveTLD(scan_url), family_id, class_id])
                
            else:
                processedData.append([scan_url, VT_scan(json_data), isNXDomain(scan_url), round(numericCharacters(scan_url)), round(VowelToConsonant(scan_url)), len(scan_url), round(SymboltoCharacter(scan_url)), retrieveTLD(scan_url), family_id, class_id])
        
        #Request rate limit exceeded. You are making more requests than allowed. You have exceeded one of your quotas (minute, daily or monthly).
        elif response.status_code == 204:
            print("Putting to sleep for 40 seconds")
            time.sleep(40)
            print("Back from sleep")
            
        else:
            print("Error in response")
            continue
    except:
        print("Something went wrong")

    
# Create the pandas DataFrame 
df = pd.DataFrame(processedData, columns = ['domain', 'VT_scan', 'isNXDomain', 'perNumChars', 'VtoC', 'lenDomain', 'SymToChar', 'TLD', 'family_id', 'class'])

# Convert the data into csv
pd.DataFrame(df).to_csv("ground_truth_data_processed.csv")