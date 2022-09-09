import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
import pandas as pd
import math
import google_client as gc
import datetime as dt

load_dotenv()

class backstage:
    platform = ''
    session = ''
    werver_ids = {}
    data = ''

    def __init__(self, platform):
        self.platform = platform

        if platform == 'algemeen':
            self.login('https://backstage.atlas-sales-agency.nl/login')
            res = self.session.get('https://backstage.atlas-sales-agency.nl/admin/career/bonus/detail?user=7377&start_month=01&start_year=2022')
        elif platform == 'svhk':
            self.platform = platform
            self.login('https://backstage.stichtingvanhetkind.nl/login')
            res = self.session.get('https://backstage.stichtingvanhetkind.nl/admin/career/bonus/detail?user=7661&start_month=01&start_year=2022')
        elif platform == 'svhk-apd':
            self.platform = platform
            self.login('https://backstage.stichtingvanhetkind.nl/login')
            res = self.session.get('https://backstage.stichtingvanhetkind.nl/admin/career/bonus/detail')
        elif platform == 'svhk-utr':
            self.platform = platform
            self.login('https://backstage.stichtingvanhetkind.nl/login')
            res = self.session.get('https://backstage.stichtingvanhetkind.nl/admin/career/bonus/detail')

        self.werver_ids = self.werver_dict(res.text)


    def login(self, url):
        login_creds = {
            "email": os.getenv('ALGEMEEN_USERNAME'),
            "password": os.getenv('ALGEMEEN_PW'),
        }

        svhk_login_creds = {
            "email": os.getenv('SVHK_USERNAME'),
            "password": os.getenv('SVHK_PW')
        }

        svhk_apd_creds = {
            "email": os.getenv('SVHK_APD_USERNAME'),
            "password": os.getenv('SVHK_APD_PW')
        }

        svhk_utr_creds = {
            "email": os.getenv('SVHK_UTR_USERNAME'),
            "password": os.getenv('SVHK_UTR_PW')
        }

        all_login_creds = [login_creds, svhk_login_creds, svhk_apd_creds, svhk_utr_creds]

        s = requests.session()
        login_page = s.get(url)
        login_page_bs = bs(login_page.text, "html.parser")
        csrf_token = login_page_bs.find("input", attrs={"name":"_csrf_token"}).get("value")
        if self.platform == 'algemeen':
            login_creds = all_login_creds[0]
        elif self.platform == 'svhk':
            login_creds = all_login_creds[1]
        elif self.platform == 'svhk-apd':
            login_creds = all_login_creds[2]
        elif self.platform == 'svhk-utr':
            login_creds = all_login_creds[3]
        login_creds["_csrf_token"] = csrf_token
        s.post(url, data=login_creds)
        self.session = s

    def werver_dict(self, page):
        i=0
        wervers_ids = []
        wervers = {}
        wervers_list = bs(page,"html.parser").find_all("option")
        for werver_id in wervers_list:
            wervers_list[i] = werver_id.text.strip()
            wervers_ids.append(werver_id.get("value"))
            wervers[wervers_list[i]] = wervers_ids[i]
            i+=1
        
        return wervers
    
    def get_name(self, id, wervers):
        # returns name of werver by werver id
        for key,value in wervers.items():
            if id == value:
                return key 
        return "key does not exist"
    
    def get_data(self, werver,content):
        wervers = self.werver_dict(content)
        data_page = bs(content, "html.parser")
        df = pd.read_html(content)
        data_werver = df[1]
        trs = data_page.find_all("table")[1].find_all("tr")[1:-3] # correctie voor laatste rijen
        if list(df[1].columns).count('Project') == 0:
            data_werver = df[2]
            trs = data_page.find_all("table")[2].find_all("tr")[1:-3] # correctie voor laatste rijen
        data_werver.rename(columns={"Unnamed: 0": "col1","Unnamed: 2":"column_three"},inplace=True)

        sal_periode = data_werver["Na uitval deze periode"]
        eenmalig_col = data_werver["Eenmalig"]
        project_col = data_werver["Project"] 

        factor = -1
        i=0
        for tr in trs:
            if isinstance(project_col[i], str):
                row = tr.find("td", attrs={"class": "number"})
                if not(row is None):
                    tds = tr.find_all("td", attrs={"class":"number"})
                    tot = tds[0].text.replace("M","").replace("⨉","").replace(",",".").strip()
                    sal = tds[3].text.replace("€\xa0","").replace(",",".").strip()
                    if not(tot=="") and not(sal=="") and float(tot)<=15:
                        factor = float(sal)/float(tot)
                        break
            i+=1
        werkdagen = 0
        tot_eenmalig = 0
        bruto_don = 0
        tob = 0
        i=0
        for tr in trs: # per rij data extraheren
            date = tr.find("td", attrs={"class":"align-middle"})
            if not(date is None):
                werkdagen += 1

            switch_sym = tr.find("i", attrs={"class": "fa fa-exchange-alt text-warning"})
            if isinstance(project_col[i], str):
                bruto_don += 1
                if (switch_sym is None) and not(pd.isnull(eenmalig_col[i])) and not(math.isnan(float(sal_periode[i]))):
                    bruto_don -= 1
                    tot_eenmalig += float(sal_periode[i])
                # inschrijfbedrag > 15
                row = tr.find("td", attrs={"class": "number"})
                if not(row is None):
                    bedrag = row.text.replace("M","").replace("⨉","").replace(",",".").strip()
                    if not(bedrag==""):
                        f_bedrag = float(bedrag)
                        if f_bedrag>15:
                            tob += factor*(f_bedrag-15)
            i+=1 

        tot_eenmalig = tot_eenmalig/100 # omzetten centen naar euros
        verd_werver = df[0]
        na_uitval = verd_werver["Na uitval deze periode"]
        # totaal opgehaald bedrag (TOB)
        tob1 = na_uitval[0].replace("€\xa0","").replace(".","").replace(",",".").strip()
        tob += (float(tob1)-tot_eenmalig)

        # gemiddeld opgehaald 
        if werkdagen>0:
            gob = tob/float(werkdagen*factor)
        else:
            gob = 0

        if verd_werver["Salaris deze periode"][4] == "-":
            uitval = 0
        else:
            uitval = float(verd_werver["Salaris deze periode"][4].replace(" %", "").replace(",","."))
        netto_don = int(round(bruto_don*(1-(uitval/100))))
        if netto_don == 0:
            gib = 0 
        else:
            gib = tob/float(netto_don*factor)

        name = self.get_name(werver, wervers)
        if name == 'key does not exist':
            name = werver

        variables = {
            "Naam": name,
            "TOB": round(tob/factor,2),
            "GOB": round(gob,2),
            "Netto donateurs": netto_don,
            "Werkdagen": werkdagen,
            "Bruto donateurs": bruto_don,
            "GIB": round(gib,2),
            "Uitval": round(100*uitval/10000,2)
        }
        return variables

    def get_links(self, wervers, ids, month, year):
        links = []
        werver_ids = ids
        for i in range(len(wervers)):
            user_id = werver_ids[i]
            if self.platform == "algemeen":
                link = f"https://backstage.atlas-sales-agency.nl/admin/career/bonus/detail?user={user_id}&start_month={month}&start_year={year}"
                links.append(link)     
            else:
                link = f"https://backstage.stichtingvanhetkind.nl/admin/career/bonus/detail?user={user_id}&start_month={month}&start_year={year}"  
                links.append(link)
        return links

    def new_index(self):
        tobs = self.data.loc[:,"TOB"].values
        prev_tob = tobs[0]
        new = [1]
        i=2
        for t in tobs[1:]:
            tob = tobs[i-1]
            if  tob == prev_tob:
                new.append("")
            else:
                new.append(i)
            prev_tob = tob
            i+=1
        return new
    
    def sort_data(self, columns):
        self.data.sort_values(by=columns, ascending=False, inplace=True)
        new_indices = self.new_index()
        self.data.insert(0, '', new_indices)
        self.data.set_index(self.data.iloc[:,0],inplace=True)
        self.data.drop(self.data.columns[[0]], axis=1, inplace=True)
    
    def run(self, wervers):
        month = dt.datetime.today().month
        # month = 8
        if month < 10:
            month = '0' + str(month)
        month = str(month)
        year = str(dt.datetime.today().year)
        t0 = dt.datetime.now()
        print(f'Fetching data for {self.platform} ...')
        werver_ids = self.werver_ids
        ids = []
        for werver in wervers:
            if list(werver_ids.keys()).count(werver) != 0:
                werver_id = werver_ids[werver]
                ids.append(werver_id)
            else:
                ids.append(werver)
        links = self.get_links(wervers, ids, month, year)
        data = []
        for j, link in enumerate(links):
            try:
                res = self.session.get(link)
            except Exception as e:
                print(e)
                print(f'Request for {wervers[j]} failed ...')
            data.append(self.get_data(ids[j], res.text))
        self.data = pd.DataFrame(data)
        t1 = dt.datetime.now()
        print(f'{self.platform.capitalize()} data fetched in {t1-t0}!')
    
if __name__ == '__main__':
    '''
        Testing
    '''
    spreadsheet_client = gc.google_client()
    spreadsheet_client.get_sheet('APD namenlijst', 'Apeldoorn - Leaderboards')
    all_wervers = spreadsheet_client.get_names(2)

    algemeen_backstage = backstage('svhk-apd')
    algemeen_backstage.run(all_wervers)
    algemeen_backstage.sort_data(['TOB'])
    algemeen_data = algemeen_backstage.data
    algemeen_data.set_index(algemeen_data.iloc[:,0],inplace=True)
    algemeen_data.drop(algemeen_data.columns[[0]], axis=1, inplace=True)
    print(algemeen_data)
    # algemeen_data.to_csv('data.csv')
