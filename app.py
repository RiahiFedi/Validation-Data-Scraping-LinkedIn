import time
#import importlib
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#from sklearn import datasets
#from sklearn.svm import SVC
#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
#import sklearn 
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
#from matplotlib.pyplot import figure
#from ds_utils.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
import plotly.figure_factory as ff
#from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from imblearn.over_sampling import SMOTE
import dash_table
import stat_des as sd
import utils.dash_reusable_components as drc
#import utils.figures as figs
from profile_sraping import scroll_down,get_driver ,login ,scrap


df=pd.read_csv('results_file_processed.csv')


from selenium import webdriver
import csv
from time import sleep
import parameters 
from bs4 import BeautifulSoup
import pandas as pd
import random
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os

# if field is present pass if field:pas if field is not present print text else:
def validate_field(field):
    if type(field) is not str:
       field = 'No results'
    return field


info = {'name' : [],
    'profile_title' : [], 
    'entreprise_name' : [],
    'duration' : [],
    'experience' : [],
    'location' : [],
    'education' : [],
    'nbr_employees' :[],
    'work_field' :[],
    'linkedin_url': []
    }



#Saves the data as a csv file
def save_res(): 
    df = pd.DataFrame(data=info)
    df.to_csv('results_file.csv', encoding = 'utf-8-sig')


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Support Vector Machine"
server = app.server


def generate_data(dataset = 'results_file_processed.csv'):
    if os.path.exists(dataset):
        return  pd.read_csv('results_file_processed.csv')
    else:
        raise ValueError(
            "Data file doesn't exist"
        )


app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "Post Scrapping Multi-Class Classification",
                                    href="https://github.com/plotly/dash-svm",
                                    style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src='https://scontent.ftun16-1.fna.fbcdn.net/v/t1.6435-9/42525465_265363214093156_8589220175729917952_n.png?_nc_cat=104&ccb=1-3&_nc_sid=09cbfe&_nc_ohc=gToJTR7EcOkAX-Gdpwv&_nc_ht=scontent.ftun16-1.fna&oh=5d44723e80d26a5d399514a1ab6ab415&oe=60CE00E3'
                                         ,style={'height':'10%', 'width':'10%'})
                            ],
                            href="https://www.wevioo.com/en",
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    className="row",
                    children=[
                        html.Div(
                            # className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        drc.NamedDropdown(
                                            name="Select Dataset",
                                            id="dropdown-select-dataset",
                                            options=[
                                                {"label": "results_file_processed.csv", "value": "results_file_processed.csv"},
                                                {
                                                    "label": "results_file_processed1.csv",
                                                    "value": "results_file_processed1.csv",
                                                },
                                                {
                                                    "label": "results_file_processed2.csv",
                                                    "value": "results_file_processed2.csv",
                                                },
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            value="results_file_processed.csv",
                                        ),
                                        html.Button('Refresh', id='refresh',
                                                    style={'BackgroundColor':'white'}),
                                        drc.NamedRadioItems(
                                            name='PCA',
                                            id='radio-stack-parameter-pca',
                                            labelStyle={
                                                'margin-right': '7px',
                                                'display': 'inline-block'
                                            },
                                            options=[
                                                {'label': ' Enabled', 'value': "True"},
                                                {'label': ' Disabled', 'value': "False"},
                                            ],
                                            value="True",
                                        ),
                                        drc.NamedRadioItems(
                                            name='SMOTE',
                                            id='radio-stack-parameter-smote',
                                            labelStyle={
                                                'margin-right': '7px',
                                                'display': 'inline-block'
                                            },
                                            options=[
                                                {'label': ' Enabled', 'value': "True"},
                                                {'label': ' Disabled', 'value': "False"},
                                            ],
                                            value="False",
                                        ),
                                    ],
                                ),
                                drc.Card(
                                    id="button-card",
                                    children=[
                                        dcc.Input(
                                            id="profile_urlinput_text",
                                            type="text",
                                            placeholder="Enter file path",
                                            #value = 'https://www.linkedin.com/in/fedi-riahi-46bb7b17a/',
                                            ),
                                        html.Button(
                                            "Confirm Profile",
                                            id="button-zero-threshold",
                                            style={'BackgroundColor':'white'}
                                        ),
                                        html.Div(id='output-container-button',
                                 children='Enter file path')
                                    ],
                                ),
                                drc.Card(
                                    id="last-card",
                                    children=[
                                        

                                        html.Div(
                                            id="shrinking-container",
                                            children=[
                                                html.P(children="Shrinking"),
                                                html.Button(
                                                    'Scrap Profile',
                                                    id='run',style={'BackgroundColor':'white'}),
                                                
                                                
                                                html.Br(),
                                                html.Br(),
                                                html.Button(
                                                    'Generate Prediction',
                                                    id='gen_pred',style={'BackgroundColor':'white'}),
                                                
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            style={'display': 'inline-block'},
                            id="div-graphs",
                            children=[dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),

]
                        ),
                        ],
                )
            ],
        ),
        html.Div(className='row',
                
            style={"width" : "100%",},
            children=[
                
                dash_table.DataTable(id='profile-table',
                   style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'lineHeight': '15px'},
                   style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                   style_cell={'fontSize':15,'color':'black'}
                   ),
                
                
                html.Br(),
                
                html.Div(
                            # className="three columns",
                            id="left-column_pf",
                            children=[
                                 html.Div(id='output-reaction',
                                 children='')
                                ]),
                html.Br(),
                html.Br(),
                dash_table.DataTable(id='data-table',
                                           style_data={
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'lineHeight': '15px'},
                                           style_cell_conditional=[
                                                {
                                                    'if': {'column_id': c},
                                                    'textAlign': 'left'
                                                } for c in ['Date', 'Region']],
                                           style_data_conditional=[
                                                    {
                                                        'if': {'row_index': 'odd'},
                                                        'backgroundColor': 'rgb(248, 248, 248)'
                                                    }],
                                           style_header={
                                                    'backgroundColor': 'rgb(230, 230, 230)',
                                                    'fontWeight': 'bold'
                                                },
                                           style_cell={'fontSize':15,'color':'black'}
                                           )])
   
    ]
)











@app.callback(
    Output("div-graphs", "children"),
    [
        Input('radio-stack-parameter-pca', 'value'),
        Input('radio-stack-parameter-smote', 'value'),
        Input("dropdown-select-dataset", "value"),
    ],
)
def update_svm_graph(
    pca,
    smote,
    dataset,
):

    # Data Pre-processing
    data = generate_data(dataset=dataset)
    counts = pd.crosstab(data.work_field,data.reaction)
    drop_l = []
    for i in list(counts.index):
        if sum(list(counts.loc[i,:])) < 5 :
            drop_l.append(i)
    for i in drop_l:
        data = data[data.work_field != i]
    
    cat_vars=[ 'work_field', 'region']
    for var in cat_vars:
        cat_list='var'+'_'+var
        cat_list = pd.get_dummies(data[var], prefix=var)
        data1=data.join(cat_list)
        data=data1
    cat_vars=['work_field', 'region','name_x', 'profile_title', 'entreprise_name','linkedin_url',]
    data_vars=data.columns.values.tolist()
    to_keep=[i for i in data_vars if i not in cat_vars]
    data_final=data[to_keep]
    
    X = data_final.loc[:, data_final.columns != 'reaction']
    y = data_final.loc[:, data_final.columns == 'reaction'] 
    
    encoder_ = LabelEncoder()
    
    for i in data_final:
        data_final[i]= encoder_.fit_transform(data_final[i])

    if pca=="True" :
        scaler = StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)
        
        pca = PCA(.95)
        pca.fit(X)
        X = pca.transform(X)
        X = pd.DataFrame(data = X)
    if smote=="True":
        os = SMOTE(random_state=0)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=3)
        columns = X.columns
        #X_train = X
        #y_train = y
        os_data_X,os_data_y=os.fit_sample(X_train, y_train)
        X_train = pd.DataFrame(data=os_data_X,columns=columns )
        y_train= pd.DataFrame(data=os_data_y,columns=['reaction'])
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=3)

    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

    
    
    
    # Train RF
    RFmodel = RandomForestClassifier(n_estimators=100,bootstrap = True,max_features = 'sqrt')
    RFmodel.fit(X_train, y_train)
    y_pred=RFmodel.predict(X_test)
    labels = np.unique(y_test)
    labels_str = []
    for i in labels:
        labels_str.append(str(i))
    x_ = labels_str
    y_ = labels_str
    z = confusion_matrix(y_test, y_pred, labels=labels)
    z_text = [[str(y) for y in x] for x in z]

   
    fig = ff.create_annotated_heatmap(z, x=x_, y=y_, annotation_text=z_text, colorscale='cividis')
    # add title
    fig.update_layout(title_text='<i><b>Confusion matrix</b></i>',
                      xaxis = dict(title='Predicted value'),
                      yaxis = dict(title='Real value'),
                      height= 500,
                      width =1000)
    

    
    # adjust margins to make room for yaxis title
    fig.update_layout(margin=dict(t=50, l=200))
    fig.update_layout(plot_bgcolor="silver", paper_bgcolor="silver")
    acc_str ="Accuracy:" + str(accuracy_score(y_test, y_pred))
    # add annotation
    fig.add_annotation(dict(font=dict(size=15),
                                            x=0,
                                            y=-0.12,
                                            showarrow=False,
                                            text=acc_str,
                                            textangle=0,
                                            xanchor='left',
                                            xref="paper",
                                            yref="paper"))
    
    # add colorbar
    fig['data'][0]['showscale'] = True


    return [
        html.Div(
            id="svm-graph-container",
            children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-sklearn-svm", figure=fig),
                style={"display": "none"},
            ),
        )
    ]
@app.callback([Output('data-table', 'data'),
               Output('data-table', 'columns')],
              [ Input('refresh', 'n_clicks')],
               [State('dropdown-select-dataset', 'value')],
              
            )
def update_table(n_clicks,data_name):
    
    df = generate_data(data_name)
    counts = pd.crosstab(df.work_field,df.reaction)
    drop_l = []
    for i in list(counts.index):
        if sum(list(counts.loc[i,:])) < 5 :
            drop_l.append(i)
    for i in drop_l:
        df = df[df.work_field != i]
    l_keep = ['name_x', 'profile_title', 'nbr_employees', 'work_field', 'reaction', 'region', 'current_job_duration', 'total_experience']
    data_final=df[l_keep]
    data_final = data_final.tail(10)
    columns = [{'name': col, 'id': col} for col in data_final.columns]
    data = data_final.to_dict(orient='records')
    return data, columns

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button-zero-threshold', 'n_clicks')],
    [dash.dependencies.State('profile_urlinput_text', 'value')])
def update_output(n_clicks, value):
    print('updated')
    return value


@app.callback([Output('profile-table', 'data'),
               Output('profile-table', 'columns'),
               Output('output-reaction','children')],
              [ Input('run', 'n_clicks'),
               Input('gen_pred', 'n_clicks')],
               [State('output-container-button', 'children'),
                State('profile-table', 'data'),
                State('profile-table', 'columns'),
                State('radio-stack-parameter-pca', 'value'),
                State('radio-stack-parameter-smote', 'value'),
                State("dropdown-select-dataset", "value")
                ],
              
            )
def update_table_profile(run,gen_pred,url,data_pf,columns_pf,pca,smote,dataset):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id=='run':    
        print(url)
        print('this was url')
        if  url!= '' and url != 'Enter file path':
            print(type(url))
            data = pd.DataFrame(scrap(login(False),str(url),initial_state = False), index=[0])
            columns = [{'name': col, 'id': col} for col in data.columns]
            data = data.to_dict(orient='records')
            print(data)
            return data, columns, ''
        else:
            info = {'name' : [],
        'profile_title' : [], 
        'entreprise_name' : [],
        'duration' : [],
        'experience' : [],
        'location' : [],
        'education' : [],
        'nbr_employees' :[],
        'work_field' :[],
        'linkedin_url': []
        }
            data = pd.DataFrame(data=info)
            columns = [{'name': col, 'id': col} for col in data.columns]
            data = data.to_dict(orient='records')
            #print(data)
            return data, columns, ''
        
    elif button_id == 'gen_pred':
        
        if  url!= '' and url != 'Enter file path':
            
            df_place_holder = pd.DataFrame(data=data_pf)
            data_pf_ = sd.data_process(df_place_holder)
            
            
            print('transformed data')
            print(data_pf_)
            
            data = generate_data(dataset=dataset)
            counts = pd.crosstab(data.work_field,data.reaction)
            drop_l = []
            for i in list(counts.index):
                if sum(list(counts.loc[i,:])) < 5 :
                    drop_l.append(i)
            for i in drop_l:
                data = data[data.work_field != i]
            
            data_pf_['reaction'] = ''
            
            placeholder_data = pd.concat([data,data_pf_])
            
            cat_vars=[ 'work_field', 'region']
            for var in cat_vars:
                cat_list='var'+'_'+var
                cat_list = pd.get_dummies(data[var], prefix=var)
                
                cat_list_='var'+'_'+var
                cat_list_ = pd.get_dummies(data_pf_[var], prefix=var)
                
                data1=data.join(cat_list)
                data_pf_=data_pf_.join(cat_list_)
                data=data1
            cat_vars=['work_field', 'region','name_x', 'profile_title', 'entreprise_name','linkedin_url',]
            
            data_vars=data.columns.values.tolist()
            to_keep=[i for i in data_vars if i not in cat_vars]
            data_final=data[to_keep]
            print('big data to keep')
            print(to_keep)
            
            cat_vars=['work_field', 'region','name', 'profile_title', 'entreprise_name','linkedin_url','education']
            data_vars=data_pf_.columns.values.tolist()
            to_keep=[i for i in data_vars if i not in cat_vars]
            print('this is keep')
            print(to_keep)
            data_pf_ = data_pf_[to_keep]
            
            X = data_final.loc[:, data_final.columns != 'reaction']
            y = data_final.loc[:, data_final.columns == 'reaction'] 
            
            encoder_ = LabelEncoder()
            
            
            print(data_final.columns.values.tolist())
            print(data_pf_.columns.values.tolist())
            
            for i in data_final:
                data_final[i]= encoder_.fit_transform(data_final[i])

                
            if pca=="True" :
                scaler = StandardScaler()
                scaler.fit(X)
                X = scaler.transform(X)
                
                
                pca = PCA(.95)
                pca.fit(X)
                
                
                X = pca.transform(X)
                X = pd.DataFrame(data = X)

            profile_X = X.tail(1)
            profile_y = y.tail(1)
            
            X = X.drop(index=X.index[-1], axis=0)
            y = y.drop(index=y.index[-1], axis=0)
            
            if smote=="True":
                os = SMOTE(random_state=0)
                #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
                X_train = X
                y_train = y
                columns = X.columns
                os_data_X,os_data_y=os.fit_sample(X_train, y_train)
                X_train = pd.DataFrame(data=os_data_X,columns=columns )
                y_train= pd.DataFrame(data=os_data_y,columns=['reaction'])
            else:
                #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
                X_train = X
                y_train = y
                
            # Train RF
            RFmodel = RandomForestClassifier(n_estimators=100, 
                                       bootstrap = True,
                                       max_features = 'sqrt')
            RFmodel.fit(X_train, y_train)
            
            profile_X['reaction'] = RFmodel.predict(profile_X)
            result = "This profile's predicted reaction is -> " + profile_X['reaction']
            return data_pf, columns_pf , result
        
        else:
            info = {'name' : [],
        'profile_title' : [], 
        'entreprise_name' : [],
        'duration' : [],
        'experience' : [],
        'location' : [],
        'education' : [],
        'nbr_employees' :[],
        'work_field' :[],
        'linkedin_url': []
        }
            data = pd.DataFrame(data=info)
            columns = [{'name': col, 'id': col} for col in data.columns]
            data = data.to_dict(orient='records')
            print(data)
            return data, columns ,''
            


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
