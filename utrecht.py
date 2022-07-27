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
        lb_client.get_sheet('Huidige maand', 'Utrecht - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('UTR namenlijst', 'Utrecht - Leaderboards')
        wervers = name_client.get_names(1)

        # Utrecht
        utrecht_backstage = backstage.backstage('algemeen')
        utrecht_backstage.run(wervers)
        utrecht_backstage.sort_data(['TOB'])
        utrecht_data = utrecht_backstage.data
        lb_client.to_spreadsheet(utrecht_data, 'B4')
        print(utrecht_data)
        print('\n')
    except Exception as e:
        print(e)
        print('utrecht.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()