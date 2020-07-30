# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import pandas as pd
from people.settings import CSV_FILE


def clean(item):
    item = re.sub(' {2,}', '', item)
    item = item.replace('\n','')
    item = item.replace('\r','')
    return item

import csv
class PeoplePipeline(object):
    items =0


    def __init__(self):

        parsed = pd.read_csv(CSV_FILE)

        if parsed.empty:

            self.file = open(CSV_FILE, 'w', newline='\n')
            self.writer = csv.DictWriter(self.file, fieldnames=[
                'Url to the employe profile',
                'Photo url',
                'Full name',
                'Position',
                'Phone numbers',
                'Email',
                'Services',
                'Sectors',
                "Publications",
                "Person brief",
                "DateTime of scraping the profile"
            ])
            self.writer.writeheader()
        else:
            self.file = open(CSV_FILE, 'a', newline='\n')
            self.writer = csv.DictWriter(self.file, fieldnames=[
                'Url to the employe profile',
                'Photo url',
                'Full name',
                'Position',
                'Phone numbers',
                'Email',
                'Services',
                'Sectors',
                "Publications",
                "Person brief",
                "DateTime of scraping the profile"
            ])
            self.items=len(parsed)

    def process_item(self, item, spider):

        self.items+=1
        item['Sectors'] = ", ".join(set(i for i in (clean(i) for i in item['Sectors']) if i))
        item['Services'] = ", ".join(set(i for i in (clean(i) for i in item['Services']) if i))
        item['Phone numbers'] = ", ".join(set(i for i in item['Phone numbers'] if i!='+'))
        item['Publications'] = " ".join(clean(i) for i in item['Publications']).replace('View less...','')
        item['Email'] = item['Email'].replace('mailto: ', '')
        item['Photo url']='https://www.morganlewis.com'+item['Photo url']
        self.writer.writerow(item)
        print(item)
        print(self.items)

        return item

    def close_spider(self, spider):
        self.file.close()



