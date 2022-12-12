import backstage
import google_client as gc
import datetime as dt
import send_mail as sm
import traceback

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

        # Den Haag
        if len(wervers) > 0:
            dh_backstage = backstage.backstage('algemeen')
            dh_backstage.run(wervers, backup=backup)
            dh_backstage.sort_data(['TOB'])
            dh_data = dh_backstage.data
            dh_data.to_csv('./CSVs/dh_data.csv')
            lb_client.to_spreadsheet(dh_data, 'B4')
    
        print(dh_data)
        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('den_haag.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()