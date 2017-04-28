import  requests
import re
import os
def get_one_html(page,images_list):
    cstart = 10
    cend = 20
    web_yidian = 1493340241177
    text = '&infinite=true&refresh=1&multi=5&appid='
    #path = 'xiaomiimage'
    base_url = 'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=12481888472&'
    for i in range(0,page):

        print ('open pages'+str(i))
        url = base_url+'cstart='+str(cstart+i*10)+'&cend='+str(cend+i*10)+text+'web_yidian&_='+str(web_yidian+i)
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            get_page_url(response.text,images_list)
        except:
            return None


def get_page_url(html,images_list):
    pattern = re.compile('"image":"(.*?)",')
    items = re.findall(pattern,html)
    for item in items:
        images_list.append(item)

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

def main():
    images_list=[]
    page = 100
    path='XiaoMi'
    get_one_html(page,images_list)
    image_path=""
    mkdir(path)
    i=1
    for image_url in images_list:
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
    main()