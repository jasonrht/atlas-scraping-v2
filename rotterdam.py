import pandas as pd
import backstage
import google_client as gc
import datetime as dt
import pd_to_html
import traceback
import send_mail as sm

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
    # merged_data.set_index(pd.Index(new_indices), inplace=True)
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
            lb_client.get_sheet(f'{MONTH_DICT[month]} {today.year}', 'Rotterdam HQ - Leaderboards')
        else:
            lb_client.get_sheet('Huidige maand', 'Rotterdam HQ - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('Namenlijst', 'Rotterdam HQ - Leaderboards')
        sp = name_client.get_names(2)
        p = name_client.get_names(3)
        st = name_client.get_names(4)
        loondienst = name_client.get_names(5)
        sp2 = []
        for name in sp:
            name_bool = name in p or name in st or name in loondienst
            if not name_bool:
                sp2.append(name)

        adj_list = lb_client.get_stat_adjustments(97)

        ### Rotterdam ZZP ###
        # Sales Professionals+
        sp_algemeen_backstage = backstage.backstage('algemeen')
        sp_algemeen_backstage.run(sp2, adj_list)
        sp_algemeen_data = sp_algemeen_backstage.data
        print(sp_algemeen_data)
        print('\n')


        sp_svhk_backstage = backstage.backstage('svhk')
        sp_svhk_backstage.run(sp2)
        sp_svhk_data = sp_svhk_backstage.data
        print(sp_svhk_data)
        print('\n')

        sp_data = merge_data(sp_algemeen_data, sp_svhk_data)
        sp_data.set_index(sp_data.iloc[:,0],inplace=True)
        sp_data.drop(sp_data.columns[[0]], axis=1, inplace=True)
        sp_data.to_csv('./CSVs/sp_data.csv')
        # sp_pd2html = pd_to_html.pd_to_html('sp', 'Sales Professionals+')
        # sp_pd2html.main('sp_data')
        lb_client.to_spreadsheet(sp_data, 'B5')

        # Sales Promotors
        p_algemeen_backstage = backstage.backstage('algemeen')
        p_algemeen_backstage.run(p, adj_list)
        p_algemeen_data = p_algemeen_backstage.data
        print(p_algemeen_data)
        print('\n')

        p_svhk_backstage = backstage.backstage('svhk')
        p_svhk_backstage.run(p)
        p_svhk_data = p_svhk_backstage.data
        print(p_svhk_data)
        print('\n')

        p_data = merge_data(p_algemeen_data, p_svhk_data)
        p_data.set_index(p_data.iloc[:,0],inplace=True)
        p_data.drop(p_data.columns[[0]], axis=1, inplace=True)
        p_data.to_csv('./CSVs/p_data.csv')
        # p_pd2html = pd_to_html.pd_to_html('p', 'Promotors')
        # p_pd2html.main('p_data')
        lb_client.to_spreadsheet(p_data, 'B59')

        # Shark Tank
        st_algemeen_backstage = backstage.backstage('algemeen')
        st_algemeen_backstage.run(st, adj_list)
        st_algemeen_data = st_algemeen_backstage.data
        print(st_algemeen_data)
        print('\n')

        st_svhk_backstage = backstage.backstage('svhk')
        st_svhk_backstage.run(st)
        st_svhk_data = st_svhk_backstage.data
        print(st_svhk_data)
        print('\n')

        st_data = merge_data(st_algemeen_data, st_svhk_data)
        st_data.set_index(st_data.iloc[:,0],inplace=True)
        st_data.drop(st_data.columns[[0]], axis=1, inplace=True)
        st_data.to_csv('./CSVs/st_data.csv')
        # st_pd2html = pd_to_html.pd_to_html('st', 'Shark Tank')
        # st_pd2html.main('st_data')
        lb_client.to_spreadsheet(st_data, 'B73')

        # Loondienst
        loondienst_backstage = backstage.backstage('algemeen')
        loondienst_backstage.run(loondienst)
        loondienst_backstage.sort_data(['TOB'])
        loondienst_data = loondienst_backstage.data
        loondienst_data.to_csv('./CSVs/loondienst_data.csv')
        # ld_pd2html = pd_to_html.pd_to_html('algemeen', 'Loondienst')
        # ld_pd2html.main('loondienst_data')
        lb_client.to_spreadsheet(loondienst_data, 'L5')
        print(loondienst_data)
        print('\n')

    #     # Merge all HTMLs
    #     tot_html = '''
    #     <html>

    # <head>
    #     <link rel="preconnect" href="https://fonts.googleapis.com">
    #     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    #     <link
    #         href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap"
    #         rel="stylesheet">

    #     <style>
    #         html {
    #             font-family: 'Lato', sans-serif;
    #         }

    #         .lb-title {
    #             text-align: center;
    #         }

    #         table {
    #             border: solid 2px black;
    #             border-collapse: collapse;
    #             color: black;
    #             width: 1000px;
    #             margin-bottom: 5rem;
    #         }

    #         tr {
    #             border-bottom: solid 2px black;
    #         }

    #         th,
    #         td {
    #             padding: 5px 10px;
    #             text-align: center;
    #             max-height: 30px;
    #             border-right: solid 2px black;
    #         }

    #         tr th:nth-child(1) {
    #             border-right: 2px solid black;
    #         }

    #         tr td:nth-child(1) {
    #             border-right: 2px solid black;
    #             background-color: white;
    #         }

    #         .promotion {
    #             background-color: green;
    #         }

    #         .rank-1 {
    #             background-color: #1d4ed8;
    #             font-weight: bold;
    #         }

    #         .rank-2 {
    #             background-color: #2563eb;
    #             font-weight: bold;
    #         }

    #         .rank-3 {
    #             background-color: #3b82f6;
    #             font-weight: bold;
    #         }

    #         .middle-rank {
    #             background-color: #60a5fa;
    #         }

    #         .other-rank {
    #             background-color: #93c5fd;
    #         }

    #         .totaal-row {
    #             font-weight: bold;
    #         }
    #     </style>
    # </head>
    # <body style="display: grid; grid-template-columns: 1fr 1fr; gap: 0 3rem; padding: 0 1rem;">
    #     '''
    #     locations = ['sp_data', 'loondienst_data', 'p_data','st_data']
    #     for loc in locations:
    #         with open(f'./HTMLs/{loc}.html', 'r') as file:
    #             tot_html += file.read()
    #         file.close()
    #     tot_html += '</body></html>'
    #     with open('./HTMLs/rtm_tot_.html', 'w') as file:
    #         file.write(tot_html)
    #     file.close()

    except Exception as e:
        traceback.print_exc()
        print('rotterdam.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()