import  requests
import re
import os
from const import *
import multiprocessing

def get_one_html(page):
    text = '&infinite=true&refresh=1&multi=5&appid='
    #path = 'xiaomiimage'
    base_url = 'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=12481888472&'

    print ('open pages'+str(page))
    url = base_url+'cstart='+str(CSTART+page*10)+'&cend='+str(CEND+page*10)+text+'web_yidian&_='+str(web_yidian+page)
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        return response.text

    except:
        return None


def get_page_url(html):
    pattern = re.compile('"image":"(.*?)",')
    items = re.findall(pattern,html)
    return items

def downlode_image(url,file_name):

    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        data = response.content
        f = open(file_name, 'wb')
        f.write(data)
        f.close()
    except:
        print 'downlode image error'


def mkdir(path):
    path = path.strip()
    isExist = os.path.exists(path)
    if not  isExist:
        os.mkdir(path)
    else:
        print 'path is exist '

def main(page):
    path='XiaoMi'
    html = get_one_html(page)
    items_url = get_page_url(html)
    image_path=""
    mkdir(path)
    i=1
    for image_url in items_url:
        image_name = image_url.split('/')
        name = image_name[-1]
        if name[-4:] =='.jpg':
            image_path = path+'/'+name
        else:
            image_path = path+'/'+name+'.jpg'
        downlode_image(image_url,image_path)
        print 'down load image'+str(i)
        i += 1

if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=5)

    for x in range(PAGE_START,PAGE_END+1):
        page =x
        pool.apply_async(main, (page, ))

    pool.close()
    pool.join()

