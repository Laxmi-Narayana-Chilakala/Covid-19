#!/usr/bin/env python
# coding: utf-8

# In[230]:


import numpy as np
import pandas as pd
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html


# In[ ]:





# In[231]:



# loading data right from the source:
death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')


# In[232]:


country_df.columns = map(str.lower, country_df.columns)
confirmed_df.columns = map(str.lower, confirmed_df.columns)
death_df.columns = map(str.lower, death_df.columns)
recovered_df.columns = map(str.lower, recovered_df.columns)
                           
confirmed_df = confirmed_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
recovered_df = recovered_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
death_df = death_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
country_df = country_df.rename(columns={'country_region': 'country'})


# In[233]:


country_df.head(3)


# In[234]:


death_df.head()


# In[235]:


confirmed_df.iloc[:,4:].sum()


# In[236]:


sorted_df=country_df.sort_values(["confirmed"],ascending=False)


# In[237]:


sorted_df[:10]


# In[238]:


confirmed_cases=country_df['confirmed'].sum()
deaths=country_df['deaths'].sum()
recovered_cases=country_df['recovered'].sum()


# In[239]:


confirmed_cases,deaths,recovered_cases


# In[ ]:





# In[240]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app=dash.Dash(__name__, external_stylesheets=external_stylesheets)


# In[241]:


dash_colors = {
    'background': '#111111',
    'text': '#BEBEBE',
    'grid': '#333333',
    'red': '#BF0000'
}


# In[ ]:





# In[256]:


app.layout=html.Div(style={'backgroundColor': dash_colors['background']},
    children=[
    html.H1(children="Covid-19 DashBoard",
           style={
               'textAlign':'center',
               'color': 'red'
           }),
    html.H5("World-wide Confirmed cases: {}".format(confirmed_cases),
            style={
               'textAlign':'center',
               'color': 'blue'
           }), 
    html.H5("Recovered cases: {}".format(recovered_cases),
            style={
               'textAlign':'center',
               'color': 'blue'
           }),
    html.H5("Deaths: {}".format(deaths),
            style={
               'textAlign':'center',
               'color': 'blue'
           }),
    
    dcc.Graph(
    id='sample-graph1',
        figure={
            'data':[
                {'x':sorted_df['country'][:10],'y':sorted_df['confirmed'][:10],'type':'bar','name':'confirmed'},
                {'x':sorted_df['country'][:10],'y':sorted_df['recovered'][:10],'type':'bar','name':'recovered'},
                {'x':sorted_df['country'][:10],'y':sorted_df['deaths'][:10],'type':'bar','name':'deaths'}
            ],
            'layout':{
                'title':"Highly Affected Countries",
                "paper_bgcolor": dash_colors['background'],
                "plot_bgcolor": dash_colors['background'],
                "font":{"color":'white'}
                
            }
        }),
        dcc.Graph(
            id='sample-graph2',
        figure={
            'data':[
                {'x':confirmed_df.iloc[:,4:].columns,'y':confirmed_df.iloc[:,4:].sum(),'type':'line','name':'confirmed'},
                {'x':confirmed_df.iloc[:,4:].columns,'y':death_df.iloc[:,4:].sum(),'type':'line','name':'deaths'},
                {'x':confirmed_df.iloc[:,4:].columns,'y':recovered_df.iloc[:,4:].sum(),'type':'line','name':'recovered'}
            ],
            'layout':{
                'title':"Trend of Covid-19 in World",
                "paper_bgcolor": dash_colors['background'],
                "plot_bgcolor": dash_colors['background'],
                "font":{"color":'white'}
                
            }
        }),
        html.H6("Total US Confirmed cases: {}".format(country_df[country_df['country']=='US']['confirmed'].sum()),
            style={
               'textAlign':'center',
               'color': '#fcbe03'
           }), 
        html.H6("Recovered cases: {}".format(country_df[country_df['country']=='US']['recovered'].sum()),
            style={
               'textAlign':'center',
               'color': '#fcbe03'
           }),
        html.H6("Deaths: {}".format(country_df[country_df['country']=='US']['deaths'].sum()),
            style={
               'textAlign':'center',
               'color': '#fcbe03'
           }),
    
 
        dcc.Graph(
            id='sample-graph3',
        figure={
            'data':[
                {'x':confirmed_df[confirmed_df['country']=='US'].iloc[:,4:].columns,'y':confirmed_df[confirmed_df['country']=='US'].iloc[:,4:].sum(),'type':'line','name':'confirmed'},
                {'x':confirmed_df[confirmed_df['country']=='US'].iloc[:,4:].columns,'y':death_df[death_df['country']=='US'].iloc[:,4:].sum(),'type':'line','name':'deaths'},
                {'x':confirmed_df[confirmed_df['country']=='US'].iloc[:,4:].columns,'y':recovered_df[recovered_df['country']=='US'].iloc[:,4:].sum(),'type':'line','name':'recovered'}
            ],
            'layout':{
                'title':"Covid-19 Trend in US",
                "paper_bgcolor": dash_colors['background'],
                "plot_bgcolor": dash_colors['background'],
                "font":{"color":'white'}
                
            }
        }),
        html.H6("Total Indian Confirmed cases: {}".format(country_df[country_df['country']=='India']['confirmed'].sum()),
            style={
               'textAlign':'center',
               'color': '#fc2803'
           }), 
        html.H6("Recovered cases: {}".format(country_df[country_df['country']=='India']['recovered'].sum()),
            style={
               'textAlign':'center',
               'color': '#fc2803'
           }),
        html.H6("Deaths: {}".format(country_df[country_df['country']=='India']['deaths'].sum()),
            style={
               'textAlign':'center',
               'color': '#fc2803'
           }),
    
        dcc.Graph(
            id='sample-graph4',
        figure={
            'data':[
                {'x':confirmed_df[confirmed_df['country']=='India'].iloc[:,4:].columns,'y':confirmed_df[confirmed_df['country']=='India'].iloc[:,4:].sum(),'type':'line','name':'confirmed'},
                {'x':confirmed_df[confirmed_df['country']=='India'].iloc[:,4:].columns,'y':death_df[death_df['country']=='India'].iloc[:,4:].sum(),'type':'line','name':'deaths'},
                {'x':confirmed_df[confirmed_df['country']=='India'].iloc[:,4:].columns,'y':recovered_df[recovered_df['country']=='India'].iloc[:,4:].sum(),'type':'line','name':'recovered'}
            ],
            
            'layout':{
                'title':"Covid-19 Trend in India",
                "paper_bgcolor": dash_colors['background'],
                "plot_bgcolor": dash_colors['background'],
                "font":{"color":'white'},
                
                
            }
        }),
        html.Div(dcc.Markdown(' '),
                 style={
            'textAlign': 'center',
            'color': '#FEFEFE'}),
        html.Div(dcc.Markdown('''
            Built by [Laxmi Narayana Chilakala](https://www.linkedin.com/in/laxmi-narayana-chilakala/)  
            Source data: [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)
            '''),
            style={
                'textAlign': 'center',
                'color': '#FEFEFE'})
])


# In[257]:


if __name__ == '__main__':
    app.run_server()


# In[249]:


dash.__version__


# In[250]:


dcc.__version__


# In[251]:


html.__version__


# In[252]:


np.__version__


# In[253]:


plotly.__version__


# In[ ]:




