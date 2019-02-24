import requests
from bs4 import BeautifulSoup
import json


def parser(html, items):
    soup = BeautifulSoup(html, 'html.parser')
    even = soup.select('.even')
    odd = soup.select('.odd')
    str = odd + even  # 字符串拼接
    for item in str:  # for循环迭代(遍历)
        _item = {}
        _item['name_of_work'] = item.select('td')[0].get_text()
        _item['link_of_work'] = 'https://hr.tencent.com/' + item.select('td a')[0].attrs['href']
        _item['category_of_work'] = item.select('td')[1].get_text()
        _item['where_of_work'] = item.select('td')[3].get_text()
        _item['time_of_release'] = item.select('td')[4].get_text()
        _item['number_of_person'] = item.select('td')[2].get_text()
        items.append(_item)


def load_request(number, items, keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
    response = requests.get(
        'https://hr.tencent.com/position.php?keywords=' + str(keyword) + '&lid=0&tid=0&start=' + str(number) + '#a',
        headers=headers)
    html = response.text
    parser(html, items)


if __name__ == "__main__":
    number = 0
    items = []
    # switch = False
    keyword = 'java'
    while number <= 460:
        # swith相当于一个开关请示，如果请求发出，爬虫启动
        load_request(number, items, keyword)
        # 一次性爬取10页数据
        number += 10
    content = json.dumps(items, ensure_ascii=False, indent=4, sort_keys=True)
    # 数据读入json中
    with open('mytxzhaopin.json', 'w+', encoding='utf-8') as f:
        f.write(content)
