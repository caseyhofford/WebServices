# API key: bb62a9dd949a79650ef7514efc0ddd49
from urllib.request import urlopen
import requests, json, urllib

data = urlopen("https://api.stlouisfed.org/fred/series?series_id=CP0114EU28M086NEST&api_key=bb62a9dd949a79650ef7514efc0ddd49&file_type=json").read().decode('utf-8')
print(data)
text_file = open("series.txt", "w")
text_file.write(data)
text_file.close()
