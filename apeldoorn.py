import backstage
import google_client as gc
import datetime as dt

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
        name_client.get_sheet('APD namenlijst', 'Apeldoorn - Leaderboards')
        wervers = name_client.get_names(1)

        # Apeldoorn
        apeldoorn_backstage = backstage.backstage('algemeen')
        apeldoorn_backstage.run(wervers)
        apeldoorn_backstage.sort_data(['TOB'])
        apeldoorn_data = apeldoorn_backstage.data
        lb_client.to_spreadsheet(apeldoorn_data, 'B4')
        print(apeldoorn_data)
        print('\n')
    except Exception as e:
        print(e)
        print('apeldoorn.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()