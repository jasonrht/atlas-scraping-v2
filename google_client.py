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

    def get_sheet(self, wks):
        try:
            print('Opening worksheet ...')
            self.sheet = self.client.open('LeaderboardsAtlas').worksheet(wks)
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
            names = list(filter(lambda x: x != 'ROTTERDAM' and x != 'Naam' and x != '' and x != WARNING, self.sheet.col_values(column_index)))
            print('Names fetched!')
            return names
        except Exception as e:
            print(e)
            print('ERROR: Failed to get names from spreadsheet ...')
        
    def get_name_status(self, name_index, status_index):
        try:
            print('Fetching names and statuses ...')
            WARNING = '!!! VERGEET NIET OM RIJEN TOE TE VOEGEN OP DE LEADERBOARDS WANNEER JE HIER EEN WERVER TOEVOEGT !!!'
            names = list(filter(lambda x: x != 'ROTTERDAM' and x != 'Naam' and x != '' and x != WARNING, self.sheet.col_values(name_index)))
            statuses = list(filter(lambda x: x != 'Status' and x != '' and x != WARNING, self.sheet.col_values(status_index)))
            name_dict = {}
            for i, name in enumerate(names):
                name_dict[name] = statuses[i]
            print('Fetched names and statuses !')
            return name_dict
        except Exception as e:
            print(e)
            print('ERROR: Failed to fetch names and statuses ...')


if __name__ == '__main__':
    '''
        Testing
    '''
    # client = google_client()
    # client.get_sheet('RTM namenlijst')
    # df = pd.DataFrame({'col1': [0,1,2,3,4,5,6], 'col2': [6,5,4,3,2,1,0]})
    # client.to_spreadsheet(df, 'F3')

    print(dt.datetime.today().year)
