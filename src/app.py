import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
import io

messi_url=requests.get('https://raw.githubusercontent.com/Nipun142/Ronaldo_vs_Messi-Dashboard/main/src/messi.csv').content
ronaldo_url = requests.get('https://raw.githubusercontent.com/Nipun142/Ronaldo_vs_Messi-Dashboard/main/src/ronaldo.csv').content
ronaldo = pd.read_csv(io.StringIO(ronaldo_url.decode('utf-8')))
messi=pd.read_csv(io.StringIO(messi_url.decode('utf-8')))

temp='gridon'     #template for graphs
#--------------------------------------------------------------------------------------------------------------------------
# creating 2 new columns containing the year a goal is scored in and the integer form of it
def func(d):
    return d.split('/')[2]

messi['myear']=messi['Date'].apply(func)
ronaldo['ryear']=ronaldo['Date'].apply(func)

def my_func(d):
    return int(d)

messi['myear_int']=messi['myear'].apply(my_func)
ronaldo['ryear_int']=ronaldo['ryear'].apply(my_func)

#--------------------------------------------------------------------------------------------------------------------------

ronaldo_goal_count=ronaldo.groupby(by='ryear').count()
messi_goal_count=messi.groupby(by='myear').count()

#-------------------------------------------------------------------------------------------------------------------------

#Bar graph Club Goals scored each year

goal_each_year_bar_graph=go.Figure(data=[
    
    go.Bar(name='Ronaldo',
           x=ronaldo_goal_count.index,
           y=ronaldo_goal_count['Club'],
           marker={'color':'#43A1D5'},
           hovertemplate =
            '<br><b>Goals</b>  %{y}<br>'+
            '<b>20%{x}</b>'),
    go.Bar(name='Messi',
           x=messi_goal_count.index,
           y=messi_goal_count['Club'], 
           marker={'color':'#c6538c'},
           hovertemplate =
            '<br><b>Goals</b>  %{y}<br>'+
            '<b>20%{x}</b>')
    
])
goal_each_year_bar_graph.update_layout(xaxis_title="Year",
                    yaxis_title="Goals")
goal_each_year_bar_graph.update_layout(title={
        'text': "Club Goals Scored Each Year",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        template='seaborn')


#-------------------------------------------------------------------------------------------------------------------------

# Goals scored in different Competitions

ronaldo_tournament=ronaldo.groupby('Tournament').count()
messi_tournament=messi.groupby('Tournament').count()

ronaldo_tree_map=px.treemap(ronaldo_tournament,
                            path=[ronaldo_tournament.index,'Club'],
                            values='Club',
                            names='Club',
                           template=temp,
                            color_discrete_sequence=['#43A1D5','#c6538c'],
                           ) 
ronaldo_tree_map.update_traces(hovertemplate='<b>%{label} </b> <br>Goals %{value}<br>')


messi_tree_map=px.treemap(messi_tournament,
                          path=[messi_tournament.index,'Club'],
                          values='Club',
                          names='Club',
                         template=temp,
                         color_discrete_sequence=['#43A1D5','#c6538c'])
messi_tree_map.update_traces(hovertemplate='<b>%{label} </b> <br>Goals %{value}<br>')

#-------------------------------------------------------------------------------------------------------------------------

# Goals scored In different Ways

c=['Left-footed shot',
'Right-footed shot',
'Header',
'Solo run',
'Penalty',
'Direct free kick',
'Long distance kick',
'Tap-in',
'Not Applicable',
'Deflected shot on goal',
'Counter attack goal',
'Penalty rebound',
'Weak foot']


goal_types=pd.DataFrame(data=[
                [len(messi[messi['Goal Type']=='Left-footed shot']),
                 len(messi[messi['Goal Type']=='Right-footed shot']),
                 len(messi[messi['Goal Type']=='Header']),
                 len(messi[messi['Goal Type']=='Solo run']),
                 len(messi[messi['Goal Type']=='Penalty']),
                 len(messi[messi['Goal Type']=='Direct free kick']),
                 len(messi[messi['Goal Type']=='Long distance kick']),
                 len(messi[messi['Goal Type']=='Tap-in']),
                 len(messi[messi['Goal Type']=='Not Applicable']),
                 len(messi[messi['Goal Type']=='Deflected shot on goal']),
                 len(messi[messi['Goal Type']=='Counter attack goal']),
                 len(messi[messi['Goal Type']=='Penalty rebound']),
                 len(messi[messi['Goal Type']=='Right-footed shot'])
                    
                ],
                [
                 len(ronaldo[ronaldo['Goal Type']=='Left-footed shot']),
                 len(ronaldo[ronaldo['Goal Type']=='Right-footed shot']),
                 len(ronaldo[ronaldo['Goal Type']=='Header']),
                 len(ronaldo[ronaldo['Goal Type']=='Solo run']),
                 len(ronaldo[ronaldo['Goal Type']=='Penalty']),
                 len(ronaldo[ronaldo['Goal Type']=='Direct free kick']),
                 len(ronaldo[ronaldo['Goal Type']=='Long distance kick']),
                 len(ronaldo[ronaldo['Goal Type']=='Tap-in']),
                 len(ronaldo[ronaldo['Goal Type']=='Not Applicable']),
                 len(ronaldo[ronaldo['Goal Type']=='Deflected shot on goal']),
                 len(ronaldo[ronaldo['Goal Type']=='Counter attack goal']),
                 len(ronaldo[ronaldo['Goal Type']=='Penalty rebound']),
                 len(ronaldo[ronaldo['Goal Type']=='Left-footed shot'])
                ]
    
],columns=c,index=['Messi Goals','Ronaldo Goals'])



goal_types_transpose=goal_types.transpose()



goal_types_transpose=goal_types_transpose[goal_types_transpose['Ronaldo Goals']>5]  # Not consdering low goals value 
                                                                                



funnel_chart=px.funnel(goal_types_transpose, 
                          y=goal_types_transpose.index, 
                          x=['Messi Goals','Ronaldo Goals'],
                          template=temp,
                          color_discrete_sequence=['#43A1D5','#c6538c'],
                          labels={"variable":""}
                         )

funnel_chart.update_layout(
                           height = 800, 
                           title={'text': "Goal By",
                                     'y':0.94, 'x':0.5, 
                                     'xanchor': 'center', 'yanchor': 'top'},
                               legend=dict(orientation="v",
                                    yanchor="bottom",
                                    x=-0.4,
                                    y=1.04
                                    ),

                              )
funnel_chart.update_traces(hovertemplate='<b>%{y} </b> <br>Goals %{x}<br>')
funnel_chart.update_layout(yaxis_title="Goal Type")


#--------------------------------------------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#-----------------------------------------------------------------------------------------------------------------------

app.layout=html.Div([
    
    
        dbc.Row([
            
            dbc.Col([html.H1("Comparing the Incomparable: Messi vs Ronaldo",style={'textAlign':'center'}) ],
                    style={'textAlign': 'center',
                               'font-weight': 'bold', 'color':'#334668', 'background-color': '#CBC3E3'},width=12),
            
            
        ]),
           dbc.Container([ dbc.Row([
            dbc.Col([
                html.Hr(style={'height': '10px', 'color': '#00008B'}),
                
            ])
        ])]),
    
        dbc.Row([
            dbc.Col([
            dbc.Card([
                html.H6('Cristiano Ronaldo'),
                dbc.CardImg(src='/assets/Ronaldo Image 3.jpg',top=True,bottom=False),# 150px by 45px
            ],style={'textAlign':'center','background-color': '#8782C6'},
                className='mb-2', color="#8782C6", outline=False)
                                             
            ],style={"padding-left": "30px"}),
            
                        
    
            
            dbc.Col([
                
                dbc.Card([
                    html.H6("Lionel Messi"),
                    dbc.CardImg(src='/assets/Messi Image 2.jpeg',top=True,bottom=False), # 150px by 45px
                    
            ],style={'textAlign':'center','background-color': '#8782C6'},className='mb-2', color="#CBC3E3", outline=False)
            ],style={"padding-right": "10px"}),

        
                dbc.Col([
                html.Br(),
                html.Br(),
                html.H5([html.A("Lionel Messi", href='https://en.wikipedia.org/wiki/Lionel_Messi'),
                     " and ",
                     html.A('Cristiano Ronaldo', href='https://en.wikipedia.org/wiki/Cristiano_Ronaldo'),
                     " are two of the greatest football players of all time,and their individual achievements and records"
                         " are simply astonishing."]),
                html.Br(),
                html.H6("This Dashboard compares their Club Goal statistics. "),
                
                html.Br(),
                    
                html.H6("Who do You think is the Greatest Of All Time ?"),
                html.Br(),
                
                html.H6(["Created by ",html.A('Nipun Rao', href='https://www.linkedin.com/in/nipun-rao-a93898195/')]),
                    
                
            ],style={"padding-right": "50px"}),
        
        
        
        ]),
    

        dbc.Row([
            
            
            dbc.Col([
                dbc.Row([
               dcc.Graph(id='funnel_chart',figure=funnel_chart, style={
                                             "padding-left": "20px",})]),
                
            ],width={"size":4 ,"order": 0, "offset": 0}),
            
            dbc.Col([
                
                dbc.Row([
                    dbc.Row([
                dcc.Tabs(id='tab_value',value='Ronaldo_val',children=[
                    dcc.Tab(label='Messi',value='Messi_val'),
                    dcc.Tab(label='Ronaldo',value='Ronaldo_val'),
                ])
                    ]),
                    dbc.Row([
                dcc.Graph(id='tree_map' )])
                ]),
                dbc.Row([
                    html.Hr(style={'height': '5px', 'color': '#CBC3E3'}), 
                    dcc.Graph(id='bar_chart',figure=goal_each_year_bar_graph,style={
                                             "padding-right": "30px",})
                ])
            ])
            
        ]),


    
],style={'background-color':'#CBC3E3'},className="pad-row")  
    

@app.callback(
    Output('tree_map','figure'),
    Input('tab_value','value')
    )
def selector(choice):
    if choice=='Messi_val':
        messi_tree_map.update_layout(title='Messi Goals by Tournament')
        return messi_tree_map
    else:
        ronaldo_tree_map.update_layout(title='Ronaldo Goals by Tournament')
        return ronaldo_tree_map

app.run_server(port=8001)
