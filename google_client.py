from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime as dt
import backstage

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

class google_client:
    client = ''
    sheet = ''

    def __init__(self):
        try:
            print('Initializing Google Spreadsheet client instance ...')
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('atlas.json', scope)
            self.client = gspread.authorize(creds)
            print('Initialization success!')
        except Exception as e:
            print(e)
            print('ERROR: Failed to initialize google client instance ...')


    def get_sheet(self, wks, filename):
        try:
            print('Opening worksheet ...')
            self.sheet = self.client.open(filename).worksheet(wks)
            print('Opened worksheet successfully!')
        except Exception as e:
            print(e)
            print('ERROR: Failed to open worksheet ...')
    
    def to_spreadsheet(self, df, corner):
        try:
            print('Updating spreadsheet ...')
            df.reset_index(inplace=True)
            self.sheet.update(corner, [df.columns.values.tolist()] + df.values.tolist())
            print('Spreadsheet update success!')
        except Exception as e:
            print(e)
            print('ERROR: Failed to update spreadsheet ...')

    def get_names(self, column_index):
        try:
            print('Fetching names from spreadsheet ...')
            WARNING = '!!! VERGEET NIET OM RIJEN TOE TE VOEGEN OP DE LEADERBOARDS WANNEER JE HIER EEN WERVER TOEVOEGT !!!'
            names = list(filter(lambda x: x != 'ZZP' and x != 'Sales Professionals+' and x != '' and x != 'Promotors' and x != 'Shark Tank' and x != 'Loondienst' and x != 'Wervers' and x != 'SVHK', self.sheet.col_values(column_index)))
            print('Names fetched!')
            return names
        except Exception as e:
            print(e)
            print('ERROR: Failed to get names from spreadsheet ...')

    def get_all_names(self):
        names = []
        all_values = client.sheet.get_all_values()
        for category in all_values[2][1:3]:
            names.append([])
            
        for value_list in all_values[3:]:
            for index, name in enumerate(value_list[1:3]):
                if(name):
                    names[index].append(name)
        return names

    def change_name(self):
        try:
            print('Changing name ...')
            prev_month = dt.datetime.today().month - 1
            prev_month_name = MONTH_DICT[prev_month]
            current_year = dt.datetime.today().year
            if prev_month == 11:
                current_year += 1
            self.sheet.update_title(f'{prev_month_name} {current_year}')
            print('Name changed successfully !')
        except Exception as e:
            print(e)
            print('ERROR: Failed to change name of spreadsheet ...')

    def duplicate_sheet(self):
        try:
            self.sheet.duplicate()
        except Exception as e:
            print(e)
            print('ERROR: Failed to change name of spreadsheet ...')

    def get_stat_adjustments(self, start_row_index):
        try:
            adj_col_values = self.sheet.col_values(4)[start_row_index:]
            adj_col_names = self.sheet.col_values(3)[start_row_index:]
            adj_col_list = []
            for index, value in enumerate(adj_col_values):
                adj_col_list.append([adj_col_names[index], value])
            adj_col_list = list(filter(lambda x: x[1] != '', adj_col_list))
            return adj_col_list

        except Exception as e:
            print(e)
            print('ERROR: Failed to get adjustment stats ...')



if __name__ == '__main__':
    '''
        Testing
    '''
    client = google_client()
    client.get_sheet('Huidige maand', 'Rotterdam HQ - Leaderboards')
    client.duplicate_sheet()
    client.get_sheet('Copy of Huidige maand', 'Rotterdam HQ - Leaderboards')
    client.change_name()
    # prev_month_client = google_client().get_sheet('')
    # client.change_name()
    # names = client.get_all_names()
    # print(names[0])

