# -*- coding: utf-8 -*-
from __future__ import unicode_literals

UTF8_ENCODING = 'utf-8'

import sys
reload(sys)
sys.setdefaultencoding(UTF8_ENCODING)

import scrapy
import neukolln.spiders
from neukolln.items import ImmoItem

import logging
logger = logging.getLogger()

import re
#from neukolln.utils import get_iso3166_alpha2_from_fr_input
#from luxresidence.mhelpers import extract_from, get_item

class LuxresidenceSpider(neukolln.spiders.NeukollnBaseSpider, scrapy.Spider):
    name='luxeresidence202009'
    allowed_domains = ['lux-residence.com']  # FIXME

    # Outputs
    neukolln_export_to_json = False
    neukolln_export_to_csv = True
    neukolln_export_to_tab = False

    start_urls = ['http://www.lux-residence.com/fr/annonces/vente/propriete-PROVENCE+ALPES+COTE+D%27AZUR.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-ILE+DE+FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-RHONE+ALPES.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-LANGUEDOC+ROUSSILLON.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-AQUITAINE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-POITOU+CHARENTES.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-MIDI+PYRENEES.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-BRETAGNE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-PAYS+DE+LA+LOIRE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-CENTRE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-BASSE+NORMANDIE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-PICARDIE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-CORSE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-BOURGOGNE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-NORD+PAS+DE+CALAIS.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-AUVERGNE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-HAUTE+NORMANDIE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-LORRAINE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-ALSACE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-LIMOUSIN.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-CHAMPAGNE+ARDENNE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-FRANCHE+COMTE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/hotel-particulier-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/appartement-neuf-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/loft-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/chateau-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/propriete-viticole-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/chalet-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/bastide-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immeuble-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/appartement-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/terrain-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-SUISSE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-BELGIQUE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-GRANDE+BRETAGNE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-ESPAGNE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-MAROC.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-CARAIBES.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-ETATS+UNIS.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-CROATIE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-LUXEMBOURG.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-CANADA.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-GRECE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-ALLEMAGNE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-ITALIE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-MONACO.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-PORTUGAL.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-BALI.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-THAILANDE.php',
         'http://www.lux-residence.com/fr/annonces/vente/immobilier-prestige-SAINT+BARTHELEMY.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-ILE+DE+FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-RHONE+ALPES.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-LANGUEDOC+ROUSSILLON.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-AQUITAINE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-POITOU+CHARENTES.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-MIDI+PYRENEES.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-BRETAGNE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-PAYS+DE+LA+LOIRE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-CENTRE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-BASSE+NORMANDIE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-PICARDIE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-CORSE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-BOURGOGNE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-NORD+PAS+DE+CALAIS.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-AUVERGNE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-HAUTE+NORMANDIE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-LORRAINE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-ALSACE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-LIMOUSIN.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-CHAMPAGNE+ARDENNE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-FRANCHE+COMTE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/hotel-particulier-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/appartement-neuf-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/loft-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/chateau-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/propriete-viticole-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/chalet-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/bastide-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/immeuble-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/appartement-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/terrain-FRANCE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-SUISSE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-BELGIQUE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-GRANDE+BRETAGNE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-ESPAGNE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-MAROC.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-CARAIBES.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-ETATS+UNIS.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-CROATIE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-LUXEMBOURG.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-CANADA.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-GRECE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-ALLEMAGNE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-ITALIE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-MONACO.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-PORTUGAL.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-BALI.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-THAILANDE.php',
         'http://www.lux-residence.com/fr/annonces/location/immobilier-prestige-SAINT+BARTHELEMY.php'
    ]


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

    total_ads = 0

    def __init__(self, *args, **kwargs):
        super(LuxresidenceSpider, self).__init__(*args, **kwargs)
        # ...

    def response_is_ban(self, request, response):
        # use default rules, but also consider HTTP 200 responses
        # a ban if there is 'captcha' word in response body.
        ban = super(LuxresidenceSpider, self).response_is_ban(request, response)
        # ban = ban or 'captcha' in response.body.lower()
        return ban

    # def start_requests(self):
    #     # override start_urls!!!
    #     url = 'http://www.lux-residence.com/fr/sitemap.php'
    #     yield scrapy.Request(url,headers=self.headers, callback=self.parse_site_map)



    # def parse(self, response):
    #     # site map links: print(response.xpath('//*[@id="content"]/div/div[3]').css('li::attr(href)').extract())



    def parse(self, response):
        for url_list in response.css('.pagination a::attr(href)').extract():
            if url_list != '#':
                yield scrapy.Request(url_list,headers=self.headers, callback=self.parse)
        for url_detail in response.css('a.btn-inverse::attr(href)').extract():
            item = ImmoItem()
            item['PAYS_AD'] = "FR"
            for key, value in self.countries.items():
                print(response.request.url)
                if key in response.request.url:
                    print("_________________________________________")
                    print(response.request.url)
                    item['PAYS_AD'] = value
                    print(item['PAYS_AD'])
                    print("_________________________________________")
            print(url_detail)
            self.total_ads = self.total_ads + 1
            print("total =================> " + str(self.total_ads))
            yield scrapy.Request(url_detail,headers=self.headers, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self,response):
        item = response.meta['item']
        item['ANNONCE_TEXT'] = response.xpath("//p[@itemprop='description']/text()").extract_first()
        item['ANNONCE_LINK'] = response.url
        item['ID_CLIENT'] = response.url.split("/")[-2]
        item['FROM_SITE'] = "http://www.lux-residence.com/"
        item['DEPARTEMENT']=response.url.split('/')[7]
        item['CP']= str(item['DEPARTEMENT'])+"000"
        title = response.css('title::text').extract_first()
        if "Location longue" in title:
            item['ACHAT_LOC'] = "2"
        if "Vente" in title:
            #item['ACHAT_LOC'] = "2"
            item['ACHAT_LOC'] = "1"
        if "Location saison" in title:
            item['ACHAT_LOC'] = "8"
        item['CATEGORIE'] = response.xpath('//*[@id="product"]/div/div/div[3]/div[2]/div[2]/ul/li[1]/p/span/text()').extract_first()
        if "neuf" in item['CATEGORIE']:
            item['NEUF_IND'] = "Y"
        else:
            item['NEUF_IND'] = "N"
        item['NOM'] = title
        item['ADRESSE'] = response.xpath("//span[@itemprop='address']/text()").extract_first()
        #item['VILLE'] = response.xpath('//*[@id="ad-head"]/div/div/div[1]/div/ul/li[3]/a/span/text()').extract_first()
	item['VILLE'] = response.xpath('//p[@class="tag-line"]/span/text()').extract_first()
        #item['REGION'] = response.xpath('//*[@id="ad-head"]/div/div/div[1]/div/ul/li[2]/a/span/text()').extract_first()
        try:
            item['M2_TOTALE'] = re.search('(?<=Surface habitable : <span class="li-info">).*?(?= m)', response.body_as_unicode()).group(0)
        except Exception as e:
            print(str(e))
	
        try:
            item['SURFACE_TERRAIN'] = re.search('(?<=Terrain : <span class="li-info">).*?(?= m)', response.body_as_unicode()).group(0)
        except Exception as e:
            print(str(e))
	
        try:
            item['PHOTO'] = len(response.css('.carousel-inner img'))
        except Exception as e:
            print(str(e))
        
        try:
            item['PIECE'] = re.search('(?<=Pièces : <span class="li-info">).*?(?=<)', response.body_as_unicode()).group(0)
            #item['PIECE']= re.search('(?<=Pi  ces : <span class="li-info">).*?(?=<)', response.body_as_unicode()) 
	except Exception as e:
            print(str(e))
        
        try:
            item['PRIX'] = re.sub('\D','',response.css('.price::text').extract_first())
        except Exception as e:
            print(str(e))
        item['SELLER_TYPE'] = "Pro"
        item['PRO_IND'] = "Y"
        item['AGENCE_NOM'] = response.xpath("//p[@itemprop='seller']/span/text()").extract_first()
        try:
            item['AGENCE_ADRESSE'] = " ".join(response.xpath("//p[@itemprop='seller']/text()").extract())
        except Exception as e:
            print(str(e))
        try:
            #item['AGENCE_CP'] = re.sub('\D','',response.xpath("//p[@itemprop='seller']/text()").extract()[1])
	    #agence_cp = response.xpath('//p[@class="adress"]/text()').extract_first()
	    agence_cp = response.xpath('//p[@class="adress"]/text()').extract()[1]
	    if agence_cp:
	        agence_cp = ''.join([i for i in agence_cp if i.isdigit()])
	        item['AGENCE_CP'] = agence_cp
	    else:
	        item['AGENCE_CP'] = ''

	    #agence_cp = item['AGENCE_CP']
	    item['AGENCE_DEPARTEMENT'] = agence_cp[:2]
            #item['AGENCE_CP'] = re.sub('\D','',response.xpath("//p[@itemprop='seller']/text()").extract())
        except Exception as e:
            print(str(e))
        try:
            item['AGENCE_VILLE'] = re.sub('\d+','',response.xpath("//p[@itemprop='seller']/text()").extract()[1]).strip()
            #item['AGENCE_VILLE']= re.sub('\d+','',response.xpath("//p[@itemprop='seller']/text()").extract())
        except Exception as e:
            print(str(e))

	agence_adresse = item['AGENCE_ADRESSE']

	#agence_adresse = row[37]
        '''
	if len(agence_adresse)<20 and len([x for x in agence_adresse if x.isdigit()]) <= 5:
                #agence_adresse = agence_adresse.replace('\"',"")
                #print agence_adresse
		agence_adresse = agence_adresse.split(' ')
		agence_cp = agence_adresse[0]
		agence_ville = agence_adresse[-1]
                #agence_cp = '"'+agence_cp+'"'
                #row[38] = '"'+agence_cp+'"'
                #row[39] = '"'+agence_ville+'"'
                #res=";".join(row)
                #print(res)
		item['AGENCE_CP'] = agence_cp
                #item['AGENCE_DEPARTEMENT'] = agence_cp[:2]
		item['AGENCE_VILLE'] = agence_ville
        '''

	'''
	row[39] = row[39].replace('\"BEAUSSET"','"'+"LE BEAUSSET"+'"').replace('\"CIOTAT"','"'+"LA CIOTAT"+'"').replace('\"TROPEZ"','"'+"ST TROPEZ"+'"')
	res=";".join(row)
	print(res)  
	'''

	'''
	#siren = response.xpath('//*[@id="ptog1"]/text()').extract_first()
	if siren :
		try:
			siren = siren.split(':')
			siren = siren[1].replace(' ','')
			item['SIREN'] = siren
		except:
			pass
	else:
		item['SIREN']= ""


	'''

	siren = response.xpath('//p[@class="tog-p"]/text()').extract_first()
	if siren is not None and len(siren)<=17 :
	    siren =''.join([i for i in siren if i.isdigit()])
	else:
	    siren =''

	item['SIREN'] = siren

	'''	
	surface_terrain1 = re.search('(?<=Terrain : <span class="li-info">).*?(?= m)', response.body_as_unicode()).group(0)
	surface_terrain2 = re.search('(?<=Surface habitable : <span class="li-info">).*?(?= m)', response.body_as_unicode()).group(0)
	if surface_terrain1:
		try:
			item['SURFACE_TERRAIN'] = surface_terrain1
		except:
			pass
	elif surface_terrain2:
		try:
			item['SURFACE_TERRAIN'] = surface_terrain2
		except:
			pass
	else:
		item['SURFACE_TERRAIN']= ''

	'''

        #item['WEBSITE'] = response.css('.agencyLink::text').extract_first()
	item['WEBSITE'] = response.xpath('//p[@class="def"]/a/text()').extract_first()
        item['NEUKOLLN_ORIGINAL_PHONE_AGENCE_TEL'] = response.css('.number::text').extract_first()
        item['NEUKOLLN_DEFAULT_CC_AGENCE_TEL'] = item['PAYS_AD']


        yield item
