import backstage
import google_client as gc
import datetime as dt
import pd_to_html
import send_mail as sm
import traceback
import pandas as pd

def new_index(df):
    tobs = df.loc[:,"TOB"].values
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

def merge_data(df1, df2):
    merged_data = pd.DataFrame(columns=['Naam','TOB','GOB','Netto donateurs','Werkdagen','Bruto donateurs','GIB','Uitval'])
    merged_data['Naam'] = df1['Naam']
    merged_data['TOB'] = df1['TOB'] + df2['TOB']
    merged_data['Werkdagen'] = df1['Werkdagen'] + df2['Werkdagen']
    merged_data['Bruto donateurs'] = df1['Bruto donateurs'] + df2['Bruto donateurs']
    merged_data['Netto donateurs'] = df1['Netto donateurs'] + df2['Bruto donateurs']
    merged_data['GOB'] = round(merged_data['TOB'] / merged_data['Werkdagen'], 2)
    merged_data['GIB'] = round(merged_data['TOB'] / merged_data['Bruto donateurs'], 2)
    merged_data['Uitval'] = round((merged_data['Bruto donateurs'] - merged_data['Netto donateurs']) / merged_data['Bruto donateurs'], 1)
    merged_data.sort_values(by=['TOB'], ascending=False, inplace=True)
    new_indices = new_index(merged_data)
    # merged_data.set_index(pd.Index(new_indices), inplace=True)
    merged_data.insert(0, '', new_indices)
    merged_data.fillna(0, inplace=True)
    print(merged_data)
    return merged_data

def main():
    try: 
        print(f'***{"-"*40}***')
        today = dt.datetime.today()
        month = today.month
        if month < 10:
            month = f'0{month}'
        else:
            month = str(month)
        YEAR = str(today.year)
        lb_client = gc.google_client()
        lb_client.get_sheet('Huidige maand', 'Utrecht - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('Namenlijst', 'Utrecht - Leaderboards')
        sp = name_client.get_names(2)
        st = name_client.get_names(3)

        # Sales Promotors
        sp_algemeen_backstage = backstage.backstage('algemeen')
        sp_algemeen_backstage.run(sp)
        sp_algemeen_data = sp_algemeen_backstage.data
        print(sp_algemeen_data)
        print('\n')

        sp_svhk_backstage = backstage.backstage('svhk-utr')
        sp_svhk_backstage.run(sp)
        sp_svhk_data = sp_svhk_backstage.data
        print(sp_svhk_data)
        print('\n')

        sp_data = merge_data(sp_algemeen_data, sp_svhk_data)
        sp_data.set_index(sp_data.iloc[:,0],inplace=True)
        sp_data.drop(sp_data.columns[[0]], axis=1, inplace=True)
        sp_data.to_csv('./CSVs/sp_utr_data.csv')
        sp_pd2html = pd_to_html.pd_to_html('sp', 'Sales Professionals+')
        sp_pd2html.main('sp_utr_data')
        # lb_client.to_spreadsheet(sp_data, 'B5')

        # Shark Tank
        st_algemeen_backstage = backstage.backstage('algemeen')
        st_algemeen_backstage.run(st)
        st_algemeen_backstage.sort_data(['TOB'])
        st_data = st_algemeen_backstage.data
        print(st_data)
        print('\n')

        st_data.to_csv('./CSVs/st_utr_data.csv')
        st_pd2html = pd_to_html.pd_to_html('st', 'Shark Tank')
        st_pd2html.main('st_utr_data')
        lb_client.to_spreadsheet(st_data, 'B60')

        # HTML -> PNG -> EMAIL
        # sm.send_m('jtsangsolutions@gmail.com', ['utrecht_data.png'], send_images=False)

        # print(sp_data)
        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('utrecht.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()