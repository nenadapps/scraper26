# brixton
import requests
from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
'''
from fake_useragent import UserAgent
import os
import sqlite3
import shutil
from stem import Signal
from stem.control import Controller
import socket
import socks
import requests

controller = Controller.from_port(port=9051)
controller.authenticate()

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor():
    controller.signal(Signal.NEWNYM)
    
UA = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')
hdr = {'User-Agent': UA.random}
'''
hdr = {'User-Agent': 'Mozilla/5.0'}

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers=hdr)
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    if '.jpg' in url:
        stamp['images'] = [url]
    else: 
        try:
            html = get_html(url)
        except:
            return stamp

        try:
            title = html.select('.product-title')[0].get_text().strip()
            stamp['title'] = title
        except: 
            stamp['title'] = None
        try:
            price = html.select('.price--main .money')[0].get_text().strip()
            stamp['price'] = price.replace('CAD', '').replace('$', '').strip()
        except: 
            stamp['price'] = None

        try:
            watermarks_perfs = []
            trs = html.select('.product-description table tr')
            for tr in trs:
                tds = tr.select('td')
                watermarks_perf = []
                for td in tds:
                    td_text = td.get_text().strip()
                    watermarks_perf.append(td_text)
                watermarks_perfs.append(watermarks_perf) 
            stamp['watermarks_perfs'] = str(watermarks_perfs)
        except: 
            stamp['watermarks_perfs'] = None


        try:
            category_cont = html.select('.breadcrumbs-container')[0]
            category = category_cont.select('a')[1].get_text().strip()
            stamp['category'] = category
        except:
            stamp['category'] = None    

        stamp['currency'] = "CAD"

        # image_urls should be a list
        images = []                    
        try:
            image_items = html.select('.product-galley--image-background')
            for image_item in image_items:
                img_temp = image_item.get('data-image')
                img_parts = img_temp.split('?') 
                img = img_parts[0].replace('//', 'https://')
                if img not in images:
                    images.append(img)
        except:
            pass

        stamp['image_urls'] = images 

        try:
            raw_text = html.select('.product-description')[0].get_text().strip()
            stamp['raw_text'] = raw_text.replace('\xa0',' ').replace('\n', ' ')
        except:
            stamp['raw_text'] = None

        if stamp['raw_text'] == None and stamp['title'] != None:
            stamp['raw_text'] = stamp['title']

        centering_margins = ''  
        paper_freshness = '' 
        colour = ''
        impression = ''
        absence_paper_flaws = ''
        perfs = ''

        try:
            items = html.select('.product-description p')
            for item in items:
                item_value = item.get_text().strip()
                if ':' in item_value:
                    items_parts = item_value.split(':')
                    heading = items_parts[0].strip()
                    value = items_parts[1].strip()
                    if heading == 'Centering/margins':
                        centering_margins = value
                    elif heading == 'Paper freshness':
                        paper_freshness = value 
                    elif heading == 'Colour':
                        colour = value 
                    elif heading == 'Impression':
                        impression = value 
                    elif heading == 'Absence of visible paper flaws':
                        absence_paper_flaws = value 
                    elif 'Perforations' in heading:
                        perfs = value     
        except: 
            pass

        stamp['centering_margins'] = centering_margins
        stamp['paper_freshness'] = paper_freshness
        stamp['colour'] = colour
        stamp['impression'] = impression
        stamp['absence_paper_flaws'] = absence_paper_flaws
        stamp['perfs'] = perfs

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):
    
    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.productitem'):
            item_cont = item.select('.productitem--title a')[0]
            item_href = item_cont.get('href')
            if '-auction' not in item_href: 
                item_link = 'https://brixtonchrome.com' + item_href
            else:
                item_cont = item.select('.productitem--image-alternate')[0]
                item_link_temp = item_cont.get('src')
                item_link_parts = item_link_temp.split('?')
                item_link = item_link_parts[0].replace('//', 'https://')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        next_url_elem = html.select('.pagination--next a')[0]
        if next_url_elem:
            next_url = 'https://brixtonchrome.com' + next_url_elem.get('href')
    except:
        pass   
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_subcategories(category):
    
    items = []

    try:
        html = get_html(category)
    except:
        return items

    try:
        for item in html.select('.collection-item__title'):
            item_link = 'https://brixtonchrome.com' + item.get('href')
            if item_link not in items:
                items.append(item_link)
    except: 
        pass
    
    shuffle(items)
    
    return items
'''
def file_names(stamp):
    file_name = []
    rand_string = "RAND_"+str(randint(0,100000000))
    file_name = [rand_string+"-" + str(i) + ".png" for i in range(len(stamp['image_urls']))]
    print (file_name)
    return(file_name)

def query_for_previous(stamp):
    # CHECKING IF Stamp IN DB
    os.chdir("/Volumes/Stamps/")
    conn1 = sqlite3.connect('Reference_data.db')
    c = conn1.cursor()
    col_nm = 'url'
    col_nm2 = 'raw_text'
    unique = stamp['url']
    unique2 = stamp['raw_text']
    c.execute('SELECT * FROM brixton WHERE {cn} == "{un}" AND {cn2} == "{un2}"'.format(cn=col_nm, cn2=col_nm2, un=unique, un2=unique2))
    all_rows = c.fetchall()
    conn1.close()
    price_update=[]
    price_update.append((stamp['url'],
    stamp['raw_text'],
    stamp['scrape_date'], 
    stamp['price'], 
    stamp['currency']))
    
    if len(all_rows) > 0:
        print ("This is in the database already")
        conn1 = sqlite3.connect('Reference_data.db')
        c = conn1.cursor()
        c.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        try:
            conn1.commit()
            conn1.close()
        except:
            conn1.commit()
            conn1.close()
        print (" ")
        sleep(randint(10,45))
        next_step = 'continue'
    else:
        os.chdir("/Volumes/Stamps/")
        conn2 = sqlite3.connect('Reference_data.db')
        c2 = conn2.cursor()
        c2.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        try:
            conn2.commit()
            conn2.close()
        except:
            conn2.commit()
            conn2.close()
        next_step = 'pass'
    print("Price Updated")
    return(next_step)

def db_update_image_download(stamp): 
    req = requests.Session()
    directory = "/Volumes/Stamps/stamps/brixton/" + str(datetime.datetime.today().strftime('%Y-%m-%d')) +"/"
    image_paths = []
    names = file_names(stamp)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    image_paths = [directory + names[i] for i in range(len(names))]
    for item in range(1,len(names)):
        print (stamp['image_urls'][item])
        try:
            imgRequest1=req.get(stamp['image_urls'][item],headers=hdr, timeout=60, stream=True)
        except:
            print ("waiting...")
            sleep(randint(3000,6000))
            print ("...")
            imgRequest1=req.get(stamp['image_urls'][item], headers=hdr, timeout=60, stream=True)
        if imgRequest1.status_code==200:
            with open(names[item],'wb') as localFile:
                imgRequest1.raw.decode_content = True
                shutil.copyfileobj(imgRequest1.raw, localFile)
                sleep(randint(18,30))
    stamp['image_paths']=", ".join(image_paths)
    database_update =[]
    # PUTTING NEW STAMPS IN DB
    database_update.append((
        stamp['url'],
        stamp['raw_text'],
        stamp['title'],
        stamp['category'],
        stamp['watermarks_perfs'],
        stamp['centering_margins'],
        stamp['paper_freshness'],
        stamp['colour'],
        stamp['impression'],
        stamp['absence_paper_flaws'],
        stamp['perfs'],
        stamp['scrape_date'],
        stamp['image_paths']))
    os.chdir("/Volumes/Stamps/")
    conn = sqlite3.connect('Reference_data.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("""INSERT INTO brixton ('url','raw_text', 'title','category',
    'watermarks_perfs','centering_margins','paper_freshness','colour','impression','absence_paper_flaws','perfs','scrape_date','image_paths') 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", database_update)
    try:
        conn.commit()
        conn.close()
    except:
        conn.commit()
        conn.close()
    print ("all updated")
    print ("++++++++++++")
    print (" ")
    sleep(randint(45,140)) 

connectTor()
count = 0
'''
categories = {
     'https://brixtonchrome.com/pages/canadian-stamps',
     'https://brixtonchrome.com/pages/nigerian-stamps',
     'https://brixtonchrome.com/pages/other-countries',
     'https://brixtonchrome.com/pages/stamps-by-topic',
     'https://brixtonchrome.com/collections/previous-weekly-auction'
}
    
for category in categories:
    print(category) 

selection = input('Choose category: ')
           
subcategories = get_subcategories(selection)
for subcategory in subcategories:
    page_url = subcategory
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            '''
            count += 1
            if count > randint(100, 256):
                print('Sleeping...')
                sleep(randint(600, 4000))
                hdr['User-Agent'] = UA.random
                renew_tor()
                connectTor()
                count = 0
            else:
                pass'''
            stamp = get_details(page_item)
            '''
            if stamp['price']==None or stamp['price']=='':
                sleep(randint(500,700))
                continue
            next_step = query_for_previous(stamp)
            if next_step == 'continue':
                print('Only updating price')
                continue
            elif next_step == 'pass':
                print('Inserting the item')
                pass
            else:
                break
            db_update_image_download(stamp)'''
print('Scrape Complete')
