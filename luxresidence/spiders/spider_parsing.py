# -*- coding: utf-8 -*-
from __future__ import unicode_literals

UTF8_ENCODING = 'utf-8'
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding(UTF8_ENCODING)
import json
import scrapy
import neukolln.spiders
from neukolln.items import ImmoItem
from ..items import LuxeresidenceItem
import logging
logger = logging.getLogger()
from scrapy import Request
import re
import random
class LuxresidenceSpider(neukolln.spiders.NeukollnBaseSpider, scrapy.Spider):
    name='luxeresidence202010'
    allowed_domains = ['lux-residence.com']

    neukolln_export_to_json = False
    neukolln_export_to_csv = True
    neukolln_export_to_tab = False
    start_urls = ["https://www.lux-residence.com/fr/vente.php"]

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    }

    countries = {
        'SUISSE' : 'CH',
        'BELGIQUE': 'BE',
        'GRANDE+BRETAGNE' :'GB',
        'ESPAGNE': 'ES',
        'MAROC': 'MA',
        'CARAIBES' : 'FR',
        'ETATS+UNIS': 'US',
        'CROATIE' : 'HR',
        'LUXEMBOURG' : 'LU',
        'CANADA' : 'CA',
        'GRECE' : 'GR',
        'ALLEMAGNE': 'DE',
        'ITALIE': 'IT',
        'MONACO': 'MC',
        'PORTUGAL': 'PT',
        'BALI': 'ID',
        'THAILANDE': 'TH',
        'SAINT+BARTHELEMY': 'FR'
    }

    def __init__(self, *args, **kwargs):
        super(LuxresidenceSpider, self).__init__(*args, **kwargs)

    def response_is_ban(self, request, response):
        ban = super(LuxresidenceSpider, self).response_is_ban(request, response)
        return ban

    def parse(self, response):
        new_liste = []
        start=list(pd.read_csv("/home/h.mahmoudi/Luxeresidence/Luxeresidence/spiders/outputs/20200629/data.csv")["url"])
        for url in start:
            new_liste.append("https://www.lux-residence.com/get/offer/fr/"+str(url))
        print("My data :",new_liste)
        for urle in new_liste:
             print("ANNONCE LINK to Parse:",urle)
             yield Request(urle, callback=self.parse_detail, meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [300,302,400,301, 404], 'cookiejar': random.randint(1,101000)} , headers={'User-Agent': 'Mozilla/5.0'})

    def parse_detail(self,response):
        item = LuxeresidenceItem()
        data = response.text
        datta = json.loads(data)
        item['PAYS_AD'] = "FR"
        item['ANNONCE_TEXT'] = datta["offer"]["Description"]["fr"].replace("\n","").replace(";","").replace(":","").replace(",","")
        item['ANNONCE_LINK'] = response.url
        item['ID_CLIENT'] = datta["offer"]["AdId"]
        item['FROM_SITE'] = "http://www.lux-residence.com/"
        item['DEPARTEMENT']= str(datta["offer"]["canonicalUrl"]["params"]["departmentZip"])
        item['CP']= str(item['DEPARTEMENT'])+"000"
        try:
            title = response.css('title::text').extract_first()
            if "Location longue" in title:
                item['ACHAT_LOC'] = "2"
            if "Vente" in title:
                item['ACHAT_LOC'] = "1"
            if "Location saison" in title:
                item['ACHAT_LOC'] = "8"
        except:
            pass
        try:
            item['CATEGORIE'] = str(datta["offer"]["hrefLangUrls"]["fr"]["params"]["propType"])
        except:
            pass
        try:
            if "neuf" in item['CATEGORIE']:
                item['NEUF_IND'] = "Y"
            else:
                item['NEUF_IND'] = "N"
        except:
            pass
        item['NOM'] = title
        item['ADRESSE'] = ""
	item['VILLE'] = str(datta["offer"]["canonicalUrl"]["params"]["town"]).replace("+"," ")
        item['REGION'] = str(datta["offer"]["canonicalUrl"]["params"]["region"]).replace("+"," ")
        try:
            item['M2_TOTALE'] = re.search('(?<=Surface habitable : <span class="li-info">).*?(?= m)', response.body_as_unicode()).group(0)
        except Exception as e:
            print(str(e))
        try:
            item['SURFACE_TERRAIN'] = re.search('(?<=Terrain : <span class="li-info">).*?(?= m)', response.body_as_unicode()).group(0)
        except Exception as e:
            print(str(e))
        try:
            photos = datta["offer"]["Photos"]
            item['PHOTO'] = str(photos[-1]["Order"])
        except Exception as e:
            print(str(e))
        try:
            item['PIECE'] = re.search('(?<=Pièces : <span class="li-info">).*?(?=<)', response.body_as_unicode()).group(0)
	except Exception as e:
            print(str(e))
        try:
            item['PRIX'] = datta["offer"]["Price"]["Raw"]
        except Exception as e:
            print(str(e))
        item['SELLER_TYPE'] = "Pro"
        item['PRO_IND'] = "Y"
        item['AGENCE_NOM'] = str(datta["offer"]["Agency"]["Name"])
        try:
            item['AGENCE_ADRESSE'] = str(datta["offer"]["Agency"]["Address"]["Street"]).replace("\n","").strip()
        except Exception as e:
            print(str(e))
        try:
            item['AGENCE_CP'] = str(datta["offer"]["Agency"]["Address"]["ZipCode"]).replace("\n","").strip()
        except Exception as e:
            print(str(e))

	    item['AGENCE_DEPARTEMENT'] = item['AGENCE_CP'][:2]
        except Exception as e:
            print(str(e))
        try:
            item['AGENCE_VILLE'] = str(datta["offer"]["Agency"]["Address"]["Locality2"]["name"]).replace("\n","").strip()
        except Exception as e:
            print(str(e))

	agence_adresse = item['AGENCE_ADRESSE']

	item['SIREN'] = str(datta["offer"]["Agency"]["Siren"]).replace("\n","").strip()
        item['AGENCE_TEL'] = str(datta["offer"]["Agency"]["PhoneNumber"]).replace("\n","").strip()
	item['WEBSITE'] = str(datta["offer"]["Agency"]["WebSiteUrl"]).replace("\n","").strip()
        #item['NEUKOLLN_ORIGINAL_PHONE_AGENCE_TEL'] = ""
        #item['NEUKOLLN_DEFAULT_CC_AGENCE_TEL'] = item['PAYS_AD']

        yield item

