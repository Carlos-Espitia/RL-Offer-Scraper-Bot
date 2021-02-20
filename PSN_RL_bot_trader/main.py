# importing the required libraries 

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * 
import sys 
import time
import webbrowser

#packages for program bot
import requests
import os
import sys
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv
from csv import reader
from playsound import playsound
import time
from colorama import Fore, Back, Style

#cloudflare
import cloudscraper

#Auto add feature 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 1. Subclass QRunnable thread 
# The main class for running long functions
class Runnable(QRunnable):
    def __init__(self):
        super().__init__()

    # Your long-running task goes here ...
    def run(self):
        #row variable for table window
        hits_table_row = 0

        global stop_bot
        #Settings
        #scam words
        scam_words = []
        with open(r'Filter\Scam words.txt', 'r', encoding='utf-8') as f:
            scam_words3 = f.readlines()
            for scam_words2 in scam_words3:
                scam_word = scam_words2.replace('\n', '')
                scam_words.append(scam_word)

        #white list offer
        white_list_itemsO = []
        with open(r'Filter\Whitelist offer words.txt', 'r', encoding='utf-8') as f:
            white_list_itemsO3 = f.readlines()
            for white_list_itemsO2 in white_list_itemsO3:
                white_list_itemO = white_list_itemsO2.replace('\n', '')
                white_list_itemsO.append(white_list_itemO)    

        #white list wants
        white_list_itemsW = []
        with open(r'Filter\Whitelist want words.txt', 'r', encoding='utf-8') as f:
            white_list_itemsW3 = f.readlines()
            for white_list_itemsW2 in white_list_itemsW3:
                white_list_itemW = white_list_itemsW2.replace('\n', '')
                white_list_itemsW.append(white_list_itemW)    

        #blacklist items offers/wants
        black_list_items = []
        with open(r'Filter\Backlist offer want words.txt', 'r', encoding='utf-8') as f:
            black_list_items3 = f.readlines()
            for black_list_items2 in black_list_items3:
                black_list_item = black_list_items2.replace('\n', '')
                black_list_items.append(black_list_item)

        trading_url = 'https://rocket-league.com/trading?filterItem=0&filterCertification=0&filterPaint=0&filterMinCredits=0&filterMaxCredits=100000&filterPlatform%5B%5D=2&filterSearchType=0&filterItemType=0'
        price_checker_url = 'https://rl.insider.gg/en/psn/'

        ##########################################################################
        #options
        options = webdriver.ChromeOptions()
        #uses my profile for logins
        options.add_argument(r"--user-data-dir=C:\Users\espitiahernandc24533\AppData\Local\Google\Chrome\User Data\Profile 1")

        path = "C:\Program Files (x86)\chromedriver.exe"
        if Auto_Add == True:
            driver = webdriver.Chrome(path, options=options)

        ##########################################################################

        Hits = 0
        Auto_Hits = 0

        Filtered_Offers = 0
        Offer_Errors = 0

        Num_Offers = 0
        Site_Reloads = 0

        os.system('cls')
        print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
        while True:
            #reset old offers
            open(r'HTML\html_offers.txt', 'w').close()

            #Use this code to check if cloadflare blocking the bot
            #scraper = cloudscraper.create_scraper()
            #print(scraper.get("https://rocket-league.com/trading?filterItem=0&filterCertification=0&filterPaint=0&filterMinCredits=0&filterMaxCredits=100000&filterPlatform%5B%5D=2&filterSearchType=0&filterItemType=0").text)

            #opening website
            try:
                trading_site = requests.get(trading_url)
            except Exception:
                print(Fore.YELLOW + "\nBot having connecton issues to site! Trying again in 3")
                time.sleep(1)
                print(Fore.YELLOW + "\nBot having connecton issues to site! Trying again in 2")
                time.sleep(1)
                print(Fore.YELLOW + "\nBot having connecton issues to site! Trying again in 1")
                time.sleep(1)
                print(Fore.YELLOW + "\nBot having connecton issues to site! Trying again in 0")
                time.sleep(.5)
                os.system('cls')
                print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
                if stop_bot == True:
                    enable_settings()
                    break
                continue

            #type of parsing
            trading_site_soup = BeautifulSoup(trading_site.content, 'html.parser')

            #Use this code to check if cloadflare blocking the bot
            #print(trading_site_soup)

            #parsing class dir
            trade_offers = trading_site_soup.findAll('div', {'class': 'rlg-trade'})
            #removing src tags from trade_offers
            regex2 = re.sub(r' src\S+', '', str(trade_offers)) 

            #importing html data to text file
            with open(r'HTML\html_data.txt', 'w', encoding="utf-8") as f:
                f.write(str(regex2))
                f.close()

            #                         trade link                Username                     Items user has                 Items user wants           Items in wants and has                   Item type                           Item type #2                   Item type #3                 blueprints in wants and has             Credits in wants and has                color circle image                  scam       
            regex = re.compile(r'(<li><a href="/trade/|<a class="rlg-trade__platform" href="|div class="rlg-trade__itemshas"|div class="rlg-trade__itemswants"|class="rlg-item__image"|class="rlg-item__name">\w+ \w+\W Inverted|class="rlg-item__name">\w+\W Inverted|class="rlg-item__name">\w+ [(]|src="/../content/media/items/avatar/|div class="rlg-item__quantity --quantity-|div class="rlg-item__paint|codes|build|bid|code|1v1|entry|1 vs 1|1vs1)')
            
            #filter types remove
            filter_types = ['(Global)']

            #import regex data to html_offers.txt
            for lines in open(r'HTML\html_data.txt', encoding='utf-8'):
                for match in re.finditer(regex, lines):
                    if not any(filter_types in lines for filter_types in filter_types):
                        with open(r'HTML\html_offers.txt', 'a', encoding="utf-8") as f:
                            f.write(lines)
                            f.close()
            
            #importing data and replacing text to be easily readable 
            main_url = 'https://rocket-league.com'
            with open(r'HTML\html_offers.txt', 'r', encoding="utf-8") as html_offers:
                offers_data = html_offers.read().replace('<li><a href="', '\n^Link : ' + main_url).replace('Trade details</a></li>', '\n^Note : ').replace('<a class="rlg-trade__platform" href="', '\n^========================^\nUsername: ').replace('" rel="noopener" style="order: 100;" target="_blank">', '').replace(' (', '(').replace('">', '').replace('"/>', '').replace('<div class="rlg-trade__itemshas', '^Offer:').replace('<div class="rlg-trade__itemswants', '^Wants:').replace('<img alt="', ' ~').replace(' " class="rlg-item__image"', '/').replace('<h2 class="rlg-item__name', 'Type:').replace('</h2>', '/').replace('blueprint" class="rlg-item__image"', 'blueprint/').replace('<div class="rlg-item__image', 'ColorSet/').replace('" class="rlg-item__set"', ' |').replace('<div class="rlg-item__quantity --quantity-', 'Q:').replace(' --premium wide', '').replace(' --uncommon', '').replace(' --premium', '').replace(' --rare', '').replace(' --import', '').replace(' --exotic', '').replace(' --limited', '').replace(' --very-rare', '').replace('--black-market', '').replace('superduperwide', '').replace('.png', '').replace('<div class="rlg-item__paint --painted-set" data-hex="ffffff" data-name="Painted set', '').replace('<div class="rlg-item__paint --', 'Clr:').replace('" data-hex="3F51B5" data-name="Cobalt', '/').replace('" data-hex="7FFF00" data-name="Lime', '/').replace('" data-hex="4CAF50" data-name="Forest Green', '/').replace('" data-hex="777777" data-name="Grey', '/').replace('" data-hex="F4B400" data-name="Orange', '/').replace('" data-hex="FF4081" data-name="Pink', '/').replace('" data-hex="9C27B0" data-name="Purple', '/').replace('" data-hex="FFEB3B" data-name="Saffron', '/').replace('" data-hex="03A9F4" data-name="Sky Blue', '/').replace('" data-hex="FFFFFF" data-name="Titanium White', '/').replace('" data-hex="D50000" data-name="Crimson', '/').replace('" data-hex="111111" data-name="Black', '/').replace('" data-hex="4C1100" data-name="Burnt Sienna', '/').replace('\n', '')
                with open("offers.txt", "w", encoding='utf-8') as offers_txt:
                    offers_txt.write(offers_data)
                    offers_txt.close()
            
            #fix car types
            #note add code for fix types with color and blueprints
            string_types_replace_edit = re.compile(r'(Type:\w+ \w+: |Type:\w+: |Type:\w+)')
            item_types = re.compile(r'(~\w+ blueprint/Clr:\w+-\w+/[(]\w+[)]|~\w+ blueprint/[(]\w+[)]|~\w+/Clr:\w+/[(]\w+ \w+[)]/|~\w+/Clr:\w+/[(]\w+ \d+[)]/|~\w+/Clr:\w+-\w+/[(]\w+[)]/|~\w+/Clr:\w+/[(]\w+[)]/|~\w+/[(]\w+ \d+[)]/|~\w+/[(]\w+ \w+-\w+[)]/|~\w+/[(]\w+[)]/)')
            types = re.compile(r'([(]\w+[)]|[(]\w+ \w+[)]|[(]\w+ \d+[)]|[(]\w+ \w+-\w+[)])')

            #remove "Type:Fennec(Fennec)" -> "(Fennec)"
            with open('offers.txt', 'r', encoding='utf-8') as f:
                list_text = f.readlines()
                line = ''.join(map(str, list_text)) 
                f.close()
                for edit in re.findall(string_types_replace_edit, line):
                    #removes "Types:"
                    with open('offers.txt', 'r', encoding='utf-8') as f2:
                        offers_data = f2.read().replace(edit, '').replace(' Blueprint', '')
                        #fix car location
                        for item_type in re.findall(item_types, offers_data):
                            for item_type2 in re.findall(types, item_type):
                                item_type_edit = item_type2.replace('(', '').replace(')', '')
                                item_type_edit2 = '~' + item_type_edit + ' '
                                #del slash end of (Fennec)"/"
                                del_slash = item_type2 + '/'
                                item_type_edit3 = item_type.replace('~', item_type_edit2).replace(del_slash, '')
                                offers_data2 = offers_data.replace(item_type, item_type_edit3)

                                with open('offers.txt', 'w', encoding='utf-8') as f3:
                                    f3.write(offers_data2)
                                    f3.close()

            #fix inverted items
            inverted_item_only = re.compile(r'(~\w+ \w+|~\w+)')
            inverted_item = re.compile(r'(~\w+ \w+/Clr:\w+-\w+/Inverted/|~\w+/Clr:\w+-\w+/Inverted/|~\w+ \w+/Clr:\w+/Inverted/|~\w+/Clr:\w+/Inverted/|~\w+/Inverted/)')
            inverted_type = re.compile(r'(Type:\w+ \w+: |Type:\w+: )')
            
            #fix inverted items
            with open('offers.txt', 'r', encoding='utf-8') as f:
                #remove Types for inverted items
                for inverted_type2 in re.findall(inverted_type, f.read()):
                    #print(inverted_type2)
                    with open('offers.txt', 'r', encoding='utf-8') as f2:
                        inverted_edit = f2.read().replace(inverted_type2, '')
                        with open('offers.txt', 'w', encoding='utf-8') as f3:
                            f3.write(inverted_edit)
                            f3.close()
            
            #fix inverted items
            with open('offers.txt', 'r', encoding='utf-8') as f:
                for inverted_item2 in re.findall(inverted_item, f.read()):
                    #print(inverted_item2)
                    for inverted_item3 in re.findall(inverted_item_only, inverted_item2):
                        #print(inverted_item3)
                        with open('offers.txt', 'r', encoding='utf-8') as f2:
                            inverted_edit2 = f2.read().replace('/Inverted/', '/').replace(inverted_item3, inverted_item3 + ' Inverted').replace('Inverted Inverted', 'Inverted')
                            with open('offers.txt', 'w', encoding='utf-8') as f3:
                                f3.write(inverted_edit2)
                                f3.close()
            
            camo_type = re.compile(r'(Type:\w+[(]\w+[)]/)')
            camo_item = re.compile(r'(~\w+[(]\w+[)]/)')

            with open('offers.txt', 'r', encoding='utf-8') as f:
                list_text = f.readlines()
                line = ''.join(map(str, list_text)) 
                f.close()
                #remove Types for inverted items
                for camo_type2 in re.findall(camo_type, line):
                    #print(camo_type2)
                    line2 = line.replace(camo_type2, '')
                    for camo_item in re.findall(camo_item, line2):
                        camo_item_new = camo_item.replace('(', ' ').replace(')', '')
                        line3 = line2.replace(camo_item, camo_item_new)
                        with open('offers.txt', 'w', encoding='utf-8') as f3:
                            f3.write(line3)
                            f3.close()

            #1 line to \n all lines
            with open('offers.txt', 'r', encoding='utf-8') as f:
                offers = f.read().replace('^', '\n')
                with open('offers.txt', 'w', encoding='utf-8') as f2:
                    f2.write(offers)
                    f2.close()         

            #importing offers to pandas
            links = []
            Note = []
            usernames = []
            items_offer = []
            items_want = []

            #import usernames to list
            with open('offers.txt', encoding='utf-8') as f:
                for line in f.readlines():
                    if re.search(r'Link :', line):
                        links.append(line)
                    if re.search(r'Note : ', line):
                        Note.append(line)
                    if re.search(r'Username:', line):
                        usernames.append(line)
                    if re.search(r'Offer:', line):
                        items_offer.append(line)
                    if re.search(r'Wants:', line):
                        items_want.append(line)

            #remove words from lists
            links2 = list(map(lambda x: str(x).replace('Link : ', '').replace('\n', ''), links)) 
            Note2 = list(map(lambda x: str(x).replace('Note : ', '| ').replace('\n', ''), Note))    
            usernames2 = list(map(lambda x: str(x).replace('Username: ', '').replace('\n', ''), usernames))
            items_offer2 = list(map(lambda x: str(x).replace('Offer: ', '').replace('\n', ''), items_offer))
            items_want2 = list(map(lambda x: str(x).replace('Wants: ', '').replace('\n', ''), items_want))
            try:
                offers_df = pd.DataFrame({'Links':links2,
                                'Note':Note2,
                                'Users':usernames2,
                                'Items_offer':items_offer2, 
                                'Items_want':items_want2})

                offers_df.to_csv(r'CSV\offers.csv')
            except Exception:
                #print("Weird array error!")
                pass

            #filter out offers with words 
            #These items have duplicated named items
            
            filter_offers = ['~JÃƒÂ¤ger 619', '~Veloce', '~Sunset 1986', '~Rad Rock', '~Peppermint', '~Stay Puft', 'ColorSet', '~Tunica', '~Neptune', '~Dot Matrix/ ', '~Lightning', '~Spyder', '~Standard/Clr:purple/', '~Sunburst', '~SARPBC', '~Ion/ ', '~Invader', '~League Legacy', '~Vortex', '~Tachyon III/ ', '~Spatial Rift/ ', '~Happy Holidays', '~Mister_monsoon', '~Mainframe', '~Gale-fire', '~Stern', '~OEM', '~Popcorn', '~3-Lobe/ ', '~Cold sweater', '~RLCS X', '~Dieci', '~Hammerhead', '~HoloData', '~Shattered', '~Reaper', '~Fireworks', '~Alchemist','~Credits offer', '~Offer', '~Non-Crate Rare offer', '~Non-Crate Exotic Offer', '~Import offer', '~Non-Crate Very Rare offer', '~Non-Crate Import Offer', '~Very Rare offer', '~Limited offer', '~Black Market offer', '~Exotic offer']

            with open(r'CSV\offers.csv', encoding='utf-8') as offers, open(r'CSV\offers2.csv', 'w',  encoding='utf-8') as offers2:
                for line in offers:
                    if not any(filter_offers in line for filter_offers in filter_offers):
                        if black_list_items_E == True:
                            if not any(black_list_items in line for black_list_items in black_list_items):
                                if scam_filter == True:
                                    if not any(scam_words in line for scam_words in scam_words):
                                        offers2.write(line)
                                        Filtered_Offers += 1
                                        Num_Offers += 1
                                        os.system('cls')
                                        print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
                                else:
                                    offers2.write(line)
                                    Filtered_Offers += 1
                                    Num_Offers += 1
                                    os.system('cls')
                                    print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
                        else:
                            if scam_filter == True:
                                if not any(scam_words in line for scam_words in scam_words):
                                    offers2.write(line)
                                    Filtered_Offers += 1
                                    Num_Offers += 1
                                    os.system('cls')
                                    print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
                            else:
                                offers2.write(line)
                                Filtered_Offers += 1
                                Num_Offers += 1
                                os.system('cls')
                                print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))


            #regex
            #change the items_in_list regex later | it confuses me
            items_in_list = re.compile(r'(~\w+\W\w+\W\w+\W\w+\W\w+\W\w+\W|~\w+\W\w+\W\w+\W\w\W\w+|~\w+\W\w+\W\w+\W\w+\W\w+\W\d+|~\w+\W\w+\W\w+\W\w+\W\w+\W|~\w+\W\w+\W\w+\W\w+\W|~\w+\W\w+\W\w+\W|~\w+\W\w\W\w+|~\w+\W\w+\W\W\w+\W|~\w+\W\W\w+\W|~\w+\W\w+\W|~\w+\W)')
            credits_r = re.compile(r'(credits/\w+/q:\d+|credits/q:\d+)')
            credits_q = re.compile(r'\d+')

            # skip first line i.e. read header first and then iterate over each row od csv as a list
            with open(r'CSV/offers2.csv', 'r', encoding='utf-8') as read_obj:
                csv_reader = reader(read_obj)
                header = next(csv_reader)
                # Check file as empty
                if header != None:
                    # Iterate over each row after the header in the csv
                    for row in csv_reader:
                        if stop_bot == True:
                            enable_settings()
                            break
                        try:
                            #print('\n' + str(row))
                            trade_link = row[1]
                            user_trader = row[3]
                            offer = row[4]
                            want = row[5]
                            offer_value = 0
                            want_value = 0

                            #filter white items offer
                            if white_list_itemsO_E == True:
                                if any(white_list_itemsO in offer for white_list_itemsO in white_list_itemsO):
                                    pass
                                else:
                                    #print("Offer included non whitelist items! skip")
                                    Num_Offers += 1
                                    Filtered_Offers += 1
                                    os.system('cls')
                                    print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
                                    continue

                            #filter white items want
                            if white_list_itemsW_E == True:
                                if any(white_list_itemsW in want for white_list_itemsW in white_list_itemsW):
                                    pass
                                else:
                                    #print("Offer included non whitelist items! skip")
                                    Num_Offers += 1
                                    Filtered_Offers += 1
                                    os.system('cls')
                                    print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
                                    continue

                            #checks offer_value
                            for match in re.findall(items_in_list, offer):
                                match3 = match.lower().replace(" ,", ",").replace("~monsoon", "~monsoon_boost").replace("~", "").replace("-", "_").replace(" ", "_").replace("'", "").replace("clr:cobalt", "cobalt").replace("clr:sky_blue", "sblue").replace("clr:burnt_sienna", "sienna").replace("clr:lime", "lime").replace("clr:grey", "grey").replace("clr:purple", "purple").replace("clr:crimson", "crimson").replace("clr:saffron", "saffron").replace("clr:orange", "orange").replace("clr:forest_green", "fgreen").replace("clr:pink", "pink").replace("clr:black", "black").replace("clr:titanium_white", "white")
                                #fix link item names
                                match2 = match3.replace("crl_northern", "octane_crl_northern").replace("cobra_kai", "octane_cobra_kai").replace("dragon_lord", "octane_dragon_lord").replace("edge_burst", "fennec_edge_burst").replace("octane_cobra_kai", "cobra_kai").replace("dominus_gentleman_beef", "gentleman_beef").replace("royal_tyrant", "octane_royal_tyrant").replace("e.t.", "et").replace("dune_racer", "octane_dune_racer").replace("dot_rush", "octane_dot_rush").replace("stratum_badge", "dominus_stratum_badge").replace("rose_king", "animus_gp_rose_king").replace("sovereign_a/t", "sovereign").replace("gold_nugget(beta_reward)", "gold_nugget_beta_reward").replace("sarp_stripe", "octane_sarp_stripe").replace("r3mx_gmt", "r3mx_gxt").replace("jãƒâ¤ger", "jager").replace("good_shape", "twinzer_good_shape").replace("tachyon", "tachyon_boost")

                                #link generator
                                #prevents using credits in link
                                #prevent blueprints
                                if not 'credits' in match2:
                                    q_amount2 = 0
                                    if 'q:' in match2:
                                        q_edit = re.compile(r'q:\d+_')
                                        q_amount = re.compile(r'\d+')
                                        for q_edit2 in re.findall(q_edit, match2):
                                            for q_amount2 in re.findall(q_amount, q_edit2):
                                                match2 = match2.replace(q_edit2, '')
                                                #print('Quantity: ' + q_amount2)

                                    #link generator for blueprints
                                    #check html blueprint price
                                    if '_blueprint' in match2:
                                        match_bp = match2.replace("_blueprint", "")
                                        #print('\n' + price_checker_url + match_bp)
                                        price_checker_site = requests.get(price_checker_url + match_bp)
                                        price_checker_site_soup = BeautifulSoup(price_checker_site.text, 'html.parser')
                                        price_check_item = price_checker_site_soup.find('tr', {'id': 'matrixRow3'})
                                        item_price2 = str(price_check_item).replace('<tr class="matrixRow" id="matrixRow3"><td><div class="hoverSettingsFlexHelper"><div class="hoverSettingsIcon" style="background-position-x: 18px;"></div><div class="hoverSettingsLabel">Blueprint value</div></div></td><td>', '').replace('</tr>', '')
                                        item_price_PSN_regex = re.compile(r'(</td><td>\d+.\d+ - \d+.\d+ k</td><td>|</td><td>\d+ - \d+.\d+ k</td><td>|</td><td>\d+ - \d+ k</td><td>|</td><td>\d+ - \d+</td><td>)')
                                        item_price_regex = re.compile(r'(\d+.\d+ - \d+.\d+ k|\d+ - \d+.\d+ k|\d+ - \d+)')
                                        for item_price3 in re.findall(item_price_PSN_regex, item_price2):
                                            for item_price in re.findall(item_price_regex, item_price3):
                                                #print(item_price)
                                                pass
                                    else:
                                        #print(price_checker_url + match2)
                                        price_checker_site = requests.get(price_checker_url + match2)
                                        price_checker_site_soup = BeautifulSoup(price_checker_site.text, 'html.parser')
                                        price_check_item = price_checker_site_soup.find('tr', {'id': 'PSNPrice'})
                                        price_check_item2 = price_check_item.find('td', {'class': 'pfData'})
                                        item_price = str(price_check_item2).replace('<td class="pfData">', '').replace('</td>', '')
                                        #print(item_price)
                                    #math to find midpoint price
                                    min_price_list = item_price.split()[:1]
                                    max_price_list = item_price.split()[2:3]
                                    K_price_list = item_price.split()[3:4]
                                    min_price = ''.join(map(str, min_price_list)) 
                                    max_price = ''.join(map(str, max_price_list)) 
                                    K_price = ''.join(map(str, K_price_list)) 

                                    if K_price == "k":
                                        if '.' in min_price: 
                                            min_price_edit = min_price.replace('.', '')
                                            min_price = min_price_edit + '00'
                                            #print(min_price)
                                        else:
                                            min_price_edit = min_price
                                            min_price = min_price_edit + '000'
                                            #print(min_price)  
                                        
                                        if '.' in max_price:
                                            max_price_edit = max_price.replace('.', '')
                                            max_price = max_price_edit + '00'
                                            #print(max_price)
                                        else:
                                            max_price_edit = max_price
                                            max_price = max_price_edit + '000'
                                            #print(max_price)  

                                    min_max_added = int(min_price) + int(max_price)

                                    midpoint_num = int(min_max_added)/2

                                    if int(q_amount2) >= 1:
                                        #print('Multiplying ' + str(q_amount2) + ' times!')
                                        midpoint_num = midpoint_num*int(q_amount2)

                                    #print(midpoint_num)
                                    offer_value += int(midpoint_num)

                                #adds credits to offer_value
                                for credits_offer in re.findall(credits_r, match2):
                                    for credits_offer_amount in re.findall(credits_q, credits_offer):
                                        offer_value += int(credits_offer_amount)
                            
                            #checks want_value
                            for match in re.findall(items_in_list, want):

                                match3 = match.lower().replace(" ,", ",").replace("~monsoon", "~monsoon_boost").replace("~", "").replace("-", "_").replace(" ", "_").replace("'", "").replace("clr:cobalt", "cobalt").replace("clr:sky_blue", "sblue").replace("clr:burnt_sienna", "sienna").replace("clr:lime", "lime").replace("clr:grey", "grey").replace("clr:purple", "purple").replace("clr:crimson", "crimson").replace("clr:saffron", "saffron").replace("clr:orange", "orange").replace("clr:forest_green", "fgreen").replace("clr:pink", "pink").replace("clr:black", "black").replace("clr:titanium_white", "white")
                                
                                match2 = match3.replace("crl_northern", "octane_crl_northern").replace("cobra_kai", "octane_cobra_kai").replace("dragon_lord", "octane_dragon_lord").replace("edge_burst", "fennec_edge_burst").replace("octane_cobra_kai", "cobra_kai").replace("balla_carra", "balla_carrãƒâ%C2%A0").replace("dominus_gentleman_beef", "gentleman_beef").replace("mr._coney", "insidio_mr_coney").replace("royal_tyrant", "octane_royal_tyrant").replace("e.t.", "et").replace("dune_racer", "octane_dune_racer").replace("dot_rush", "octane_dot_rush").replace("stratum_badge", "dominus_stratum_badge").replace("rose_king", "animus_gp_rose_king").replace("sovereign_a/t", "sovereign").replace("gold_nugget(beta_reward)", "gold_nugget_beta_reward").replace("sarp_stripe", "octane_sarp_stripe").replace("r3mx_gmt", "r3mx_gxt").replace("jãƒâ¤ger", "jager").replace("good_shape", "twinzer_good_shape").replace("tachyon", "tachyon_boost")

                                #link generator
                                #prevents using credits in link
                                #prevent blueprints
                                if not 'credits' in match2:
                                    q_amount2 = 0
                                    if 'q:' in match2:
                                        q_edit = re.compile(r'q:\d+_')
                                        q_amount = re.compile(r'\d+')
                                        for q_edit2 in re.findall(q_edit, match2):
                                            for q_amount2 in re.findall(q_amount, q_edit2):
                                                match2 = match2.replace(q_edit2, '')
                                                #print('Quantity: ' + q_amount2)

                                    #link generator for blueprints
                                    #check html blueprint price
                                    if '_blueprint' in match2:
                                        match_bp = match2.replace("_blueprint", "")
                                        #print(price_checker_url + match_bp)
                                        price_checker_site = requests.get(price_checker_url + match_bp)
                                        price_checker_site_soup = BeautifulSoup(price_checker_site.text, 'html.parser')
                                        price_check_item = price_checker_site_soup.find('tr', {'id': 'matrixRow3'})
                                        item_price2 = str(price_check_item).replace('<tr class="matrixRow" id="matrixRow3"><td><div class="hoverSettingsFlexHelper"><div class="hoverSettingsIcon" style="background-position-x: 18px;"></div><div class="hoverSettingsLabel">Blueprint value</div></div></td><td>', '').replace('</tr>', '')
                                        item_price_PSN_regex = re.compile(r'(</td><td>\d+.\d+ - \d+.\d+ k</td><td>|</td><td>\d+ - \d+.\d+ k</td><td>|</td><td>\d+ - \d+ k</td><td>|</td><td>\d+ - \d+</td><td>)')
                                        item_price_regex = re.compile(r'(\d+.\d+ - \d+.\d+ k|\d+ - \d+.\d+ k|\d+ - \d+)')
                                        for item_price3 in re.findall(item_price_PSN_regex, item_price2):
                                            for item_price in re.findall(item_price_regex, item_price3):
                                                #print(item_price)
                                                pass
                                    else:
                                        #print(price_checker_url + match2)
                                        price_checker_site = requests.get(price_checker_url + match2)
                                        price_checker_site_soup = BeautifulSoup(price_checker_site.text, 'html.parser')
                                        price_check_item = price_checker_site_soup.find('tr', {'id': 'PSNPrice'})
                                        price_check_item2 = price_check_item.find('td', {'class': 'pfData'})
                                        item_price = str(price_check_item2).replace('<td class="pfData">', '').replace('</td>', '')
                                        #print(item_price)

                                    #math to find midpoint price
                                    min_price_list = item_price.split()[:1]
                                    max_price_list = item_price.split()[2:3]
                                    K_price_list = item_price.split()[3:4]
                                    min_price = ''.join(map(str, min_price_list)) 
                                    max_price = ''.join(map(str, max_price_list))
                                    K_price = ''.join(map(str, K_price_list)) 

                                    if K_price == "k":
                                        if '.' in min_price: 
                                            min_price_edit = min_price.replace('.', '')
                                            min_price = min_price_edit + '00'
                                            #print(min_price)
                                        else:
                                            min_price_edit = min_price
                                            min_price = min_price_edit + '000'
                                            #print(min_price)  
                                        
                                        if '.' in max_price:
                                            max_price_edit = max_price.replace('.', '')
                                            max_price = max_price_edit + '00'
                                            #print(max_price)
                                        else:
                                            max_price_edit = max_price
                                            max_price = max_price_edit + '000'
                                            #print(max_price)
                                    
                                    min_max_added = int(min_price) + int(max_price)

                                    midpoint_num = int(min_max_added)/2
                                    
                                    if int(q_amount2) >= 1:
                                        #print('Multiplying ' + str(q_amount2) + ' times!')
                                        midpoint_num = midpoint_num*int(q_amount2)

                                    #print(midpoint_num)

                                    want_value += int(midpoint_num)
                                #adds credits to want_value
                                for credits_want in re.findall(credits_r, match2):
                                    for credits_want_amount in re.findall(credits_q, credits_want):
                                        want_value += int(credits_want_amount)

                            #Final results
                            #print("\noffer_value: " + str(offer_value))
                            #print("want_value: " + str(want_value))
                            gain_value = offer_value - want_value
                            #print("Gain Value: " + str(gain_value))
                            Num_Offers += 1
                            os.system('cls')
                            print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))

                            #filter cost
                            if offer_value >= min_offer_value and offer_value <= max_offer_value:
                                if want_value >= min_want_value and want_value <= max_want_value:
                                    if gain_value >= min_gain_value and gain_value <= max_gain_value:
                                        with open('offer_hits.csv', 'r', encoding='utf-8') as f:
                                            #grab num lines
                                            reader2 = csv.reader(f)
                                            lines2 = len(list(reader2))
                                            f.close()
                                            #print(lines2)

                                            #fix row
                                            new_row = str(row).replace("'", "").replace("[", "").replace("]", "")
                                            #checks num line limit
                                            if lines2 <= 50:
                                                with open('offer_hits.csv', 'a+', newline ='', encoding='utf-8') as f2:
                                                    f2.write(str(new_row) + " ," + str(offer_value) + " ," + str(want_value) + " ," + str(gain_value) + "\n")
                                                    f2.close()
                                            else:
                                                with open('offer_hits.csv', 'w+', encoding='utf-8') as reset:
                                                    reset.write('Bot Settings, Offer link, Note, Username, Items Offering, Items Want, Offer Value, Want Value, Gain Value\n' + str(new_row) + ' ,' + str(offer_value) + ' ,' + str(want_value) + ' ,' + str(gain_value) + '\n')
                                                    reset.close()

                                            playsound(r"mp3_files\hit.mp3")
                                            
                                            #Realtime table Window
                                            global hit_list
                                            #set rows
                                            hit_list.setRowCount(hits_table_row + 1)
                                            hit_list.setItem(hits_table_row, 0, QtWidgets.QTableWidgetItem(str(trade_link)))
                                            hit_list.setItem(hits_table_row, 1, QtWidgets.QTableWidgetItem(str(user_trader)))
                                            hit_list.setItem(hits_table_row, 2, QtWidgets.QTableWidgetItem(str(offer)))
                                            hit_list.setItem(hits_table_row, 3, QtWidgets.QTableWidgetItem(str(want)))
                                            hit_list.setItem(hits_table_row, 4, QtWidgets.QTableWidgetItem(str(offer_value)))
                                            hit_list.setItem(hits_table_row, 5, QtWidgets.QTableWidgetItem(str(want_value)))
                                            hit_list.setItem(hits_table_row, 6, QtWidgets.QTableWidgetItem(str(gain_value)))
                                            hits_table_row = hits_table_row + 1

                                            if Auto_Add == True:
                                                if gain_value >= 350:
                                                    offer_item_count = offer.count('~')
                                                    if offer_item_count <= 1:
                                                        want_item_count = want.count('~')
                                                        if want_item_count <= 1:
                    
                                                            driver.get(user_trader)

                                                            time.sleep(8)

                                                            friend_req_disabled = False
                                                            try:
                                                                driver.find_element_by_xpath('//*[@title="Add Friend"]').click()
                                                                time.sleep(4)
                                                                try:
                                                                    #confirm friend
                                                                    driver.find_element_by_xpath('//*[@class="sb-request-dialog__button sb-request-dialog__button--send sb-common-button sb-common-button--primary sb-common-button__on-click ember-view"]').click()
                                                                except Exception:
                                                                    #print("Couldn't confirm friend request")
                                                                    friend_req_disabled = True
                                                                    pass
                                                            except Exception:
                                                                #print("User already friended or couldn't find friend button")
                                                                pass
                                                            try:
                                                                #follow
                                                                time.sleep(2)
                                                                driver.find_element_by_xpath('//*[@class="color-picked-button__label-container _qa-follow-verified-user"]').click()
                                                            except Exception:
                                                                #print("User already followed")
                                                                pass
                                                            ########################################################
                                                            driver.get(trade_link)
                                                            try:
                                                                #click on Chat button of the offer
                                                                driver.find_element_by_xpath('//*[@class="rlg-trade__action --chat"]').click()
                                                                try:
                                                                    #send text to the user of the offer
                                                                    if friend_req_disabled == False:
                                                                        driver.find_element_by_xpath('//*[@id="messagetext"]').send_keys('I saw your recent trade offer post, I added you on PSN, Invite me to trade' + Keys.ENTER)
                                                                    else:
                                                                        driver.find_element_by_xpath('//*[@id="messagetext"]').send_keys('You have your PSN friend request disabled, can you friend me and Invite me to trade on your recent trade offer' + Keys.ENTER)
                                                                except Exception:
                                                                    #print("Couldn't find chat box!")
                                                                    pass
                                                            except Exception:
                                                                #print("Couldn't find 'Chat' button!")
                                                                pass

                                                            #print("\nfinished Auto Add User")
                                                            Auto_Hits += 1
                                                            os.system('cls')
                                                            print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))

                                            Hits += 1
                                            os.system('cls')
                                            print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
                                
                        except Exception:
                            #print("Couldn't calculate item value\n")
                            Offer_Errors += 1
                            Num_Offers += 1
                            os.system('cls')
                            print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))

            #print("Amount of Offer Errors due to bot not being able to grab the value of an item: " + str(Offer_Errors))
            #print("Finished checking offers, refreshing website for new offers...")
            #print(i)
            Site_Reloads += 1
            os.system('cls')
            print(Fore.GREEN + 'Hits: ' + str(Hits) + Fore.GREEN +  '\nAuto Hits: ' + str(Auto_Hits) + Fore.YELLOW +  '\nFiltered Offers: ' + str(Filtered_Offers) + Fore.RED + '\nOffer Errors: ' + str(Offer_Errors) + Fore.WHITE + '\nTotal Offers Checked: ' + str(Num_Offers) + Fore.CYAN + '\nSite Loads: ' + str(Site_Reloads) + Fore.BLUE + '\n\n||| Offer Filter |||' + Fore.WHITE + '\nMinimum price offer = ' + str(min_offer_value) + '\nMaximum price offer = ' + str(max_offer_value) + Fore.BLUE + '\n||| Want Filter |||' + Fore.WHITE + '\nMinimum price want = ' + str(min_want_value) + '\nMaximum price want = ' + str(max_want_value) + Fore.BLUE + '\n||| Gain Filter |||' + Fore.WHITE + '\nMinimum gain = ' + str(min_gain_value) + '\nMaximum gain = ' + str(max_gain_value))
            time.sleep(2)

            if stop_bot == True:
                enable_settings()
                break

class Table_Hits(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Offer Hits")
        self.setStyleSheet(u"background-color: rgb(47, 47, 47)")

        #create table
        global hit_list
        hit_list = QTableWidget() 

        #set grid line
        grid_layout = QGridLayout(self)
        grid_layout.addWidget(hit_list, 0, 0)

        #Set columns
        hit_list.setColumnCount(7)
        hit_list.setHorizontalHeaderLabels(["Offer Link", "Username", "Items Offering", "Items Want", "Offer Value", "Want Value", "Gain Value"])    

        #Table will fit the screen horizontally 
        #
        hit_list.setStyleSheet(u"background-color: rgb(59, 59, 59);\n"
        "color: rgb(62, 162, 255);\n"
        "gridline-color: rgb(255, 255, 255);\n"
        "selection-color: rgb(0, 0, 0);\n"
        "selection-background-color: rgb(255, 255, 255);\n"
        "")

        #disable edit feature in cells table
        hit_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        hit_list.clicked.connect(self.link_clicker)

    #'item' is text in cell 
    def link_clicker(self, item):
        cellContent = item.data()
        if 'https://' in cellContent:
            webbrowser.open(cellContent)
        

class Window(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        global max_offer_SB, min_offer_SB, max_want_SB, min_want_SB, max_gain_SB, min_gain_SB
        global E_scam_filter, E_WL_items_W, E_WL_items_O, E_BL_items_OW, E_auto_friend_DM
        # set the title 
        self.setWindowTitle("RL Bot by Carl0s#2776") 

        #Background color
        self.setStyleSheet("background-color: rgb(53, 53, 53);") 

        #window size
        height = 281
        width = 401
        self.setFixedHeight(height) 
        self.setFixedWidth(width) 

        #Title Label
        self.title_label = QLabel(self)
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; color:#000000;\">PSN Rocket League Offer Scraper Bot</span></p></body></html>", None))
        self.title_label.setGeometry(QRect(0, 0, 401, 41))
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("background-color: rgb(0, 112, 224)")

        #Settings Lebel
        self.setting_label = QLabel(self)
        self.setting_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#90cbff;\">Settings</span></p></body></html>", None))
        self.setting_label.setGeometry(QRect(0, 40, 401, 31))
        self.setting_label.setAlignment(QtCore.Qt.AlignCenter)
        self.setting_label.setStyleSheet("background-color: rgb(89, 89, 89)")

        #Enable scam filter
        E_scam_filter = QCheckBox(self)
        E_scam_filter.setText(QCoreApplication.translate("MainWindow", u"Enable Scam Filter", None))
        E_scam_filter.setGeometry(QRect(10, 80, 121, 17))
        E_scam_filter.setStyleSheet("color: rgb(255, 255, 255)")
        
        #Whitelist items want filter
        E_WL_items_W = QCheckBox(self)
        E_WL_items_W.setText(QCoreApplication.translate("MainWindow", u"Enable Whitelist Items Want Filter", None))
        E_WL_items_W.setGeometry(QRect(10, 100, 181, 17))
        E_WL_items_W.setStyleSheet("color: rgb(255, 255, 255)")

        #Whitelist items Offer filter
        E_WL_items_O = QCheckBox(self)
        E_WL_items_O.setText(QCoreApplication.translate("MainWindow", u"Enable Whitelist Items Offer Filter", None))
        E_WL_items_O.setGeometry(QRect(10, 120, 181, 17))
        E_WL_items_O.setStyleSheet("color: rgb(255, 255, 255)")
    
        #Enable Blacklist Items Offer/Want Filter
        E_BL_items_OW = QCheckBox(self)
        E_BL_items_OW.setText(QCoreApplication.translate("MainWindow", u"Enable Blacklist Items Offer/Want Filter", None))
        E_BL_items_OW.setGeometry(QRect(10, 140, 211, 17))
        E_BL_items_OW.setStyleSheet("color: rgb(255, 255, 255)")

        #Enable Auto Friend/DM
        E_auto_friend_DM = QCheckBox(self)
        E_auto_friend_DM.setText(QCoreApplication.translate("MainWindow", u"Enable Auto Friend/DM", None))
        E_auto_friend_DM.setGeometry(QRect(10, 160, 131, 17))
        E_auto_friend_DM.setStyleSheet("color: rgb(255, 255, 255)")

        ##############################

        #Offer price label
        self.offer_price_label = QLabel(self)
        self.offer_price_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; color:#ffffff;\">Offer Price Filter</span></p></body></html>", None))
        self.offer_price_label.setGeometry(QRect(280, 80, 111, 21))

        #Max offer Label
        self.max_offer_label = QLabel(self)
        self.max_offer_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">Maximum</span></p></body></html>", None))
        self.max_offer_label.setGeometry(QRect(230, 100, 51, 20))

        #Max offer spinbox
        max_offer_SB = QSpinBox(self)
        max_offer_SB.setGeometry(QRect(280, 100, 111, 16))
        max_offer_SB.setStyleSheet(u"background-color: rgb(229, 229, 229);")
        max_offer_SB.setMaximum(1000000000)

        #Min offer Label
        self.min_offer_label = QLabel(self)
        self.min_offer_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Minimum</span></p></body></html>", None))
        self.min_offer_label.setGeometry(QRect(236, 120, 41, 20))

        #Min offer spinbox
        min_offer_SB = QSpinBox(self)
        min_offer_SB.setGeometry(QRect(280, 120, 111, 16))
        min_offer_SB.setStyleSheet(u"background-color: rgb(229, 229, 229);")
        min_offer_SB.setMaximum(1000000000)

        ##############################

        #want price label
        self.want_price_label = QLabel(self)
        self.want_price_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; color:#ffffff;\">Want Price Filter</span></p></body></html>", None))
        self.want_price_label.setGeometry(QRect(280, 140, 111, 16))

        #Max want Label
        self.max_want_label = QLabel(self)
        self.max_want_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">Maximum</span></p></body></html>", None))
        self.max_want_label.setGeometry(QRect(230, 160, 51, 20))

        #Max want spinbox
        max_want_SB = QSpinBox(self)
        max_want_SB.setGeometry(QRect(280, 160, 111, 16))
        max_want_SB.setStyleSheet(u"background-color: rgb(229, 229, 229);")
        max_want_SB.setMaximum(1000000000)

        #Min want Label
        self.min_want_label = QLabel(self)
        self.min_want_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Minimum</span></p></body></html>", None))
        self.min_want_label.setGeometry(QRect(236, 180, 41, 20))

        #Min want spinbox
        min_want_SB = QSpinBox(self)
        min_want_SB.setGeometry(QRect(280, 180, 111, 16))
        min_want_SB.setStyleSheet(u"background-color: rgb(229, 229, 229);")
        min_want_SB.setMaximum(1000000000)

        ##############################

        #gain price label
        self.gain_price_label = QLabel(self)
        self.gain_price_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; color:#ffffff;\">Gain Price Filter</span></p></body></html>", None))
        self.gain_price_label.setGeometry(QRect(280, 200, 111, 16))

        #Max gain Label
        self.max_gain_label = QLabel(self)
        self.max_gain_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">Maximum</span></p></body></html>", None))
        self.max_gain_label.setGeometry(QRect(230, 220, 51, 20))

        #Max gain spinbox
        max_gain_SB = QSpinBox(self)
        max_gain_SB.setGeometry(QRect(280, 220, 111, 16))
        max_gain_SB.setStyleSheet(u"background-color: rgb(229, 229, 229);")
        max_gain_SB.setMaximum(1000000000)

        #Min gain Label
        self.min_gain_label = QLabel(self)
        self.min_gain_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Minimum</span></p></body></html>", None))
        self.min_gain_label.setGeometry(QRect(236, 240, 41, 20))

        #Min gain spinbox
        min_gain_SB = QSpinBox(self)
        min_gain_SB.setGeometry(QRect(280, 240, 111, 16))
        min_gain_SB.setStyleSheet(u"background-color: rgb(229, 229, 229);")
        min_gain_SB.setMaximum(1000000000)

        ##############################

        #reset all the settings from previous use
        self.settings = QSettings('RLbot', 'settings')
        try:
            scam_filter_REG = self.settings.value('Scam filter value')
            WL_items_W_REG = self.settings.value('Whitelist Want filter value')
            WL_items_O_REG = self.settings.value('Whitelist Offer filter value')
            BL_items_OW_REG = self.settings.value('Blacklist Offer/Want filter value')
            auto_friend_DM_REG = self.settings.value('Auto Add/DM value')

            if scam_filter_REG == 2:
                E_scam_filter.setChecked(True)
            else:
                E_scam_filter.setChecked(False)

            if WL_items_W_REG == 2:
                E_WL_items_W.setChecked(True)
            else:
                E_WL_items_W.setChecked(False)

            if WL_items_O_REG == 2:
                E_WL_items_O.setChecked(True)
            else:
                E_WL_items_O.setChecked(False)

            if BL_items_OW_REG == 2:
                E_BL_items_OW.setChecked(True)
            else:
                E_BL_items_OW.setChecked(False)

            if auto_friend_DM_REG == 2:
                E_auto_friend_DM.setChecked(True)
            else:
                E_auto_friend_DM.setChecked(False)

            max_offer_SB.setValue(self.settings.value('Max Offer value'))
            min_offer_SB.setValue(self.settings.value('Min Offer value'))
            max_want_SB.setValue(self.settings.value('Max Want value'))
            min_want_SB.setValue(self.settings.value('Min Want value'))
            max_gain_SB.setValue(self.settings.value('Max Gain value'))
            min_gain_SB.setValue(self.settings.value('Min Gain value'))
        except:
            pass

        ##############################
        self.threadpool = QtCore.QThreadPool()
        #Stop button
        global stop_bot2
        stop_bot2 = QPushButton(self)
        stop_bot2.setGeometry(QRect(30, 200, 71, 51))
        stop_bot2.setText(QCoreApplication.translate("MainWindow", u"Stop Bot", None))
        stop_bot2.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        stop_bot2.clicked.connect(self.stop)
        stop_bot2.setDisabled(True)

        #run button
        global run_bot
        run_bot = QPushButton(self)
        run_bot.setGeometry(QRect(120, 200, 71, 51))
        run_bot.setText(QCoreApplication.translate("MainWindow", u"Start Bot", None))
        run_bot.setStyleSheet(u"background-color: rgb(217, 217, 217);")
        run_bot.clicked.connect(self.start)

    def closeEvent(self, event):
        global max_offer_SB, min_offer_SB, max_want_SB, min_want_SB, max_gain_SB, min_gain_SB
        #save settings in REGISTRY
        self.settings.setValue('Scam filter value', E_scam_filter.checkState())
        self.settings.setValue('Whitelist Want filter value', E_WL_items_W.checkState())
        self.settings.setValue('Whitelist Offer filter value', E_WL_items_O.checkState())
        self.settings.setValue('Blacklist Offer/Want filter value', E_BL_items_OW.checkState())
        self.settings.setValue('Auto Add/DM value', E_auto_friend_DM.checkState())
        self.settings.setValue('Max Offer value', max_offer_SB.value())
        self.settings.setValue('Min Offer value', min_offer_SB.value())
        self.settings.setValue('Max Want value', max_want_SB.value())
        self.settings.setValue('Min Want value', min_want_SB.value())
        self.settings.setValue('Max Gain value', max_gain_SB.value())
        self.settings.setValue('Min Gain value', min_gain_SB.value())
        global stop_bot
        stop_bot = True
        print("closed program")
        sys.exit()
    
    def start(self):
        global scam_filter, white_list_itemsW_E, white_list_itemsO_E, black_list_items_E, Auto_Add, max_offer_value, min_offer_value, max_want_value, min_want_value, max_gain_value, min_gain_value
        global max_offer_SB, min_offer_SB, max_want_SB, min_want_SB, max_gain_SB, min_gain_SB
        if E_scam_filter.checkState() == 2:
            scam_filter = True
        else:
            scam_filter = False 

        if E_WL_items_W.checkState() == 2:
            white_list_itemsW_E = True
        else:
            white_list_itemsW_E = False

        if E_WL_items_O.checkState() == 2:
            white_list_itemsO_E = True
        else:
            white_list_itemsO_E = False

        if E_BL_items_OW.checkState() == 2:
            black_list_items_E = True
        else:
            black_list_items_E = False

        if E_auto_friend_DM.checkState() == 2:
            Auto_Add = True
        else:
            Auto_Add = False

        max_offer_value = max_offer_SB.value()
        min_offer_value = min_offer_SB.value()
        max_want_value = max_want_SB.value()
        min_want_value = min_want_SB.value()
        max_gain_value = max_gain_SB.value()
        min_gain_value = min_gain_SB.value()

        disable_settings()

        global stop_bot
        stop_bot = False

        #################################################
        self.Table_Hits_CL = Table_Hits()
        self.Table_Hits_CL.show()

        #########################################################################
        #Qthread code 
        pool = QThreadPool.globalInstance()
        # 2. Instantiate the subclass of QRunnable
        runnable = Runnable()
        # 3. Call start()
        pool.start(runnable)

    def stop(self):
        global stop_bot
        stop_bot = True

def disable_settings():
    global stop_bot
    E_scam_filter.setDisabled(True)
    E_WL_items_W.setDisabled(True)
    E_WL_items_O.setDisabled(True)
    E_BL_items_OW.setDisabled(True)
    E_auto_friend_DM.setDisabled(True)

    max_offer_SB.setDisabled(True)
    min_offer_SB.setDisabled(True)
    max_want_SB.setDisabled(True)
    min_want_SB.setDisabled(True)
    max_gain_SB.setDisabled(True)
    min_gain_SB.setDisabled(True)

    run_bot.setDisabled(True)
    stop_bot2.setDisabled(False)

def enable_settings():
    global stop_bot
    E_scam_filter.setDisabled(False)
    E_WL_items_W.setDisabled(False)
    E_WL_items_O.setDisabled(False)
    E_BL_items_OW.setDisabled(False)
    E_auto_friend_DM.setDisabled(False)

    max_offer_SB.setDisabled(False)
    min_offer_SB.setDisabled(False)
    max_want_SB.setDisabled(False)
    min_want_SB.setDisabled(False)
    max_gain_SB.setDisabled(False)
    min_gain_SB.setDisabled(False)

    run_bot.setDisabled(False)
    stop_bot2.setDisabled(True)

    os.system('cls')
    print(Fore.YELLOW + 'Bot has been paused')
    
if __name__ == '__main__':
    # create pyqt5 app 
    App = QApplication(sys.argv)
    # create the instance of our Window 
    window = Window()
    window.show() 

    # start the app 
    sys.exit(App.exec())
