import backstage
import google_client as gc
import datetime as dt
import send_mail as sm
import traceback

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
        wervers = name_client.get_names(2)

        # Utrecht
        utrecht_backstage = backstage.backstage('algemeen')
        utrecht_backstage.run(wervers)
        utrecht_backstage.sort_data(['TOB'])
        utrecht_data = utrecht_backstage.data
        utrecht_data.to_csv('./CSVs/utrecht_data.csv')
        lb_client.to_spreadsheet(utrecht_data, 'B4')

        # HTML -> PNG -> EMAIL
        sm.send_m('jtsangsolutions@gmail.com', 'utrecht_data.png')

        print(utrecht_data)
        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('utrecht.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()