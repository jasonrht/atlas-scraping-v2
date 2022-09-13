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
        lb_client.get_sheet('Huidige maand', 'Apeldoorn - Leaderboards')
        name_client = gc.google_client()
        name_client.get_sheet('Namenlijst', 'Apeldoorn - Leaderboards')
        wervers = name_client.get_names(2)
        svhk_wervers = name_client.get_names(3)

        # Apeldoorn
        apeldoorn_backstage = backstage.backstage('algemeen')
        apeldoorn_backstage.run(wervers)
        apeldoorn_backstage.sort_data(['TOB'])
        apeldoorn_data = apeldoorn_backstage.data
        apeldoorn_data.to_csv('./CSVs/apeldoorn_data.csv')

        lb_client.to_spreadsheet(apeldoorn_data, 'B5')
        # apd_pd2html = pd_to_html.pd_to_html('algemeen', 'Loondienst')
        # apd_pd2html.main('apeldoorn_data')

        apeldoorn_svhk_backstage = backstage.backstage('svhk-apd')
        apeldoorn_svhk_backstage.run(svhk_wervers)
        apeldoorn_svhk_backstage.sort_data(['TOB'])
        apeldoorn_svhk_data = apeldoorn_svhk_backstage.data
        apeldoorn_svhk_data.to_csv('./CSVs/apeldoorn_svhk_data.csv')

        lb_client.to_spreadsheet(apeldoorn_svhk_data, 'L5')
        # apd_svhk_pd2html = pd_to_html.pd_to_html('algemeen', 'Loondienst')
        # apd_svhk_pd2html.main('apeldoorn_svhk_data')

    #     html = '''
    #     <html>

    # <head>
    #     <link rel="preconnect" href="https://fonts.googleapis.com">
    #     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    #     <link
    #         href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap"
    #         rel="stylesheet">

    #     <style>
    #         html {
    #             font-family: 'Lato', sans-serif;
    #         }

    #         .lb-title {
    #             text-align: center;
    #         }

    #         table {
    #             border: solid 2px black;
    #             border-collapse: collapse;
    #             color: black;
    #             width: 1000px;
    #             margin-bottom: 5rem;
    #         }

    #         tr {
    #             border-bottom: solid 2px black;
    #         }

    #         th,
    #         td {
    #             padding: 5px 10px;
    #             text-align: center;
    #             max-height: 30px;
    #             border-right: solid 2px black;
    #         }

    #         tr th:nth-child(1) {
    #             border-right: 2px solid black;
    #         }

    #         tr td:nth-child(1) {
    #             border-right: 2px solid black;
    #             background-color: white;
    #         }

    #         .promotion {
    #             background-color: green;
    #         }

    #         .rank-1 {
    #             background-color: #1d4ed8;
    #             font-weight: bold;
    #         }

    #         .rank-2 {
    #             background-color: #2563eb;
    #             font-weight: bold;
    #         }

    #         .rank-3 {
    #             background-color: #3b82f6;
    #             font-weight: bold;
    #         }

    #         .middle-rank {
    #             background-color: #60a5fa;
    #         }

    #         .other-rank {
    #             background-color: #93c5fd;
    #         }

    #         .totaal-row {
    #             font-weight: bold;
    #         }
    #     </style>
    # </head>
    # <body style="display: grid; grid-template-columns: 1fr 1fr; gap: 0 3rem; padding: 0 1rem;">
    #     '''
    #     groups = ['apeldoorn_data', 'apeldoorn_svhk_data']
    #     for group in groups:
    #         with open(f'./HTMLs/{group}.html', 'r') as r_file:
    #             html += r_file.read()
    #         r_file.close()
    #     html += '</body></html>'
    #     with open('./HTMLs/apeldoorn_tot.html', 'w') as w_file:
    #         w_file.write(html)
    #     w_file.close()

        print(apeldoorn_data)
        print('\n')
    except Exception as e:
        traceback.print_exc()
        print('apeldoorn.py - ERROR: Failed to run script ...')

if __name__ == '__main__':
    main()