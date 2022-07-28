import send_mail as sm
import pandas as pd
import pdfcrowd
import os
from dotenv import load_dotenv

load_dotenv()

def to_image(filename):
    try:
        client = pdfcrowd.HtmlToImageClient('tsangsol', os.getenv('PDF_API'))
        client.setOutputFormat('png')
        client.convertFileToFile(f'./HTMLs/{filename}.html', f'./PNGs/{filename}.png')
    except Exception as e:
        print(e)
        print('ERROR')

def row_to_html(row, row_index):
    row_color = ''
    if row_index == 0:
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
    html = f'<tr class="{row_color}"><td>{adj_row_index}</td><td>{row[1]}</td><td>€ {str(row[2]).replace(".",",")}</td><td>€ {str(row[3]).replace(".",",")}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>€ {str(row[7]).replace(".",",")}</td><td>{str(round(row[8]*100, 2)).replace(".",",")} %</td></tr>'
    return html

def df_to_html(df, filename):
    table_rows = ''
    for i, row in df.iterrows():
        html_row = row_to_html(row, i)
        table_rows += html_row
    html = f'''
    <html>

<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap"
        rel="stylesheet">

    <style>
        html {{
            font-family: 'Lato', sans-serif;
        }}

        table {{
            border: solid 2px black;
            border-collapse: collapse;
            color: black;
            width: 1000px;
        }}

        tr {{
            border-bottom: solid 2px black;
        }}

        th,
        td {{
            padding: 5px 10px;
            text-align: center;
            max-height: 30px;
            border-right: solid 2px black;
        }}

        tr th:nth-child(1) {{
            border-right: 2px solid black;
        }}

        tr td:nth-child(1) {{
            border-right: 2px solid black;
            background-color: white;
        }}


        .rank-1 {{
            background-color: #1d4ed8;
        }}

        .rank-2 {{
            background-color: #2563eb;
        }}

        .rank-3 {{
            background-color: #3b82f6;
        }}

        .middle-rank {{
            background-color: #60a5fa;
        }}

        .other-rank {{
            background-color: #93c5fd;
        }}
    </style>
</head>

<body>
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
        </tbody>
</body>

</html>
    '''

    with open(f'./HTMLs/{filename}.html', 'w') as file:
        file.write(html)
        file.close()
    return table_rows

def main(csv_filename):
    df = pd.read_csv(f'./CSVs/{csv_filename}.csv')
    df.fillna('', inplace=True)
    df_to_html(df, csv_filename)
    to_image(csv_filename)

if __name__ == '__main__':
    main()
