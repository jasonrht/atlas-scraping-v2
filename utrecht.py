import backstage
import google_client as gc
import datetime as dt
import pd_to_html
import traceback
import pandas as pd

MONTH_DICT = {
    1: 'Januari',
    2: 'Februari',
    3: 'Maart',
    4: 'April',
    5: 'Mei',
    6: 'Juni',
    7: 'Juli',
    8: 'Augustus',
    9: 'September',
    10: 'Oktober',
    11: 'November',
    12: 'December'
}

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
    '''
        Merge the data of two dataframes.
    '''
    merged_data = pd.DataFrame(columns=['Naam','TOB','GOB','Netto donateurs','Werkdagen','Bruto donateurs','GIB','Uitval'])
    merged_data['Naam'] = df1['Naam']
    merged_data['TOB'] = df1['TOB'] + df2['TOB']
    merged_data['Werkdagen'] = df1['Werkdagen'] + df2['Werkdagen']
    merged_data['Bruto donateurs'] = df1['Bruto donateurs'] + df2['Bruto donateurs']
    merged_data['Netto donateurs'] = df1['Netto donateurs'] + df2['Netto donateurs']
    merged_data['GOB'] = round(merged_data['TOB'] / merged_data['Werkdagen'], 2)
    merged_data['GIB'] = round(merged_data['TOB'] / merged_data['Netto donateurs'], 2)
    merged_data['Uitval'] = round((merged_data['Bruto donateurs'] - merged_data['Netto donateurs']) / merged_data['Bruto donateurs'], 3)
    merged_data.sort_values(by=['TOB'], ascending=False, inplace=True)
    new_indices = new_index(merged_data)
    merged_data.insert(0, '', new_indices)
    merged_data.fillna(0, inplace=True)
    print(merged_data)
    return merged_data

def main(backup=False):
    try: 
        print(f'***{"-"*40}***')
        today = dt.datetime.today()
        month = today.month
        if backup:
            month = month - 1
            
        if month < 10:
            month = f'0{month}'
        else:
            month = str(month)
        YEAR = str(today.year)
        lb_client = gc.google_client()
        if backup:
            lb_client.get_sheet(f'{MONTH_DICT[month]} {today.year}', 'Utrecht - Leaderboards')
        else:
            lb_client.get_sheet('Huidige maand', 'Utrecht - Leaderboards')        
        name_client = gc.google_client()
        name_client.get_sheet('Namenlijst', 'Utrecht - Leaderboards')
        sp = name_client.get_names(2)
        p = name_client.get_names(3)
        st = name_client.get_names(4)
        ld = name_client.get_names(5)
        sp2 = []
        for name in sp:
            name_bool = name in p or name in st or name in ld
            if not name_bool:
                sp2.append(name)

        # Sales Promotors
        sp_algemeen_backstage = backstage.backstage('algemeen')
        sp_algemeen_backstage.run(sp2)
        sp_algemeen_data = sp_algemeen_backstage.data
        print(sp_algemeen_data)
        print('\n')

        sp_svhk_backstage = backstage.backstage('svhk-utr')
        sp_svhk_backstage.run(sp2)
        sp_svhk_data = sp_svhk_backstage.data
        print(sp_svhk_data)
        print('\n')

        sp_data = merge_data(sp_algemeen_data, sp_svhk_data)
        sp_data.set_index(sp_data.iloc[:,0],inplace=True)
        sp_data.drop(sp_data.columns[[0]], axis=1, inplace=True)
        sp_data.to_csv('./CSVs/sp_utr_data.csv')
        # sp_pd2html = pd_to_html.pd_to_html('sp', 'Sales Professionals+')
        # sp_pd2html.main('sp_utr_data')
        lb_client.to_spreadsheet(sp_data, 'B5')

        # Promotors
        p_algemeen_backstage = backstage.backstage('algemeen')
        p_algemeen_backstage.run(p)
        p_algemeen_data = p_algemeen_backstage.data
        print(p_algemeen_data)
        print('\n')

        p_svhk_backstage = backstage.backstage('svhk-utr')
        p_svhk_backstage.run(p)
        p_svhk_data = p_svhk_backstage.data
        print(p_svhk_data)
        print('\n')

        p_data = merge_data(p_algemeen_data, p_svhk_data)
        p_data.set_index(p_data.iloc[:,0],inplace=True)
        p_data.drop(p_data.columns[[0]], axis=1, inplace=True)
        p_data.to_csv('./CSVs/p_utr_data.csv')
        # p_pd2html = pd_to_html.pd_to_html('p', 'Sales Professionals+')
        # p_pd2html.main('p_utr_data')
        lb_client.to_spreadsheet(p_data, 'B39')

        # Shark Tank
        st_algemeen_backstage = backstage.backstage('algemeen')
        st_algemeen_backstage.run(st)
        st_algemeen_data = st_algemeen_backstage.data
        print(st_algemeen_data)
        print('\n')

        st_svhk_backstage = backstage.backstage('svhk-utr')
        st_svhk_backstage.run(st)
        st_svhk_data = st_svhk_backstage.data
        print(st_svhk_data)
        print('\n')

        st_data = merge_data(st_algemeen_data, st_svhk_data)
        st_data.set_index(st_data.iloc[:,0],inplace=True)
        st_data.drop(st_data.columns[[0]], axis=1, inplace=True)
        st_data.to_csv('./CSVs/st_utr_data.csv')

        # st_data.to_csv('./CSVs/st_utr_data.csv')
        # st_pd2html = pd_to_html.pd_to_html('st', 'Shark Tank')
        # st_pd2html.main('st_utr_data')
        lb_client.to_spreadsheet(st_data, 'B53')

        # Loondienst
        ld_algemeen_backstage = backstage.backstage('algemeen')
        ld_algemeen_backstage.run(ld)
        ld_algemeen_data = ld_algemeen_backstage.data
        print(ld_algemeen_data)
        print('\n')

        ld_svhk_backstage = backstage.backstage('svhk-utr')
        ld_svhk_backstage.run(ld)
        ld_svhk_data = ld_svhk_backstage.data
        print(ld_svhk_data)
        print('\n')

        ld_data = merge_data(ld_algemeen_data, ld_svhk_data)
        ld_data.set_index(ld_data.iloc[:,0],inplace=True)
        ld_data.drop(ld_data.columns[[0]], axis=1, inplace=True)
        ld_data.to_csv('./CSVs/ld_utr_data.csv')

        # st_data.to_csv('./CSVs/st_utr_data.csv')
        # st_pd2html = pd_to_html.pd_to_html('st', 'Shark Tank')
        # st_pd2html.main('st_utr_data')
        lb_client.to_spreadsheet(ld_data, 'L5')

        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('utrecht.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()