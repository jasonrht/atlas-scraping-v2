import pandas as pd
import pdfcrowd
import os
from dotenv import load_dotenv

load_dotenv()

class pd_to_html:
    status = ''
    lb_name = ''
    totals = ''

    def __init__(self, lb_status, lb_name):
        self.status = lb_status
        self.lb_name = lb_name
        self.totals = {
            'TOB': 0,
            'GOB': 0,
            'Netto donateurs': 0,
            'Werkdagen': 0,
            'Bruto donateurs': 0,
            'GIB': 0,
            'Uitval': 0,
        }  

    def to_image(self, filename):
        try:
            client = pdfcrowd.HtmlToImageClient('tsangsol', os.getenv('PDF_API'))
            client.setOutputFormat('png')
            client.convertFileToFile(f'./HTMLs/{filename}.html', f'./PNGs/{filename}.png')
        except Exception as e:
            print(e)
            print('ERROR')

    def row_to_html(self, row, row_index):
        gob = row[3]

        self.totals['TOB'] += row[2]
        self.totals['Netto donateurs'] += row[4]
        self.totals['Werkdagen'] += row[5]
        self.totals['Bruto donateurs'] += row[6]

        row_color = ''
        if (gob >= 40 and self.status == 'p') or (gob >= 30 and self.status == 'st'):
            row_color = 'promotion'
        elif row_index == 0:
            row_color = 'rank-1'
        elif row_index == 1:
            row_color = 'rank-2'
        elif row_index == 2:
            row_color = 'rank-3'
        elif row_index > 2 and row_index < 10:
            row_color = 'middle-rank'
        elif row_index > 9:
            row_color = 'other-rank'

        adj_row_index = row[0]
        if type(adj_row_index) == float:
            adj_row_index = int(adj_row_index)
        html = f'<tr class="{row_color}"><td>{adj_row_index}</td><td>{row[1]}</td><td>€ {str(abs(round(row[2],2))).replace(".",",")}</td><td>€ {str(abs(round(row[3],2))).replace(".",",")}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>€ {str(abs(round(row[7],2))).replace(".",",")}</td><td>{str(abs(round(row[8]*100, 2))).replace(".",",")} %</td></tr>'
        return html

    def df_to_html(self, df, filename):
        table_rows = ''
        for i, row in df.iterrows():
            html_row = self.row_to_html(row, i)
            table_rows += html_row
        self.calc_totals()
        html = f'''
        <div>
        <h1 class="lb-title">{self.lb_name}</h1>
        <table>
            <thead>
                <tr class="columns">
                    <th>#</th>
                    <th>Naam</th>
                    <th>TOB</th>
                    <th>GOB</th>
                    <th>Netto donateurs</th>
                    <th>Werkdagen</th>
                    <th>Bruto donateurs</th>
                    <th>GIB</th>
                    <th>Uitval</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
                <tr class='totaal-row'>
                    <td style="border-right: 0px;">Totaal</td>
                    <td></td>
                    <td>€ {str(round(self.totals['TOB'],2)).replace(".",",")}</td>
                    <td>€ {str(round(self.totals['GOB'],2)).replace(".",",")}</td>
                    <td>{(self.totals['Netto donateurs'])}</td>
                    <td>{self.totals['Werkdagen']}</td>
                    <td>{self.totals['Bruto donateurs']}</td>
                    <td>€ {str(round(self.totals['GIB'],2)).replace(".",",")}</td>
                    <td>{str(round(self.totals['Uitval']*100,1)).replace(".",",")} %</td>
                </tr>
            </tbody>
            </table>
            </div>
        '''

        with open(f'./HTMLs/{filename}.html', 'w') as file:
            file.write(html)
            file.close()

        return table_rows
    
    def calc_totals(self):
        self.totals['GOB'] = round(self.totals['TOB'] / self.totals['Werkdagen'],2)
        self.totals['GIB'] = round(self.totals['TOB'] / self.totals['Bruto donateurs'],2)
        self.totals['Uitval'] = round((self.totals['Bruto donateurs'] - self.totals['Netto donateurs']) / self.totals['Bruto donateurs'],1)

    def main(self, csv_filename):
        df = pd.read_csv(f'./CSVs/{csv_filename}.csv')
        df.fillna('', inplace=True)
        self.df_to_html(df, csv_filename)
        self.to_image(csv_filename)

if __name__ == '__main__':
    pd_to_html.main()