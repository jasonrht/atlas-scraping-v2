from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime as dt

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
            self.sheet.update(corner, [df.columns.values.tolist()] + df.values.tolist())
            print('Spreadsheet update success!')
        except Exception as e:
            print(e)
            print('ERROR: Failed to update spreadsheet ...')

    def get_names(self, column_index):
        try:
            print('Fetching names from spreadsheet ...')
            WARNING = '!!! VERGEET NIET OM RIJEN TOE TE VOEGEN OP DE LEADERBOARDS WANNEER JE HIER EEN WERVER TOEVOEGT !!!'
            names = list(filter(lambda x: x != 'ZZP' and x != 'Sales Professionals+' and x != '' and x != 'Promotors' and x != 'Shark Tank' and x != 'Loondienst' and x != 'Wervers', self.sheet.col_values(column_index)))
            print('Names fetched!')
            return names
        except Exception as e:
            print(e)
            print('ERROR: Failed to get names from spreadsheet ...')

if __name__ == '__main__':
    '''
        Testing
    '''
    client = google_client()
    client.get_sheet('Huidige maand', 'Rotterdam HQ - Leaderboards')
    print(client.get_names(4))

