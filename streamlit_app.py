# Local File
#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!pip install pandas
#!pip install plotly
#!pip install dash
#!pip install dash_bootstrap_components


# In[3]:


import pandas as pd
import numpy as np
#pd.set_option('max_rows',20)
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


# In[4]:


#Get Data
test_df = pd.read_csv('C:/Users/Farida/Documents/Data_Science/P7/P7_test_df.csv')

test_df = test_df.drop(columns=['Unnamed: 0'])


# In[5]:


from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import GradientBoostingClassifier

Selected_Customer = test_df.loc[test_df['SK_ID_CURR'] == 100160]

feature_list = list(test_df.columns)

X = test_df.drop(['TARGET'], axis=1).values
y = test_df['TARGET'].values

data = Selected_Customer.drop(['TARGET'], axis=1).values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

undersample = RandomUnderSampler(sampling_strategy=1)
X_train, y_train = undersample.fit_resample(X_train, y_train)

gbc = GradientBoostingClassifier(n_estimators=836, min_samples_split=2, min_samples_leaf=2, max_depth=45)

score = gbc.fit(X_train, y_train).predict(data)

Credit_given_test = np.max(gbc.predict_proba(data))

if score==0:
  credit_score=Credit_given_test

else:
  credit_score=(1-Credit_given_test)

# Get numerical feature importances
importances = list(gbc.feature_importances_)

# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]

# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

#Ten most important features
ten_most_important = feature_importances[0:10]

ten_most_important_df = pd.DataFrame(ten_most_important)

ten_most_important_df.columns = ['Feature', 'Importance']

ten_most_important_df['Credit Granted?'] = None

if credit_score>=0.35:
  ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('Yes')
elif credit_score>=0.25:
  ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('Risky')
else:
  ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('No')

# Print out the feature and importances 
ten_most_important_df


#Generate Line Graph using Plotly
def Local_LIME():
    df = ten_most_important_df
   # df.head(10)
    yaxis_title = "Importance"
    fig = px.bar(df, y='Importance', x='Feature', title='Local Feature Importances',height=600,color='Importance')
    fig.update_layout(title_x=0.5,plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE',xaxis_title="Feature",yaxis_title=yaxis_title)
    return fig


# In[10]:


#DASH APP
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Credit Dashboard'
#Page Header
colors = {
    'background': '#111111',
    'bodyColor':'#F2DFCE',
    'text': '#7FDBFF'
}


# In[11]:


def get_page_heading_style():
    return {'backgroundColor': colors['background']}


def get_page_heading_title():
    return html.H1(children='Credit Dashboard',
                                        style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    })

def get_page_heading_subtitle():
    return html.Div(children='Local',
                                         style={
                                             'textAlign':'center',
                                             'color':colors['text']
                                         })

def generate_page_header():
    main_header =  dbc.Row(
                            [
                                dbc.Col(get_page_heading_title(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    subtitle_header = dbc.Row(
                            [
                                dbc.Col(get_page_heading_subtitle(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    header = (main_header,subtitle_header)
    return header


# In[12]:


def get_customer_list():
    return test_df['SK_ID_CURR'].unique()

def create_dropdown_list(cntry_list):
    dropdown_list = []
    for cntry in sorted(cntry_list):
        tmp_dict = {'label':cntry,'value':cntry}
        dropdown_list.append(tmp_dict)
    return dropdown_list

def get_country_dropdown(id):
    return html.Div([
                        html.Label('Select Customer'),
                        dcc.Dropdown(id='my-id'+str(id),
                            options=create_dropdown_list(get_customer_list()),
                            value='100004'
                        ),
                        html.Div(id='my-div'+str(id))
                    ])


# In[13]:


def graph1():
    return dcc.Graph(id='graph1',figure=Local_LIME())
#Generate CARDS for overall numbers
def generate_card_content(card_header,card_value,overall_value):
    card_head_style = {'textAlign':'center','fontSize':'150%'}
    card_body_style = {'textAlign':'center','fontSize':'200%'}
    card_header = dbc.CardHeader(card_header,style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5(f"{int(card_value):,}", className="card-title",style=card_body_style),
            html.P(
                "Worlwide: {:,}".format(overall_value),
                className="card-text",style={'textAlign':'center'}
            ),
        ]
    )
    card = [card_header,card_body]
    return card


# In[14]:


# In[15]:


def generate_layout():
    page_header = generate_page_header()
    layout = dbc.Container(
        [
            page_header[0],
            page_header[1],
            html.Hr(),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(get_country_dropdown(id=1),md=dict(size=4,offset=4))                    
                ]
            
            ),
            dbc.Row(
                [                
                    
                    dbc.Col(graph1(),md=dict(size=6,offset=3))
        
                ],
                align="center",

            ),            
        ],fluid=True,style={'backgroundColor': colors['bodyColor']}
    )
    return layout
app.layout = generate_layout()


# In[16]:


@app.callback(
    [Output(component_id='graph1',component_property='figure'), #bar chart
    Output(component_id='card1',component_property='children')], #overall card numbers
    [Input(component_id='my-id1',component_property='value')]#, #dropdown
    # Input(component_id='my-slider',component_property='value')] #slider
)
def update_output_div(input_value1,input_value2):
    return Local_LIME(input_value1,input_value2),generate_cards(input_value1)


# In[17]:


app.run_server(host= '0.0.0.0',debug=False)


# In[ ]:




