import requests
import re


# 下载网页
def get_html_text(url):
    try:
        r = requests.get(url, timeout=30)
        # r.raise_for_status()方法内部判断r.status_code是否等于200不需要增加额外的if语句，该语句便于利用try-except进行异常处理。
        r.raise_for_status()
        # r.encoding    从HTTP header中猜测的响应内容的编码方式
        # r.apparent_encoding	从内容中分析响应内容的编码方式(备选编码方式)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# 解析网页并保存数据
def parse_page(html):
    try:
        # "view_price":"148.00"
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        # "raw_title":"广州酒家 双黄纯白莲蓉月饼广式中秋月饼礼盒750g送礼员工福利"
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        # "item_loc":"浙江 杭州"
        loc = re.findall(r'\"item_loc\"\:\".*?\"', html)
        # "view_sales":"24482人付款"
        sale = re.findall(r'\"view_sales\"\:\".*?\"', html)

        for i in range(len(plt)):
            # eval() 函数用来执行一个字符串表达式，并返回表达式的值。
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            location = eval(loc[i].split(':')[1])
            location = location.split(' ')[0]
            sales = eval(sale[i].split(':')[1])
            sales = re.match(r'\d+', sales).group(0)
            print(price)
            with open("月饼数据.txt", 'a', encoding='utf-8')as f:
                print(f)
            f.write(title + ',' + price + ',' + sales + ',' + location + '\n')
    except:
        print("")


def main():
    goods = "月饼"
    depth = 10
    start_url = 'https://s.taobao.com/search?q=' + goods
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(4 * i)
            print('url=', url)
            html = get_html_text(url)
            parse_page(html)
        except:
            continue


main()
