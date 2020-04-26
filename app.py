import pandas as pd
import numpy as np
import plotly
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import warnings
import os
warnings.simplefilter('ignore')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title='COVID-19'
server=app.server

#dashboard.bind(app)

# Data
confirmed_df = pd.read_csv('http://api.covid19india.org/states_daily_csv/confirmed.csv')
deaths_df = pd.read_csv("https://api.covid19india.org/states_daily_csv/deceased.csv")
recovered_df = pd.read_csv("https://api.covid19india.org/states_daily_csv/recovered.csv")

confirmed_df = confirmed_df.iloc[:, :-1]
deaths_df = deaths_df.iloc[:, :-1]
recovered_df = recovered_df.iloc[:, :-1]

confirmed_df.head()
deaths_df.head()
recovered_df.head()

confirmed_df.columns

cols = {
    "date": "date",
    "TT": "Total",
    "AN": "Andaman and Nicobar Islands",
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CH": "Chandigarh",
    "CT": "Chhattisgarh",
    "DD": "Daman and Diu",
    "DL": "Delhi",
    "DN": "Dadra and Nagar Haveli",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HP": "Himachal Pradesh",
    "HR": "Haryana",
    "JH": "Jharkhand",
    "JK":"Jammu & Kashmir",
    "KA": "Karnataka",
    "KL": "Kerala",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "MH": "Maharashtra",
    "ML": "Meghalaya",
    "MN": "Manipur",
    "MP": "Madhya Pradesh",
    "MZ": "Mizoram",
    "NL": "Naga Land",
    "OR": "Odisha",
    "PB": "Punjab",
    "PY": "Puducherry",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TG": "Telengana",
    "TN": "Tamil Nadu",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UT": "Union Territories",
    "WB": "West Bengal"

}

confirmed_df.rename(columns=cols, inplace=True)
recovered_df.rename(columns=cols, inplace=True)
deaths_df.rename(columns=cols, inplace=True)

confirmed_df['cumulate_total'] = confirmed_df['Total'].cumsum()
recovered_df['cumulate_total'] = recovered_df['Total'].cumsum()
deaths_df['cumulate_total'] = deaths_df['Total'].cumsum()

confirmed_cases = confirmed_df['Total'].sum()
recovered_cases = recovered_df['Total'].sum()
deaths = deaths_df['Total'].sum()
Active = confirmed_cases - recovered_cases - deaths

dash_colors = {
    'background': '#111111',
    'text': '#BEBEBE',
    'grid': '#333333',
    'red': '#BF0000'
}

cls = confirmed_df.columns
cls = cls[2:-1]
confirmed_dict = {}
for i in cls:
    a = []
    a.append(int(confirmed_df[i].sum()))
    a.append(int(recovered_df[i].sum()))
    a.append(int(deaths_df[i].sum()))
    confirmed_dict.update({i: a})

confirmed_dict
d = pd.DataFrame(list(confirmed_dict.items()))

final_df = pd.DataFrame(d[1].values.tolist(), columns=['Total Confirmed','Recovered','Deaths'],
                        index=d[0]).reset_index()
final_df.rename(columns={0: 'State'}, inplace=True)
final_df['Active'] = final_df["Total Confirmed"] - final_df['Recovered'] - final_df['Deaths']
final_df["Last_24Hrs Confirmed"]=confirmed_df.tail(1).T[2:-1].reset_index().iloc[:,1:]
final_df=final_df[['State',"Last_24Hrs Confirmed","Total Confirmed",'Recovered','Deaths','Active']]
sorted_df = final_df.sort_values(["Total Confirmed"], ascending=False)

final_df1 = sorted_df.copy()
sorted_df = sorted_df[:10]



app.layout = html.Div(style={'backgroundColor': dash_colors['background']},
                      children=[
                          html.H1(children="Covid-19 Indian DashBoard",
                                  style={
                                      'font-family': 'Times New Roman',
                                      'textAlign': 'center',
                                      'color': 'red'
                                  }),

                          html.H5('''Coronavirus disease 2019(COVID-19) is an infectious spreading disease,which is casued by severe acute respiratory syndrome coronavirus 2(SARS-Cov-2).This disease was first found in 2019 in Wuhan distirct of China,
    and is spreading tremendously across the globe,resulted in pandemic declaration by World Health Organization.''',
                                 style={
                                    'font-family': 'Times New Roman',
                                    'textAlign':'center',
                                     'color': 'white'
                                 }),
                          html.H4("Confirmed cases: {}".format(confirmed_cases),
                                  style={
                                      'textAlign': 'center',
                                      'font-family': 'Times New Roman',
                                      'color': '#F3AE0F',
                                      'height': 22

                                  }),
                          html.H4("Recovered cases: {}".format(recovered_cases),
                                  style={
                                      'font-family': 'Times New Roman',
                                      'textAlign': 'center',
                                      'color': '#F3AE0F',
                                      'height': 22

                                  }),
                          html.H4("Deaths: {}".format(deaths),
                                  style={ 
                                      'font-family': 'Times New Roman',
                                      'textAlign': 'center',
                                      'color': '#F3AE0F',
                                      'height': 22
                                  }),
                          html.H4("Active cases: {}".format(Active),
                                  style={
                                      'font-family': 'Times New Roman',
                                      'textAlign': 'center',
                                      'color': '#F3AE0F',
                                      'height': 22
                                  }),
                          dcc.Graph(
                              id='sample-graph1',
                              figure={
                                  'data': [
                                      {'x': confirmed_df['date'], 'y': confirmed_df['cumulate_total'],
                                       'type': 'line', 'name': 'confirmed'},
                                      {'x': confirmed_df['date'], 'y': deaths_df['cumulate_total'], 'type': 'line',
                                       'name': 'deaths'},
                                      {'x': confirmed_df['date'], 'y': recovered_df['cumulate_total'],
                                       'type': 'line', 'name': 'recovered'}
                                  ],
                                  'layout': {
                                      'title': "Trend of Covid-19 in India",
                                      "paper_bgcolor": dash_colors['background'],
                                      "plot_bgcolor": dash_colors['background'],
                                      "font": {"color": 'white'}

                                  }
                              }),dcc.Graph(
                                    id='sample-graph2',
                                            figure={
                                                  'data':[
                                             {'x':confirmed_df['date'],'y':confirmed_df['Telengana'],'type':'line','name':'Confirmed'},
                                             {'x':confirmed_df['date'],'y':deaths_df['Telengana'],'type':'line','name':'Deaths'},
                                             {'x':confirmed_df['date'],'y':recovered_df['Telengana'],'type':'line','name':'Recovered'}
                                                         ],
                                                      'layout':{
                                                                    'title':"Trend of Covid-19 in Telangana",
                                                                    "paper_bgcolor": dash_colors['background'],
                                                                    "plot_bgcolor": dash_colors['background'],
                                                                    "font":{"color":'white'}    } }),
                                     dcc.Graph(
                                              id='sample-graph3',
                                               figure={
                                                       'data':[
                                            {'x':confirmed_df['date'],'y':confirmed_df["Andhra Pradesh"],'type':'line','name':'Confirmed'},
                                            {'x':confirmed_df['date'],'y':deaths_df["Andhra Pradesh"],'type':'line','name':'Deaths'},
                                            {'x':confirmed_df['date'],'y':recovered_df["Andhra Pradesh"],'type':'line','name':'Recovered'}
                                                               ],
                                                  'layout':{
                                                                'title':"Trend of Covid-19 in Andhra Pradesh",
                
                                                             "paper_bgcolor": dash_colors['background'],
                                                           "plot_bgcolor": dash_colors['background'],
                
                                                        "font":{"color":'white'}
                
                                                     }
                                                       }),
                          dcc.Graph(
                              id="sample-graph4",
                              figure={
                                  'data': [
                                      {'x': sorted_df['State'], 'y': sorted_df['Total Confirmed'], 'type': 'bar',
                                       'name': 'confirmed'},
                                      {'x': sorted_df['State'], 'y': sorted_df['Recovered'], 'type': 'bar',
                                       'name': 'recovered'},
                                      {'x': sorted_df['State'], 'y': sorted_df['Deaths'], 'type': 'bar',
                                       'name': 'deaths'},
                                      {'x': sorted_df['State'], 'y': sorted_df['Active'], 'type': 'bar',
                                       'name': 'active'}
                                  ],
                                  'layout': {
                                      'title': "Highly affected states",
                                      "paper_bgcolor": dash_colors['background'],
                                      "plot_bgcolor": dash_colors['background'],
                                      "font": {"color": 'white'}

                                  }

                              }
                          ),
                          dash_table.DataTable(
                              id='table',
                              columns=[{"name": i, "id": i} for i in final_df1.columns],
                              data=final_df1.to_dict('records'),

                              style_table={
                                  'maxHeight': '500px',
                                  'overflowY': 'scroll',
                                  'border': 'thin lightgrey solid'

                              }, style_cell={
                                  # all three widths are needed
                                  'minWidth': '180px', 'width': '150px', 'maxWidth': '180px', 'textAlign': 'center','font_size': '21px',
                                  'color': "black", "paper_bgcolor": dash_colors['background'],'font-family': 'Times New Roman',
                                  "plot_bgcolor": dash_colors['background']
                              }, style_data={
                                  'whiteSpace': 'normal',
                                  'height': '20px'
                              },

                          ), html.Div(dcc.Markdown(' '),
                                      style={
                                          'textAlign': 'center',
                                          'color': '#FEFEFE'}),
                          html.Div(dcc.Markdown('''
            Built by [Laxmi Narayana Chilakala](https://www.linkedin.com/in/laxmi-narayana-chilakala/)  
            Source data: [covid19india](https://api.covid19india.org/)
            '''),
                                   style={
                                       'textAlign': 'center',
                                       'color': '#FEFEFE'})

                      ])
port=int(os.getenv("PORT",5000))
if __name__ == '__main__':
    app.run_server(debug=True,port=port)
    
