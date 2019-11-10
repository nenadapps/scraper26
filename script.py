import requests
from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):

    stamp = {}
    
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
        raw_text_cont = html.select('.product-description')[0]
        raw_text = raw_text_cont.select('p')[0].get_text().strip()
        stamp['raw_text'] = raw_text
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
                elif heading == 'Perforations':
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
        for item in html.select('.productitem--title a'):
            item_link = 'https://brixtonchrome.com' + item.get('href')
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
            stamp = get_details(page_item)
