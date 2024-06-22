import requests

api_key = '8106990c422257a37738565f5a413385'

# http://api.openweathermap.org/geo/1.0/direct?q={city name}&limit=5&appid={API key}
# 根据城市名获取经纬度
def get_location(city):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    # print(data)
    return data[0]['lat'], data[0]['lon']


# api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
# 根据经纬度获取天气信息
def get_weather(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    # print(data)
    return data

# {
	# 	'dt': 1716033600,
	# 	'main': {
	# 		'temp': 294.59,
	# 		'feels_like': 294.59,
	# 		'temp_min': 294.59,
	# 		'temp_max': 294.59,
	# 		'pressure': 1013,
	# 		'sea_level': 1013,
	# 		'grnd_level': 1012,
	# 		'humidity': 69,
	# 		'temp_kf': 0
	# 	},
	# 	'weather': [{
	# 		'id': 800,
	# 		'main': 'Clear',
	# 		'description': 'clear sky',
	# 		'icon': '01n'
	# 	}],
	# 	'clouds': {
	# 		'all': 0
	# 	},
	# 	'wind': {
	# 		'speed': 4.47,
	# 		'deg': 129,
	# 		'gust': 9.97
	# 	},
	# 	'visibility': 10000,
	# 	'pop': 0,
	# 	'sys': {
	# 		'pod': 'n'
	# 	},
	# 	'dt_txt': '2024-05-18 12:00:00'
	# },
# 处理数据
def handle_data(data):
    dailyDataList = []
    lowestTempToday = 1000
    highestTempToday = 0
    dateToday = data['list'][0]['dt_txt'].split(' ')[0]
    # 遍历data['list']，获取每天的最低温度和最高温度，以及天气情况
    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]
        if date == dateToday:
            temp = item['main']['temp']
            if temp < lowestTempToday:
                lowestTempToday = temp
            if temp > highestTempToday:
                highestTempToday = temp
        else:
            # 由于温度数据使用的是绝对温度，所以需要转换为摄氏度
            lowestTempToday = round(lowestTempToday - 273.15, 2)
            highestTempToday = round(highestTempToday - 273.15, 2)
            dailyDataList.append({
                'date': dateToday,
                'lowestTemp': lowestTempToday,
                'highestTemp': highestTempToday,
            })
            dateToday = date
            lowestTempToday = 1000
            highestTempToday = 0
    print(dailyDataList)
    return dailyDataList
        


#测试获取经纬度
# print(get_location('shanghai'))

#测试获取天气信息
# get_weather(31.2222, 121.4581)

handle_data(get_weather(*get_location('胡志明')))