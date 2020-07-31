import json
import os
import glob
import pandas as pd

with open(r'C:\Users\cj0520\Desktop\PowerRequirements\devices.json') as json_file:
    data = json.load(json_file)
    for i in data['ios']:
        ios_name = i["name"]
        ios_version = i["os_version"]
        ios_model = i['model']
    for a in data['android']:
        android_name = a["name"] 
        android_version = a["os_version"] 
        android_model = a["model"] 

version_data = pd.read_csv(r'C:\Users\cj0520\Desktop\PowerRequirements\data\versions.csv') 
df = pd.DataFrame(version_data) 

transmitter_version = df.at[0,'Value']

data = {'Type':['transmitter_version','ios_name', 'ios_version', 'ios_model', 'android_name', 'android_version', 'android_model'], 
   'Value':[transmitter_version, ios_name, ios_version, ios_model, android_name, android_version, android_model]} 

df = pd.DataFrame(data)

df.to_csv(r'C:\Users\cj0520\Desktop\PowerRequirements\data\versions.csv')