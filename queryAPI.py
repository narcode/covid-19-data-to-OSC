import requests
from pythonosc.udp_client import SimpleUDPClient
import datetime
import time
import concurrent.futures
import argparse

parser = argparse.ArgumentParser(
    description='''
Python script to query Covid-data for Mexico, Iran, Indonesia and India. 
The data will get parsed and the average deaths per day will be sent via OSC')
''',
epilog='''
example: python3 queryAPI.py --start 2021-01-03 --end 2020-12-28
''')
parser.add_argument('--start', help='start date to query covid data', metavar='YYY-mm-dd')
parser.add_argument('--end', help='end date to query covid data', metavar='YYY-mm-dd')
parser.add_argument('--oscport', help='port to send the osc messages. defaults to 57120', type=int, default=57120)
parser.add_argument('--oscip', help='ip address to send the osc messages to. defaults to localhost', default='127.0.0.1')

args = parser.parse_args()

if  args.start == None and args.end == None:
    parser.print_help()
    exit()

today = datetime.date.today()

# endpoints: 
mx = "https://api.coronatracker.com/v5/analytics/trend/country?countryCode=mx&startDate=%s&endDate=%s"%(args.start, args.end)
iran = "https://api.coronatracker.com/v5/analytics/trend/country?countryCode=ir&startDate=%s&endDate=%s"%(args.start, args.end)
india = "https://api.coronatracker.com/v5/analytics/trend/country?countryCode=in&startDate=%s&endDate=%s"%(args.start, args.end)
indo = "https://api.coronatracker.com/v5/analytics/trend/country?countryCode=id&startDate=%s&endDate=%s"%(args.start, args.end)

data = {}
r = {}
endpoints = {'mx': mx, 'iran':iran, 'india': india, 'indo': indo}

for (k, endpoint) in endpoints.items():
    r[k] = requests.get(endpoint)
    data[k] = r[k].json()

filteredData = { 'mx': {}, 'iran': {}, 'india': {}, 'indo': {} };


for country in data:
    for result in data[country]:
        filteredData[country][result['last_updated'][0:10]] = result['total_deaths']

#mockup = {'mx': {'2022-01-03': 299525, '2022-01-02': 299525, '2022-01-01': 299428, '2021-12-31': 299285, '2021-12-30': 299132, '2021-12-29': 298944, '2021-12-28': 298819 },
          #'iran': {'2022-01-03': 131680, '2022-01-02': 131680, '2022-01-01': 131639, '2021-12-31': 131606, '2021-12-30': 131572, '2021-12-29': 131527, '2021-12-28': 131474 },
          #'india': {'2022-01-03': 481770, '2022-01-02': 481770, '2022-01-01': 481519, '2021-12-31': 481080, '2021-12-30': 480860, '2021-12-29': 480592, '2021-12-28': 480320 },
          #'indo': {'2022-01-03': 144097, '2022-01-02': 144097, '2022-01-01': 144096, '2021-12-31': 144094, '2021-12-30': 144088, '2021-12-29': 144081, '2021-12-28': 144071}
          #}

perhour = { 'mx': {}, 'iran': {}, 'india':{}, 'indo':{} }
result = { 'mx': {}, 'iran': {}, 'india':{}, 'indo':{} }


# OSC
ip = "127.0.0.1"
port = 57120

client = SimpleUDPClient(ip, port)  # Create client

# calculate average per hour per day
def calcPerHour():
    for country in filteredData.keys():
        for (day, deaths) in filteredData[country].items():
            current = datetime.datetime.strptime(day, '%Y-%m-%d')
            yesterday = current - datetime.timedelta(days=1)
            try:
                diff = deaths - filteredData[country][yesterday.strftime('%Y-%m-%d')]
                av = diff/24
                perhour[country][current.strftime('%Y-%m-%d')] = av
                print("%s day diff %s: %i | average per hour: %f"%(country, day, diff, av))
            except KeyError:
                print('only one week!')
                
def sendData(country, seconds):
    print(country)
    print(perhour)
    for date in perhour[country]:
        value = perhour[country][date]
        if value == 0:
            r = 2
        else:
            r = value
        # day cycle
        for h in range(round(r)):
            print("\n%s - %s at %d: %d"%(country, date, h, value))
            if value > 0:
                client.send_message("/d/%s"%(country), value)   # Send float message
            #time.sleep(seconds/24) # v2
            time.sleep(r/2) # /2 to speed up

    
if __name__ == '__main__':
    a = calcPerHour()
    with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
        future_to_f = { executor.submit(sendData, c, 10): c for c in perhour.keys() }
        for future in concurrent.futures.as_completed(future_to_f):
            r = future_to_f[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (r, exc))
    
    