# Query Covid-19 data and send OSC messages from it

## install dependencies

`pip3 install -r requirements.txt`

## quick use

`python3 queryAPI.py --start 2021-01-03 --end 2021-01-17`

this will send OSC messages to the port 57120 in localhost (for example to handle in SuperCollider) 

## command-line help
`python3 queryAPI.py -h`


```
usage: queryAPI.py [-h] [--start YYY-mm-dd] [--end YYY-mm-dd]
                   [--oscport OSCPORT] [--oscip OSCIP]

Python script to query Covid-data for Mexico, Iran, Indonesia and India. The
data will get parsed and the average deaths per day will be sent via OSC')

optional arguments:
  -h, --help         show this help message and exit
  --start YYY-mm-dd  start date to query covid data
  --end YYY-mm-dd    end date to query covid data
  --oscport OSCPORT  port to send the osc messages. defaults to 57120
  --oscip OSCIP      ip address to send the osc messages to. defaults to
                     localhost

example: python3 queryAPI.py --start 2021-01-03 --end 2020-12-28
```
