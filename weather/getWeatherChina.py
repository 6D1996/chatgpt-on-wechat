# 通过高德api获取明日天气
# https://restapi.amap.com/v3/weather/weatherInfo?parameters
import requests


myGaoDeKey = '8806b998dcd760300782478d4b734d9d'

def get_weather_tomorrow(cityCode):
    url = f'https://restapi.amap.com/v3/weather/weatherInfo?city={cityCode}&key={myGaoDeKey}&extensions=all'
    response = requests.get(url)
    data = response.json()
    # print(data)
    return data
# {'date': '2024-05-17', 'week': '5', 'dayweather': '阴', 'nightweather': '多云', 'daytemp': '21', 'nighttemp': '17', 'daywind': '南', 'nightwind': '南', 'daypower': '1-3', 'nightpower': '1-3', 'daytemp_float': '21.0', 'nighttemp_float': '17.0'}
# 仅展示明日天气，且用通俗易懂的方式输出文本
# “今天是2024年5月18日 星期*，青岛明日天气晴朗，17~21℃，东南风1到3级。”
def show_weather(data):
    city = data['forecasts'][0]['city']
    tomorrow = data['forecasts'][0]['casts'][1]
    dateToday = data['forecasts'][0]['casts'][0]['date']
    week = ['一', '二', '三', '四', '五', '六', '日'][int(tomorrow['week'])-1]
    # 转成中文年月日
    dateToday = dateToday.split('-')
    dateToday = f"{dateToday[0]}年{dateToday[1]}月{dateToday[2]}日，星期{week}"
    desc = tomorrow['dayweather']
    # 如果白天和晚上天气不一样，加上晚上的天气
    if tomorrow['dayweather'] != tomorrow['nightweather']:
        desc += '转' + tomorrow['nightweather']
    temp = f"{tomorrow['nighttemp']}~{tomorrow['daytemp']}℃" 

    # 风力最小值,取白天和晚上的最小值
    powerLow = min(int(tomorrow['daypower'].split('-')[0]), int(tomorrow['nightpower'].split('-')[0]))
    # 风力最大值,取白天和晚上的最大值
    powerHigh = max(int(tomorrow['daypower'].split('-')[1]), int(tomorrow['nightpower'].split('-')[1]))

    wind = tomorrow['daywind']+'风'
    # 如果白天和晚上风向不一样，加上晚上的风向
    if tomorrow['daywind'] != tomorrow['nightwind']:
        wind += '转' + tomorrow['nightwind'] + '风,'
        wind += f'风力{powerLow}到{powerHigh}级'
    else:
        wind += f'{powerLow}到{powerHigh}级'

    return f"今天是{dateToday}，{city}明日天气{desc}，{temp}，{wind}。"
        
    


# 测试上海浦东
# get_weather_tomorrow('310115')

# 测试北京
print(show_weather(get_weather_tomorrow('110000')))