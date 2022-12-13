import backstage
import google_client as gc
import datetime as dt
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
            lb_client.get_sheet(f'{MONTH_DICT[int(month)]} {today.year}', 'Den Haag - Leaderboards')
        else:
            lb_client.get_sheet('Huidige maand', 'Den Haag - Leaderboards')            
        name_client = gc.google_client()
        name_client.get_sheet('Namenlijst', 'Den Haag - Leaderboards')
        wervers = name_client.get_names(2)
        # wervers = ['Rosa de Kiefte']

        adj_list = lb_client.get_stat_adjustments(61)

        # Den Haag
        if len(wervers) > 0:
            dh_backstage = backstage.backstage('algemeen')
            dh_backstage.run(wervers, adj_list ,backup=backup)
            dh_data = dh_backstage.data
            print(dh_data)

            svhk_backstage = backstage.backstage('svhk')
            svhk_backstage.run(wervers, backup=backup)
            svhk_data = svhk_backstage.data
            print(svhk_data)
            print('\n')

            data = merge_data(dh_data, svhk_data)
            data.set_index(data.iloc[:,0],inplace=True)
            data.drop(data.columns[[0]], axis=1, inplace=True)
            data.to_csv('./CSVs/dh_data.csv')
            print(data)
    
            lb_client.to_spreadsheet(data, 'B4')
        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('den_haag.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()