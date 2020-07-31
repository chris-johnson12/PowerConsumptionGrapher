import glob
import os
import math
import array as arr
import pandas as pd
import plotly.graph_objects as go

avgCurrents_ANDROID = [] 
avgCurrents_RECV_ANDROID = []
avgCurrents_RECV_IOS = []
avgCurrents_RECV = []
avgCurrents_IOS = []
avgCurrents_NO_DISPLAY = []

date_ANDROID = []
date_RECV_ANDROID = []
date_RECV_IOS = []
date_RECV = []
date_IOS = []
date_NO_DISPLAY = []

case = []
date = []
current = []

dict_ANDROID = {}
dict_RECV_ANDROID = {}
dict_RECV_IOS = {}
dict_RECV = {}
dict_IOS = {}
dict_NO_DISPLAY = {}

files = glob.glob(r"C:\Users\cj0520\Desktop\PowerRequirements\data\*.txt")
files.sort(key=os.path.getmtime)
for file in files:
    fp = open(file, 'r')
    lines = fp.readlines()
    dateRan = file[47:57]
    for line in lines:
        currentPrefix = 'Ch1 AVG current:'
        currentSuffix = 'uA'
        if currentPrefix in line:
            avgCurrent = line[16:26]
        testCasePrefix = 'TEST_CASE:'
        if testCasePrefix in line:
            testCase = line.strip().lstrip(testCasePrefix).strip()
            toStrip = '-'
            if (testCase == 'Android'):
                date_ANDROID.append(dateRan)
                avgCurrents_ANDROID.append(round(float(avgCurrent),1))
            elif (testCase == 'Receiver, Android'):
                date_RECV_ANDROID.append(dateRan)
                avgCurrents_RECV_ANDROID.append(round(float(avgCurrent),1))
            elif (testCase == 'Receiver, IOS'):
                date_RECV_IOS.append(dateRan)
                avgCurrents_RECV_IOS.append(round(float(avgCurrent),1))
            elif (testCase == 'Receiver'):
                date_RECV.append(dateRan)
                avgCurrents_RECV.append(round(float(avgCurrent),1))
            elif (testCase == 'IOS'):
                date_IOS.append(dateRan)
                avgCurrents_IOS.append(round(float(avgCurrent),1))
            elif (testCase == "NO_DISPLAY"):
                date_NO_DISPLAY.append(dateRan)
                avgCurrents_NO_DISPLAY.append(round(float(avgCurrent),1))
            else: print ("Unhandled test case:", testCase, "in file:", file)
            
dict_ANDROID = {'dateTested': date_ANDROID, 'ANDROID': avgCurrents_ANDROID}
dict_RECV_ANDROID = {'dateTested': date_RECV_ANDROID, 'RECV_ANDROID': avgCurrents_RECV_ANDROID}
dict_RECV_IOS = {'dateTested': date_RECV_IOS, 'RECV_IOS': avgCurrents_RECV_IOS}
dict_RECV = {'dateTested': date_RECV, 'RECV': avgCurrents_RECV}
dict_IOS = {'dateTested': date_IOS, 'IOS': avgCurrents_IOS}
dict_NO_DISPLAY = {'dateTested': date_NO_DISPLAY, 'NO_DISPLAY': avgCurrents_NO_DISPLAY}

df1 = pd.DataFrame(data=dict_ANDROID)
df2 = pd.DataFrame(data=dict_RECV_ANDROID)
df3 = pd.DataFrame(data=dict_RECV_IOS)
df4 = pd.DataFrame(data=dict_RECV)
df5 = pd.DataFrame(data=dict_IOS)
df6 = pd.DataFrame(data=dict_NO_DISPLAY)

df = pd.merge(df1,df2, how='outer')
df = pd.merge(df,df3, how= 'outer')
df = pd.merge(df,df5, how= 'outer')
df = pd.merge(df,df4, how= 'outer')
df = pd.merge(df,df6, how= 'outer')

df = df.where(pd.notnull(df), None)

df = df.drop_duplicates(subset='dateTested', keep='first')

df = df.sort_values('dateTested', ascending=True)

#df['IOS'] = df['IOS'].mask(df['IOS'] > 100.0, None)

fig = go.Figure()

df = df.iloc[43:]

df['Battery Budget'] = 21.6

df7 = pd.read_csv(r'C:\Users\cj0520\Desktop\PowerRequirements\data\versions.csv')

#add each of the columns to be graphed
fig.add_trace(go.Scatter(
    x=df['dateTested'],
    y=df['ANDROID'],
    name = 'Android Ver. ' + df7.at[5,'Value'],
    connectgaps=True,
    #text = "this will pop up on hover over" 
))
fig.add_trace(go.Scatter(
    x=df['dateTested'],
    y=df['IOS'],
    name= 'IOS Ver. ' + df7.at[2,'Value'],
    connectgaps=True
))
fig.add_trace(go.Scatter(
    x=df['dateTested'],
    y=df['RECV_ANDROID'],
    name='Receiver, Adroid',
    connectgaps=True
))
fig.add_trace(go.Scatter(
    x=df['dateTested'],
    y=df['RECV_IOS'],
    name='Receiver, IOS',
    connectgaps=True
))
fig.add_trace(go.Scatter(
    x=df['dateTested'],
    y=df['RECV'],
    name='Receiver (Ver. 5.1.1.040)',
    connectgaps=True
))
fig.add_trace(go.Scatter(
    x=df['dateTested'],
    y=df['NO_DISPLAY'],
    name='No Display',
    connectgaps=True
))
fig.add_trace(go.Scatter(
    x=df['dateTested'],
    y=df['Battery Budget'],
    name = 'Battery Budget',
    line_color="#000000",
))

fig.update_layout(
    title='Transmitter Power Consumption, Transmitter Ver. '+ df7.at[0,'Value'],
    xaxis_title="Date Test Ran",
    yaxis_title="MicroAmps (uA)"
)

#TODO: add another white trace use graph_object.scatter to NOT trace the white trace
#use #FFFFFF to make it white, use <b> to create a new line and html formatting for bold
#make sure it is the last trace so it extends into white space

#add dates to the axis, so the html model is easier to read and navigate
fig.update_layout(yaxis=dict(title='MicroAmps (uA)'),
                  xaxis=dict(title='Date Test Ran',
                  tick0= df['dateTested'].iloc[0],
                  tickvals= df['dateTested'],
                  ticktext = df['dateTested']
                  )
                 )
fig.write_html(r'C:\Users\cj0520\Desktop\PowerRequirements\data\power_graph.html')