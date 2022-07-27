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
        lb_client.get_sheet('Huidige maand', 'Amsterdam - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('AMS namenlijst', 'Amsterdam - Leaderboards')
        wervers = name_client.get_names(1)

        # Amsterdam
        amsterdam_backstage = backstage.backstage('algemeen')
        amsterdam_backstage.run(wervers)
        amsterdam_backstage.sort_data(['TOB'])
        amsterdam_data = amsterdam_backstage.data
        lb_client.to_spreadsheet(amsterdam_data, 'B4')
        print(amsterdam_data)
        print('\n')
    except Exception as e:
        print(e)
        print('amsterdam.py - ERROR: Failed to run script ...')
if __name__ == '__main__':
    main()