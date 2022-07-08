import dash
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import html,dcc
import requests
import pandas as pd
import numpy as np
import phonenumbers
from phonenumbers import carrier
from dash import dash_table
from wordcloud import WordCloud,STOPWORDS
import base64
from io import BytesIO


app = dash.Dash(__name__,suppress_callback_exceptions = True,external_stylesheets = [dbc.themes.FLATLY])

sidebar = dbc.Card([
        
        dbc.CardImg(src = 'https://x8hokg.deta.dev/stream/chips%20chicken.jpg'),
        html.Br(),
        dbc.Nav([
                dbc.NavLink('Account',href = '/',active = 'exact'),
                dbc.NavLink('Operation',href = '/operation',active = 'exact'),
                dbc.NavLink('Food',href = '/food',active = 'exact')
                ],vertical = True,pills = True)
        
        ],inverse = True,outline = False,style = {'background-color':'rgb(204, 235, 212)','height':'740px','border-style':'ridge','border-width':'5px'})

content = dbc.Col(id = 'content',width = 9)

app.layout = dbc.Container([
        html.Br(),
        dbc.Row([
                dcc.Location(id = 'url'),
                dbc.Col(sidebar,width = 3),
                content
                ])
        
        ],fluid = True)

@app.callback(Output('content','children'),Input('url','pathname'))
def content(pathname):
    
    if (pathname == '/') | (pathname == '/account_dataset') | (pathname == '/balance_dataset'):
        
        navigation = dbc.Nav([
                
                dbc.NavLink('Account Dashboard',href = '/',active = 'exact'),
                dbc.NavLink('Account Dataset',href = '/account_dataset',active = 'exact'),
                dbc.NavLink('Balance Dataset',href = '/balance_dataset',active = 'exact')
                
                ],pills = True)
    
        if pathname == '/':
            
            output = dbc.Row([
                    dbc.Row(navigation),
                    dbc.Row([html.Br()]),
                    dbc.Row([
                            
                            dbc.Col([
                                     dcc.Interval(id='interval-component2',interval=5*1000,n_intervals=0),
                                     dcc.Graph(id = 'bar-network',style = {'height':'350px'})],width = 6),
                            dbc.Col([
                                    dcc.Interval(id='interval-component',interval=5*1000,n_intervals=0),
                                    dcc.Graph(id = 'pie-location',style = {'height':'350px'})],width = 6)
                            
                            ]),
                    dbc.Row([
                            html.Br()
                            ]),
                    dbc.Row([
                            dbc.Col([dcc.Graph(id = 'line-balance',style = {'height':'300px'})],width = 8),
                            dbc.Col([dbc.Card([
                                    
                                    dbc.Row([html.Br(),html.Br(),html.Br()]),
                                    dbc.Row([
                                            dbc.Col([
                                                    
                                            dcc.Interval(id='interval-component3',interval=5*1000,n_intervals=0),
                                            dcc.Dropdown(id = 'drop-customer',value = 'precious nliwasa',style = {'color':'black'})
                                            
                                            ],width = {'size':8,'offset':2})
                                    ])
                                    ],style = {'height':'250px','background-color':'rgb(204, 235, 212)','border-style':'ridge','border-width':'5px','border-color':'rgb(204, 235, 212)'})],width = 4)
                            ])
                    ])
    
        elif pathname == '/account_dataset':
    
            output = dbc.Row([
                    dbc.Row(navigation),
                    dbc.Row([html.Br()]),
                    dbc.Row([dcc.Interval(id='interval-component4',interval=15*1000,n_intervals=0),html.Div(id = 'account-dataset')])
                    ])
    
        else:
            
            output = dbc.Row([
                    dbc.Row(navigation),
                    dbc.Row([html.Br()]),
                    dbc.Row([dcc.Interval(id='interval-component5',interval=15*1000,n_intervals=0),html.Div(id = 'balance-dataset')])
                    ])
    
    elif (pathname == '/food') | (pathname == '/food/menu'): 
        
        navigation = dbc.Nav([
                
                dbc.NavLink('Food Provided Dataset',href = '/food',active = 'exact'),
                dbc.NavLink('Menu Dataset',href = '/food/menu',active = 'exact')
                
                ],pills = True)
    
        if pathname == '/food':
            
            output = dbc.Row([
                    
                    dbc.Row(navigation),
                    dbc.Row([html.Br()]),
                    dbc.Row([
                            
                            dbc.Col([dcc.Interval(id ='interval-component6',interval = 5*1000,n_intervals = 0),html.Div(id = 'food-dataset')],width = 8),
                            dbc.Col([dbc.Card([
                                    
                                    dbc.Row([html.Br()]),
                                    dbc.Row([
                                            
                                            dbc.Col([
                                                    
                                                     dcc.Interval(id = 'interval-component8',interval = 2*1000,n_intervals = 0),
                                                     dcc.Dropdown(id = 'meal-options',value = 'chips',placeholder = 'enter meal')],width = {'size':8,'offset':2})
                                            ]),
                                    dbc.Row([html.Br()]),
                                    dbc.Row([dbc.Col([dbc.CardImg(id = 'meal-pic',style = {'border-style':'ridge','border-color':'rgb(19, 235, 112)'})],width = {'size':8,'offset':'2'})]),
                                    dbc.Row([html.Br()]),
                                    dbc.Row([dbc.Col([html.H3(id = 'meal-price')],width = {'size':8,'offset':2})]),
                                    dbc.Row([html.Br()]),
                                    dbc.Row([dbc.Col([html.H3(id = 'meal-description')],width = {'size':8,'offset':2})])
                                    
                                    ],style = {'background-color':'rgb(204, 235, 212)','height':'600px','border-style':'ridge','border-color':'rgb(19, 235, 112)','border-width':'5px'})],width = 4)
                            
                            ])
                    
                    ])
    
        else:
            
            output = dbc.Row([
                    
                    dbc.Row(navigation),
                    dbc.Row([html.Br()]),
                    dbc.Row([dcc.Interval(id ='interval-component7',interval = 5*1000,n_intervals = 0),html.Div(id = 'menu-dataset')])
                    
                    ])
        
    elif (pathname == '/operation') | (pathname == '/operation/operations') | (pathname == '/operation/orders'):
        
        navigation = dbc.Nav([
                
                dbc.NavLink('Operations Dashboard',href = '/operation',active = 'exact'),
                dbc.NavLink('Operations Dataset',href = '/operation/operations',active = 'exact'),
                dbc.NavLink('Orders Dataset',href = '/operation/orders',active = 'exact')
                
                ],pills = True)
    
        if pathname == '/operation':
            
            output = dbc.Row([
                    
                        dbc.Row([navigation]),
                        dbc.Row([html.Br()]),
                        dbc.Row([
                                
                                dbc.Row([
                                        
                                        dbc.Col([
                                                dcc.Interval(id ='interval-component12',interval = 10*1000,n_intervals = 0),
                                                dcc.Graph(id = 'time-order',style = {'height':'350px'})
                                                ],width = 7),
                                        dbc.Col([
                                                dcc.Interval(id ='interval-component11',interval = 180*1000,n_intervals = 0),
                                                html.Div(id = 'wordcloud-all',style = {'height':'350px'})
                                                ],width = 5)
                                        
                                        ]),
                                dbc.Row([html.Br()]),
                                dbc.Row([
                                        
                                        dbc.Col([
                                                dcc.Interval(id ='interval-component14',interval = 10*1000,n_intervals = 0),
                                                dcc.Graph(id = 'orders-total',style = {'height':'320px'})
                                                ],width = 6),
                                        dbc.Col([
                                                dcc.Interval(id ='interval-component13',interval = 10*1000,n_intervals = 0),
                                                dcc.Graph(id = 'operations-total',style = {'height':'320px','width':'480px'})
                                                ],width = 6)
                                        
                                        ])
                                
                                ])
                    
                    ])
            
        elif pathname == '/operation/operations':
            
            output = dbc.Row([
                    
                        dbc.Row([navigation]),
                        dbc.Row([html.Br()]),
                        dbc.Row([dcc.Interval(id='interval-component9',interval=3*1000,n_intervals=0),html.Div(id = 'operations-dataset')])
                    
                    ])
            
        else:
            
            output = dbc.Row([
                    
                        dbc.Row([navigation]),
                        dbc.Row([html.Br()]),
                        dbc.Row([dcc.Interval(id='interval-component10',interval=3*1000,n_intervals=0),html.Div(id = 'orders-dataset')])
                    
                    ])
        
        
    return output

def customer_data():
    
    customers = requests.get(url = 'https://x8hokg.deta.dev/get_customers/')
    
    df = pd.DataFrame(customers.json()['_items'])  
    
    return df
    

@app.callback(Output('pie-location','figure'),[Input('interval-component','n_intervals')])
def Pie_loc(n):
    
    df = customer_data()
    
    df2 = df.groupby('Location')[['Full Name']].count()
    
    graph_data = [go.Pie(values = df2['Full Name'].values,labels = df2.index,hole = 0.7)]
    
    layout = go.Layout(title = 'Customers By Location',
                        plot_bgcolor = 'rgb(204, 235, 212)',
                        paper_bgcolor = 'rgb(204, 235, 212)')
    
    return dict(data = graph_data,layout = layout)
    

@app.callback(Output('bar-network','figure'),Input('interval-component2','n_intervals'))
def bar_net(n):
    
    df = customer_data()
    
    phone_ = []
    
    for i in df['Phone Number'].str.split(':').str[1]:
        phone_.append(phonenumbers.parse(i))
        
    network = []
    
    for i in phone_:
        network.append(carrier.name_for_number(i,'en'))
        
    labels = pd.Series(network).value_counts() .index
    values = pd.Series(network).value_counts().values
    
    np.random.seed(567)
    bar = [go.Bar(y = labels,x = values,orientation = 'h',marker = dict(color = list(np.random.choice(['rgb(242, 58, 64)','rgb(144, 58, 242)','rgb(58, 221, 242)','rgb(242, 113, 58)'],replace = False,size = len(labels)))))]
    
    layout = go.Layout(title = 'Customers By Network Carrier',
                        plot_bgcolor = 'rgb(204, 235, 212)',
                        paper_bgcolor = 'rgb(204, 235, 212)',
                        xaxis = dict(title = 'Counts'),
                        yaxis = dict(title = 'Network'))
    
    return dict(data = bar,layout = layout)
    #return bar
def balances_dataset():
    
    balance = requests.get('https://x8hokg.deta.dev/account_balances/')
    
    balance_df = pd.DataFrame(balance.json()['_items'])
    
    balance_df.Time = pd.to_datetime(balance_df.Time)
    
    balance_df.index = balance_df.Time
    
    balance_df.drop('Time',axis = 'columns',inplace = True)
    
    balance_df.sort_values('Time',inplace = True)
    
    return balance_df
    
@app.callback(Output('drop-customer','options'),Input('interval-component3','n_intervals'))
def options_customer(n):
    
    df = balances_dataset()
    names_ = df['Full Name'].unique()
    
    options_a = {'options':list(names_)}
    
    return [{'label':str(i),'value':str(i)} for i in list(options_a['options'])]

@app.callback(Output('line-balance','figure'),Input('drop-customer','value'))
def line_balance(options):
    
    df = balances_dataset()
    
    df = df.loc[df['Full Name'] == options]
    
    scatter_data = [go.Scatter(x = df.index,y = df.Amount,mode = 'text+lines',marker = dict(color = 'rgb(242, 58, 58)'),text = [str(i) for i in df.Amount])]
    
    layout = go.Layout(title = 'Balance by Date',
                        plot_bgcolor = 'rgb(204, 235, 212)',
                        paper_bgcolor = 'rgb(204, 235, 212)',
                        xaxis = dict(title = 'Time'),
                        yaxis =dict(title = 'Balance'))
    
    return dict(data = scatter_data,layout = layout)

@app.callback(Output('account-dataset','children'),Input('interval-component4','n_intervals'))
def account_datasets_output(n):
    
    account_df  = customer_data()[['Full Name','Email','Phone Number','Location']]
    
    table =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in account_df.columns
               ],
                    data = account_df.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 19,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95,'background-color':'rgb(204, 235, 212)','color':'black'},
                    style_header = {'background-color':'rgb(19, 235, 112)'})
    
    return table

@app.callback(Output('balance-dataset','children'),Input('interval-component5','n_intervals'))
def balance_datasets_output(n):
    
    balance_df  = balances_dataset()[['Full Name','Amount']]
    
    table =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in balance_df.columns
               ],
                    data = balance_df.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 19,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95,'background-color':'rgb(204, 235, 212)','color':'black'},
                    style_header = {'background-color':'rgb(19, 235, 112)'})
    
    return table

def food_dataset():
    
    food_ = requests.get(url = 'https://x8hokg.deta.dev/get_food/')
    
    food_db = pd.DataFrame(food_.json()['_items'])
    
    return food_db

@app.callback(Output('food-dataset','children'),Input('interval-component6','n_intervals'))
def food_datasets_output(n):
    
    food_df  = food_dataset()[['Food','Price']]
    
    table =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in food_df.columns
               ],
                    data = food_df.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 19,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95,'background-color':'rgb(204, 235, 212)','color':'black'},
                    style_header = {'background-color':'rgb(19, 235, 112)'})
    
    return table

def menu_dataset():
    
    menu_ = requests.get(url = 'https://x8hokg.deta.dev/get_menu/')
    
    menu_db = pd.DataFrame(menu_.json()['_items'])
    
    return menu_db[['Food','Time']]

@app.callback(Output('menu-dataset','children'),Input('interval-component7','n_intervals'))
def menu_datasets_output(n):
    
    menu_df  = menu_dataset()
    
    table =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in menu_df.columns
               ],
                    data = menu_df.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 19,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95,'background-color':'rgb(204, 235, 212)','color':'black'},
                    style_header = {'background-color':'rgb(19, 235, 112)'})
    
    return table


@app.callback(Output('meal-options','options'),Input('interval-component8','n_intervals'))
def meal_options(n):
    
    food_df  = food_dataset()
    names_ = food_df['Food'].unique()
    
    options_a = {'options':list(names_)}
    
    return [{'label':str(i),'value':str(i)} for i in list(options_a['options'])]


@app.callback(Output('meal-pic','src'),Input('meal-options','value'))  
def meal_pic(option):
                
    if len(option.split(' ')) == 1:
                    
        pic_url = 'https://x8hokg.deta.dev/stream/{}.jpg'.format(option)
                    
    else:
                    
        first = option.split(' ')[0]
        second = option.split(' ')[1]
                    
        pic_url = 'https://x8hokg.deta.dev/stream/{}%20{}.jpg'.format(first,second)
        
    return pic_url

@app.callback([Output('meal-price','children'),Output('meal-description','children')],Input('meal-options','value'))  
def meal_price_description(option):
    
    food_df = food_dataset()
    
    price_df = food_df.loc[food_df['Food'] == option]
    
    return html.H5(['Price : Mk' + str(price_df.Price.values[0])],style = {'border-radius':'10px','border-style':'ridge','padding':'10px','border-color':'rgb(19, 235, 112)'}),html.H5(['Description : ' + str(price_df.Description.values[0])],style = {'border-radius':'10px','border-style':'ridge','padding':'10px','border-color':'rgb(19, 235, 112)'})
    

def operations_dataset():
    
    operations_ = requests.get(url = 'https://x8hokg.deta.dev/get_all_operations/')
    
    operations_db = pd.DataFrame(operations_.json()['_items'])
    
    return operations_db

@app.callback(Output('operations-dataset','children'),Input('interval-component9','n_intervals'))
def operations_datasets_output(n):
    
    operations_df  = operations_dataset()[['User','Operation','Message','time']]
    
    table =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in operations_df.columns
               ],
                    data = operations_df.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 19,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95,'background-color':'rgb(204, 235, 212)','color':'black'},
                    style_header = {'background-color':'rgb(19, 235, 112)'})
    
    return table

def orders_dataset():
    
    orders_ = requests.get(url = 'https://x8hokg.deta.dev/get_orders/')
    
    orders_db = pd.DataFrame(orders_.json()['_items'])
    
    return orders_db

@app.callback(Output('orders-dataset','children'),Input('interval-component10','n_intervals'))
def orders_datasets_output(n):
    
    orders_df  = orders_dataset()[['Food','Price','Phone Number','Time']]
    
    table =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in orders_df.columns
               ],
                    data = orders_df.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 19,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95,'background-color':'rgb(204, 235, 212)','color':'black'},
                    style_header = {'background-color':'rgb(19, 235, 112)'})
    
    return table


@app.callback(Output('wordcloud-all','children'),Input('interval-component11','n_intervals'))
def wordcloud_output(n):
    
    messages = str(operations_dataset().Message)
    
    stopwords_ = set(STOPWORDS)
    
    wc = WordCloud(stopwords = stopwords_,background_color = 'rgb(204, 235, 212)',height = 351,width = 400,max_words = 300,max_font_size = 60).generate(messages)
    wc_img = wc.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()
        
    return html.Img(src="data:image/png;base64," + img2)

@app.callback(Output('time-order','figure'),Input('interval-component12','n_intervals'))
def orders_time_bar_output(n):
    
    orders = orders_dataset()
    
    orders.Time = pd.to_datetime(orders.Time)
    
    orders.index = orders.Time
    
    orders.drop('Time',axis = 'columns',inplace = True)
    
    orders.sort_values('Time',inplace = True)
    
    scatter_data = [go.Scatter(x = orders.index,y = orders.Price,mode = 'lines',marker = dict(color = 'rgb(242, 58, 58)'))]
    
    layout = go.Layout(title = 'Orders By Time',
                        plot_bgcolor = 'rgb(204, 235, 212)',
                        paper_bgcolor = 'rgb(204, 235, 212)',
                        xaxis = dict(title = 'Time'),
                        yaxis = dict(title = 'Order (Price)'))
    
    return dict(data = scatter_data,layout = layout)
    
@app.callback(Output('operations-total','figure'),Input('interval-component13','n_intervals'))
def operations_bar_output(n):    
    
    operations = operations_dataset()
    
    labels = operations.Operation.value_counts().index
    values = operations.Operation.value_counts().values
    
    bar_data = [go.Bar(x = labels,y = values,marker = dict(color = 'rgb(242, 58, 58)'))]
    
    layout = go.Layout(title = 'Total Operations By Type',
                        plot_bgcolor = 'rgb(204, 235, 212)',
                        paper_bgcolor = 'rgb(204, 235, 212)',
                        yaxis = dict(title = 'Counts'))
    
    
    return dict(data = bar_data,layout = layout)

@app.callback(Output('orders-total','figure'),Input('interval-component14','n_intervals'))
def orders_bar_output(n):    
    
    orders = orders_dataset()
    
    labels = orders.Food.value_counts().index
    values = orders.Food.value_counts().values
    
    bar_data = [go.Bar(x = labels,y = values)]
    
    layout = go.Layout(title = 'Total Orders By Food',
                        plot_bgcolor = 'rgb(204, 235, 212)',
                        paper_bgcolor = 'rgb(204, 235, 212)',
                        yaxis = dict(title = 'Counts'))
    
    
    return dict(data = bar_data,layout = layout)

if __name__ == '__main__':
    app.run_server(debug = True)