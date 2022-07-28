import backstage
import google_client as gc
import datetime as dt
import pandas_to_html as pd2html
import send_mail as sm

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
        lb_client.get_sheet('Huidige maand', 'Nijmegen - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('NMG namenlijst', 'Nijmegen - Leaderboards')
        wervers = name_client.get_names(1)

        # Utrecht
        nijmegen_backstage = backstage.backstage('algemeen')
        nijmegen_backstage.run(wervers)
        nijmegen_backstage.sort_data(['TOB'])
        nijmegen_data = nijmegen_backstage.data
        nijmegen_data.to_csv('./CSVs/nijmegen_data.csv')
        # lb_client.to_spreadsheet(nijmegen_data, 'B4')

        # HTML -> PNG -> EMAIL
        pd2html.main('nijmegen_data')
        sm.send_m('jtsangsolutions@gmail.com', 'nijmegen_data.png')
        print(nijmegen_data)
        print('\n')
    except Exception as e:
        print(e)
        print('nijmegen.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()