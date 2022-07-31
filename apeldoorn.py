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
        lb_client.get_sheet('Huidige maand', 'Apeldoorn - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('Namenlijst', 'Apeldoorn - Leaderboards')
        wervers = name_client.get_names(2)

        # Apeldoorn
        apeldoorn_backstage = backstage.backstage('algemeen')
        apeldoorn_backstage.run(wervers)
        apeldoorn_backstage.sort_data(['TOB'])
        apeldoorn_data = apeldoorn_backstage.data
        apeldoorn_data.to_csv('./CSVs/apeldoorn_data.csv')

        # apeldoorn_backstage = backstage.backstage('algemeen')
        # apeldoorn_backstage.run(wervers)
        # apeldoorn_backstage.sort_data(['TOB'])
        # apeldoorn_data = apeldoorn_backstage.data
        # apeldoorn_data.to_csv('./CSVs/apeldoorn_data.csv')
        lb_client.to_spreadsheet(apeldoorn_data, 'B4')

        # HTML -> PNG -> EMAIL
        sm.send_m('jtsangsolutions@gmail.com', 'apeldoorn_data.png')

        print(apeldoorn_data)
        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('apeldoorn.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()