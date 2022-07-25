import pandas as pd
import backstage
import google_client as gc
import datetime as dt
import send_mail as sm

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
    merged_data['GOB'] = merged_data['TOB'] / merged_data['Werkdagen']
    merged_data['GIB'] = merged_data['TOB'] / merged_data['Bruto donateurs']
    merged_data['Uitval'] = (merged_data['Bruto donateurs'] - merged_data['Netto donateurs']) / merged_data['Bruto donateurs']
    merged_data.sort_values(by=['TOB'], ascending=False, inplace=True)
    new_indices = new_index(merged_data)
    # merged_data.set_index(pd.Index(new_indices), inplace=True)
    merged_data.insert(0, '', new_indices)
    merged_data.fillna(0, inplace=True)
    print(merged_data)
    return merged_data


def main():
    print(f'***{"-"*40}***')
    today = dt.datetime.today()
    month = today.month
    if month < 10:
        month = f'0{month}'
    else:
        month = str(month)
    YEAR = str(today.year)
    lb_client = gc.google_client()
    lb_client.get_sheet('Leaderboard Juli 2022')
    name_client = gc.google_client()
    name_client.get_sheet('RTM namenlijst')
    sp = name_client.get_names(1)
    p = name_client.get_names(4)
    st = name_client.get_names(7)
    loondienst = name_client.get_names(10)

    ### Rotterdam ZZP ###
    # Sales Professionals+
    sp_algemeen_backstage = backstage.backstage('algemeen')
    sp_algemeen_backstage.run(sp)
    sp_algemeen_data = sp_algemeen_backstage.data
    print(sp_algemeen_data)
    print('\n')

    sp_svhk_backstage = backstage.backstage('svhk')
    sp_svhk_backstage.run(sp)
    sp_svhk_data = sp_svhk_backstage.data
    print(sp_svhk_data)
    print('\n')

    sp_data = merge_data(sp_algemeen_data, sp_svhk_data)
    lb_client.to_spreadsheet(sp_data, 'B3')

    # Sales Promotors
    p_algemeen_backstage = backstage.backstage('algemeen')
    p_algemeen_backstage.run(p)
    p_algemeen_data = p_algemeen_backstage.data
    print(p_algemeen_data)
    print('\n')

    p_svhk_backstage = backstage.backstage('svhk')
    p_svhk_backstage.run(p)
    p_svhk_data = p_svhk_backstage.data
    print(p_svhk_data)
    print('\n')

    p_data = merge_data(p_algemeen_data, p_svhk_data)
    lb_client.to_spreadsheet(p_data, 'B' + str(3 + len(sp) + 4))

    # Shark Tank
    st_algemeen_backstage = backstage.backstage('algemeen')
    st_algemeen_backstage.run(st)
    st_algemeen_data = st_algemeen_backstage.data
    print(st_algemeen_data)
    print('\n')

    st_svhk_backstage = backstage.backstage('svhk')
    st_svhk_backstage.run(st)
    st_svhk_data = st_svhk_backstage.data
    print(st_svhk_data)
    print('\n')

    st_data = merge_data(st_algemeen_data, st_svhk_data)
    lb_client.to_spreadsheet(st_data, 'B' + str(3 + len(sp) + len(p) + 8))

    # Loondienst
    loondienst_backstage = backstage.backstage('algemeen')
    loondienst_backstage.run(loondienst)
    loondienst_backstage.sort_data(['TOB'])
    loondienst_data = loondienst_backstage.data
    name_client.to_spreadsheet(loondienst_data, 'L3')
    print(loondienst_data)
    print('\n')

    sm.send_m('jtsangsolutions@gmail.com')

if __name__ == '__main__':
    main()