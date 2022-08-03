import backstage
import google_client as gc
import datetime as dt
import pd_to_html
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
        lb_client.get_sheet('Huidige maand', 'Nijmegen - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('Namenlijst', 'Nijmegen - Leaderboards')
        wervers = name_client.get_names(2)

        # Utrecht
        nijmegen_backstage = backstage.backstage('algemeen')
        nijmegen_backstage.run(wervers)
        nijmegen_backstage.sort_data(['TOB'])
        nijmegen_data = nijmegen_backstage.data
        nijmegen_data.to_csv('./CSVs/nijmegen_data.csv')

        nmg_pd2html = pd_to_html.pd_to_html('algemeen', 'Nijmegen')
        nmg_pd2html.main('nijmegen_data')

        html = '''
        <html>

    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link
            href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap"
            rel="stylesheet">

        <style>
            html {
                font-family: 'Lato', sans-serif;
            }

            .lb-title {
                text-align: center;
            }

            table {
                border: solid 2px black;
                border-collapse: collapse;
                color: black;
                width: 1000px;
                margin-bottom: 5rem;
            }

            tr {
                border-bottom: solid 2px black;
            }

            th,
            td {
                padding: 5px 10px;
                text-align: center;
                max-height: 30px;
                border-right: solid 2px black;
            }

            tr th:nth-child(1) {
                border-right: 2px solid black;
            }

            tr td:nth-child(1) {
                border-right: 2px solid black;
                background-color: white;
            }

            .promotion {
                background-color: green;
            }

            .rank-1 {
                background-color: #1d4ed8;
                font-weight: bold;
            }

            .rank-2 {
                background-color: #2563eb;
                font-weight: bold;
            }

            .rank-3 {
                background-color: #3b82f6;
                font-weight: bold;
            }

            .middle-rank {
                background-color: #60a5fa;
            }

            .other-rank {
                background-color: #93c5fd;
            }

            .totaal-row {
                font-weight: bold;
            }
        </style>
    </head>
    <body style="display: grid; grid-template-columns: 1fr 1fr; gap: 0 3rem; padding: 0 1rem;">
        '''
        with open('./HTMLs/nijmegen_data.html', 'r') as r_file:
            html += r_file.read()
        r_file.close()
        html += '</body></html>'
        with open('./HTMLs/nmg_tot.html', 'w') as w_file:
            w_file.write(html)
        w_file.close()
        lb_client.to_spreadsheet(nijmegen_data, 'B4')

        print(nijmegen_data)
        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('nijmegen.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()