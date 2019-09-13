# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 01:22:22 2019

@author: Sireesha Chamarthi
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from inputs import *
from error_calculator import Error_calculator
import plotly.graph_objs as go
import numpy as np
import dash_bootstrap_components as dbc
from scipy import interpolate




# print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.

app.config['suppress_callback_exceptions']=True
colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}
astrometry_type = ['Differential astrometry (relative to field stars)', 'Differential astrometry (science objects relative to each other)', 'Absolute Astrometry']


app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
     
    html.Div([
    html.H1('TMT-IRIS Astrometry Error Budget Tool' ,
    style={'color': 'white', 'font-style': 'italic', 'font-weight': 'bold','textAlign':'center'}
    ),

#    html.Div([
#    dcc.RadioItems(
#            id='astrometry-type-id',
#            options=[{'label': i, 'value': i} for i in astrometry_type],
#            value=astrometry_type[0],
#            labelStyle={'display': 'inline-block'}
#        ),
#    ],style={'width': '30%', 'float':'center', 'display': 'inline-block','textAlign':'center','margin-right': '500px', 'margin-top': '25px'}),
    
    html.Div([
    html.Label('Astrometry science case'),
    dcc.Dropdown(
            id='astrometry-type-id',
            options=[{'label': i, 'value': i} for i in astrometry_type],
            value=astrometry_type[0],
            multi = False,
            style={'color':'black'}
                ),
    ],
    
    style={'width': '40%', 'color': 'white','float':'center', 'display': 'inline-block','textAlign':'center','font-weight': 'bold','margin-right': '400px','margin-left': '50px','margin-bottom': '10px'}),
    # html.Div(id='blankspace1-id',
    #     style={'width': '30%', 'float':'center', 'display': 'inline-block'}),
    
	html.Button(id = 'Calculate',n_clicks=0,children='Calculate', style={'width': '10%','backgroundColor': 'white','opacity': '1','font-weight': 'bold','color': 'black', 'float':'right', 'display': 'inline-block','margin-left': '10px','margin-right': '150px','margin-top': '20px'}),
                  
               
############################3tabs############################################
             
     ###################### output ############################################
    

    html.Div(id='ls-id',
        style={'width': '30%', 'color': 'white','font-weight': 'bold','float':'center', 'display': 'inline-block'}),

    html.Div(id='final_output-id',
#        style={'width': '30%', 'float':'right', 'display': 'inline-block'}),
        style={'backgroundColor': '#111111','opacity': '.8','width':'50%','color': 'white','float':'center', 'font-weight': 'bold','textAlign':'center','font-size':'25px','margin-bottom': '10px','margin-left': '20%'}),


############################## observation field #################################




    html.Div(
    dcc.Tabs(id="tabs",style={'width': '100%',
        'font-size': '50%',
        'height': '100%','font-weight': 'bold','fontSize': 14}, vertical = False,
        children=[
    dcc.Tab(label='Science Input', style={
        'width': '100%',
        'font-size': '50%',
        'height': '100%',
        'backgroundColor': '#111111','opacity': '.8','font-weight': 'bold','color':'white','fontSize': 14
    },
            children=[
             html.Div([      
                         
                       
                       
                       
     
        ## Field of observation
        html.H5(children='Observation Field',
            style={ 'backgroundColor': '#FFFFFF','textAlign': 'center','font-weight': 'bold','color':'black'},
               ),
                
                
                 ## Nsci input
            # header
        html.Div(children='Number of science objects',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
            ),
            # input tab
        html.Div([
        dcc.Input(id='Nsci-id', value=1, type='number',min=0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                  
                ]),
                  
                  
           ## Nfield input
            # header
        html.Div(children='Number of field stars',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='Nfield-id', value=1, type='number',min=0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                  
                 ]),        
        
          
                  
                  
                   ## Nref input
            # header
        html.Div(children='Number of reference stars',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='Nref-id', value = 1, type='number',min=0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                  
                 ]),

                  
                     ## Nngs input
            # header
        html.Div(children='Number of NGS stars',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='Nngs-id', value = 3, type='number',min=1,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                  
                 ]),          
        
                   
                         html.Div(children='Mag(Vega) Science Obj',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text'],'float':'center'}
                ),
            # input tab
        html.Div([
        dcc.Input(id='SNR-sci-id', value = 20, type='number',
                  style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                 ]),      
                  
                   ## SNR field input
            # header
        html.Div(children='Mag(Vega) Field Obj',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='SNR-fie-id', value = 20, type='number',
                  style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                 ]),

        ## SNR sci input
            # header
        html.Div(children='Mag(Vega) Ref Obj',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='SNR-ref-id', value = 20, type='number',
                  style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                 ]),
                        ## r ref-sci input input
            # header
        html.Div(children= 'R ref_ sci (arcsec)',  
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']
                  }
                 ),
            # input tab
        html.Div([
        dcc.Input(id='rref-sci-id', value = 10, type='number',step=0.01,min =0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                  
         
                 ]),

           ## r detla science input
            # header
        html.Div(children='R delta sci (arcsec)',
         
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']
                  }
                 ),
            # input tab
        html.Div([
        dcc.Input(id='rdsci-id', value = 1, type='number',step=0.01,min =0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
         
                 ]),
         
     

       

       
          
                  
      

            ],style={'backgroundColor': '#111111','opacity': '.8','width': '30%','float': 'left','display': 'inline-block','margin-top': '10px','margin-right': '175px','margin-left': '50px','height': '620px'}),
                  
                       
                       
   ############################## GLOBAL INPUTS##############################
            
                       
                       
                       
                       
     html.Div(children=[
                 
                      
        ## global header
        html.H5(children='Global inputs',
            style={ 'backgroundColor': '#FFFFFF','textAlign': 'center','font-weight': 'bold','color':'black'},
            ),
                
                
        ## wavelength input
                # header
        html.Div(children='Filter',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
                
                
                # input tab
        # html.Div([
        # dcc.Input(id='wavelength-id', value = 0.0000025, type='number',
                  # step=1e-7,min =0.0000008,max=0.0000025,
                  # style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                 # ]),

                dcc.Dropdown(
                                id='wavelength-id',
                                options=[{'label': 'Z', 'value': 0.000000928 }, {'label': 'Y', 'value': 0.00000109 }, {'label': 'J', 'value': 0.00000127 }, {'label': 'H', 'value': 0.000001629 }, {'label': 'K', 'value': 0.000002182 },],
                                multi = False,
                                value=0.000000928,style={'textAlign': 'center','margin-left': '50px','width':'70%','textAlign':'center'} 
                                
                                
                                
                ),
         ## SNR sci input
            # header
 

        ## RNGS input
                # header
        html.Div(children='R_NGS (arcsec)',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                 ),
                # input tab
        html.Div([
        dcc.Input(id='RNGS-id', value=50, type='number',step=0.01,min =0,
                  style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
               
                 ]),

        ## Rref input
            # header
        html.Div(children='R_ref (arcsec)',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='rref-id', value=17, type='number',step=0.01,min =0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
 
                 ]),

        ## T input
            # header
        html.Div(children='Integration time  (s)',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='T-id', value=100, type='number',step=0.01,min =0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),
                ]),

        ## dt input
            # header
        html.Div(children='dt_epoch (yr)',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='dt-id', value=1.5, type='number',step=0.01,min =0,
        style={'textAlign': 'center','margin-left': '100px','width':'50%'}),

                 ]),
            ],style={'backgroundColor': '#111111','opacity': '.8','width': '30%','float': 'center','display': 'inline-block','margin-top': '10px','margin-right': '15px','margin-left': '50px','height': '400px'}),
                        
         
                  





     ]),

###################### Engineering ##############################
 dcc.Tab(label='Engineering Input',style={
        'width': '100%',
        'font-size': '50%',
        'height': '100%',
        'backgroundColor': '#111111','opacity': '.8','font-weight': 'bold','color':'white','fontSize': 14
    }, 
            children=[
            html.Div([               

                       

        ## User defined variances
        html.H5(children='Opto-mechanical',
            style={ 'backgroundColor': '#FFFFFF','textAlign': 'center','font-weight': 'bold','color':'black'},
               ),
       
        ## NGS Position Error
            # header
        html.Div(children='NGS Position Error',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='NGS-perr-id', value = 2000, type='number',step =5,min=0,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),

        ## NFIRAOS/IRIS optics
            # header
        html.Div(children='NFIRAOS/IRIS optics',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text'],'margin-left': '15px'}
                ),
            # input tab
        html.Div([
        dcc.Input(id='IRIS-opt-id', value = 8, type='number',step=1,min=1,max=50,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
        
                 ]),

        ## NFIRAOS/IRIS surfaces
            # header
        html.Div(children='NFIRAOS/IRIS surfaces',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='IRIS-surf-id', value=4, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Quasi-static distortions
            # header
        html.Div(children='Quasi-static distortions',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='quas-stat-id', value=5, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Telescope Optics
            # header
        html.Div(children='Telescope Optics',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='tel-opt-id', value=5, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Rotator errors
            # header
        html.Div(children='Rotator errors',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='rot-err-id', value=3, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Actuator spikes
            # header
        html.Div(children='Actuator spikes',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='act-spike-id', value=1, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Vibration
            # header
        html.Div(children='Vibration',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='vib-id', value=5, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Coupling with atm.
            # header
        html.Div(children='Coupling with atm.',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='coup-atm-id', value=3, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

            ],style={'backgroundColor': '#111111','opacity': '.8','width': '30%','float': 'left','display': 'inline-block','margin-top': '10px','margin-right': '50px','margin-left': '10px','height': '650px'}),

                                         
                       
                       
                       
                       
                       
           ###################### focal plane ##############################
                    
                       
    html.Div(children=[

        html.H5(children='Focal Plane',
            style={ 'backgroundColor': '#FFFFFF','textAlign': 'center','font-weight': 'bold','color':'black'},
               ),
       
        ## Noise Calibration
            # header
        html.Div(children='Noise Calibration',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='Ncal-id', value = 5, type='number',step =0.1,min=0,max=10,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),
                  
                  
        ## Pixel blur calibration
            # header
        html.Div(children='Pixel blur calibration',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='pix-blur-id', value = 5, type='number',step =0.1,min=0,max=10,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),
                  
                  
         ## Pixel irregularities
            # header
        html.Div(children='Pixel irregularities',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='pix-irr-id', value = 5, type='number',step =0.1,min=0,max=10,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),         
                  

         ## Detector non linerity
            # header
        html.Div(children='Detector non linerity',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='dect-non-id', value = 1, type='number',step =0.1,min=0,max=5,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),  

                  
      ## PSF knowledge
            # header
        html.Div(children='PSF knowledge',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='PSF-id', value = 5, type='number',step =5,min=0,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),  
                  
                  
      ## Confusion
            # header
        html.Div(children='Confusion',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='confu-id', value = 5, type='number',step =5,min=0,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),
                  
                   html.H5(children='Residual Turbulance',
            style={ 'backgroundColor': '#FFFFFF','textAlign': 'center','font-weight': 'bold','color':'black'},
               ),
       
        ## Halo Effect
            # header
        html.Div(children='Halo Effect',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='halo-id', value = 3, type='number',step =0.1,min=0,max=5,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),

        ## Turbulance Condition Variability
            # header
        html.Div(children='Turb. variability',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text'],'margin-left': '15px'}
                ),
            # input tab
        html.Div([
        dcc.Input(id='turb-var-id', value = 1, type='number',step=1,min=1,max=50,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
        
                 ]),
        ],style={'backgroundColor': '#111111','opacity': '.8','width': '30%','float': 'center','display': 'inline-block','margin-top': '10px','margin-right': '10px','margin-left': '10px','height': '650px'}),
       

    ###################### ATMOSPHERIC REFRACTION VARIANCES ##############################

    html.Div(children=[
        ## User defined variances
        html.H5(children='Atmospheric refraction',
            style={ 'backgroundColor': '#FFFFFF','textAlign': 'center','font-weight': 'bold','color':'black'},
               ),
       
        ## NGS Position Error
            # header
        html.Div(children='Differential Refraction',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='diff-ref-id', value = 2, type='number',step =0.1,min=0,max=5,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),

        ## Dispersion: Object spectra
            # header
        html.Div(children='Dispersion Obj. Spec.',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text'],'margin-left': '15px'}
                ),
            # input tab
        html.Div([
        dcc.Input(id='disp-obj-id', value = 5, type='number',step=1,min=1,max=50,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
        
                 ]),

        ## Dispersion: Atm. Conditions
            # header
        html.Div(children='Dispersion atm. cond.',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='disp-atm-id', value=5, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Dispersion ADC Position
            # header
        html.Div(children='Dispersion ADC pos.',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='disp-adc-id', value=1, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),

        ## Dispaersion Variability
            # header
        html.Div(children='Dispaersion Variability',
            style={'textAlign': 'center', 'font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
            dcc.Input(id='disp-var-id', value=2, type='number',step=0.01,min=0,max=5,
                style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
                
                         ]),
                      
                              html.H5(children='Ref obj. catalog',
            style={ 'backgroundColor': '#FFFFFF','textAlign': 'center','font-weight': 'bold','color':'black'},
               ),
       
        ## Position error
            # header
        html.Div(children='Position error',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text']}
                ),
            # input tab
        html.Div([
        dcc.Input(id='pos-err-id', value = 1000, type='number',step =5,min=0,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
          
                 ]),

        ## Aberration grav. deflection
            # header
        html.Div(children='Aberration grav. defl.',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text'],'margin-left': '15px'}
                ),
            # input tab
        html.Div([
        dcc.Input(id='ab-grav-id', value = 1, type='number',step=1,min=1,max=50,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
        
                 ]),

        ## Other
            # header
        html.Div(children='Other',
            style={'textAlign': 'center','font-weight': 'bold','color': colors['text'],'margin-left': '15px'}
                ),
            # input tab
        html.Div([
        dcc.Input(id='other-id', value = 1, type='number',step=1,min=1,max=50,
        style={'textAlign': 'center','margin-left': '70px','width':'70%'}),
        
                 ]),

            ],style={'backgroundColor': '#111111','opacity': '.8','width': '30%','float': 'right','display': 'inline-block','margin-top': '10px','margin-right': '10px','margin-left': '10px','height': '650px'}),


  
        ]),     
                  
    ###################### PLOTS ##############################
    

    dcc.Tab(label='Plots',style={
            'width': '100%',
            'font-size': '50%',
            'height': '100%',
            'backgroundColor': '#111111','opacity': '.8','font-weight': 'bold','color':'white','fontSize': 14
        }, 
                children=[
                 html.Div([ 
                
                dcc.Graph(
                                id='example-graph',
                                figure={
                                'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'scatter', 'name': 'SNR'},
                            
                                ],
                                'layout': go.Layout(
                                title=go.layout.Title(text="Error vs SNR"),
                                xaxis={'title': 'Astrometric Error'},
                                yaxis={'title': 'SNR'}, 
                                )
                                        
                                        
                                
                                }
                                )        
                           
 ],style={'backgroundColor': '#111111','opacity': '0.95','color':'white','fontSize': 12,'width':'100%','textAlign':'left','margin-right': '15px'}),                                    

        ]),         
 ##########################documentation##################################
    dcc.Tab(label='Documentation',style={
        'width': '100%',
        'font-size': '50%',
        'height': '100%',
        'backgroundColor': '#111111','opacity': '.8','font-weight': 'bold','color':'white','fontSize': 14
    }, 
            children=[
             html.Div([      
         
    
              
dcc.Markdown('''

> #### **Astrometry science cases**


> **Absolute astrometry :** The determination of the science object positions in the sky coordinate system.

> **Differential astrometry- Science Objects relative to each other :** The measurement of the separations of different science objects in the field relative to each other.

> **Differential astrometry- Relative to field stars :** The measurement of the separations of different science objects in the field relative to other field objects.



> #### **Observation field**

> **Science objects :** Objects of scientific interest.

> **Reference objects :** Objects with known sky coordinates.

> **Field objects :** Anything object in the science field for which we measure coordinates.

> **NGS :** Natural Guide Star.

>**R ref sci :** Distance between the science object and the reference object.

>**R delta sci :** Relevant scale of the science object movement. This might be the size of the orbit of
> a star moving around the Galactic center, of a binary star orbit, or the distance over which an object moves in a straight(ish) line over all the epoch of a set of observations.
   

> #### **Global inputs**

> **R_NGS  :** The average separations of the NGSs.

> **R_ref :** The average separations of the reference objects.

> **T :** Integration time.

> **dt epoch :** Time since catalog reference epoch.

> **Mag(vega) :** Star magnitude with respect to Vega

> #### **Engineering Inputs**
For more details on the Engineering and the other Input values, please refer to 1.

> #### **User Tips**
> * *Differential astrometry- Relative to field stars* is implemented according to September 2019 version of the spreadsheet. *Differential astrometry- Science Objects relative to each other* and *Absolute Astrometry* are implemented as per 2014 version of the spreadsheet with calculations as described in [1].

> * The 2014 version calculates variance in x, y coordinates and theta coordinates for one average SNR of the field. The 2019 calculates variances for depending on separate SNR for field stars , reference stars and NGS. In near future all calculations are expected to happen in 2019 format.

> * *Magnitude field*, *Magnitude ref*, *Magnitude NGS*, *number of field stars*, *number of NGS stars* are not used of *Absolute Astrometry* and *Differential astrometry- Science Objects relative to each other*.

> * Number of reference stars cannot be zero for *Differential astrometry- Relative to field stars*.

> * *R delta sci* is not applicable to *Differential astrometry- Science Objects relative to each other*. *R sep* = *R ref sci* in ref. 1 for *Absolute Astrometry*.

> * *R ref sci* is not applicable to *Absolute Astrometry*. *R sep* = *R delta sci* in ref. 1 for *Differential astrometry- Science Objects relative to each other*.

> * The astrometric error budget functions use SNR in ref. 1. For magnitude vs astrometric precision plots we convert magnitude and exposure time to SNR.  The conversion of magnitude to SNR is done using [exposure time calculator](https://www.tmt.org/etc/iris).

> #### **Reference**
> 1. M. Schock, B. Ellerbroek, et al.,"TMT Top Down Astrometry Error Budget", TMT internal report TMT.AOS.TEC.12.039.DRF03, Thirty Meter Telescope, 2014             

'''),  
                       
   

        
 ],style={'backgroundColor': '#111111','opacity': '0.95','color':'white','fontSize': 12,'width':'100%','textAlign':'left','margin-right': '15px'}),                                    

        ]),
        
             ])


),
        

 
    
####################### reference ############################################
#
#    html.Div(children=[
#                    dcc.Markdown('''
#                        References
#                        1. M. Schock, B. Ellerbroek, et al.,"TMT Top Down Astrometry Error Budget", TMT internal report TMT.AOS.TEC.12.039.DRF03, Thirty Meter Telescope, 2014
#                        '''),
#                ],
#                style={'backgroundColor': '#111111','opacity': '.8','color': 'white', 'font-weight': 'bold','textAlign':'left','font-size':'12px','margin-top': '-10px'}),

                                 
#    html.Div(id='page-1-content'),
                         
       

       
       
    
    html.Div(id='butt-state'),
#    html.Br(),
#    dcc.Link('documentation', href='/documentation'),                  

    # 
#        ], style={'background': '#blue'}),

        ], style={'background-image': 'url(https://github.com/chamarthisireesha/TMTAstrometry/blob/master/background.png?raw=true)',}),


   


])


@app.callback(Output('final_output-id', 'children'),
    [Input(component_id='Calculate', component_property='n_clicks')],
    [State(component_id='wavelength-id', component_property='value'),
    State(component_id='SNR-sci-id', component_property='value'),
    State(component_id='SNR-fie-id', component_property='value'),
    State(component_id='SNR-ref-id', component_property='value'),
    State(component_id='RNGS-id', component_property='value'),
    State(component_id='rref-id', component_property='value'),
    State(component_id='T-id', component_property='value'),
    State(component_id='dt-id', component_property='value'),
    State(component_id='Nsci-id', component_property='value'),
    State(component_id='Nfield-id', component_property='value'),
    State(component_id='Nref-id', component_property='value'),
    State(component_id='Nngs-id', component_property='value'),
    State(component_id='rref-sci-id', component_property='value'),
    State(component_id='rdsci-id', component_property='value'),
    State(component_id='Ncal-id', component_property='value'),
    State(component_id='pix-blur-id', component_property='value'),
    State(component_id='pix-irr-id', component_property='value'),
    State(component_id='dect-non-id', component_property='value'),
    State(component_id='PSF-id', component_property='value'),
    State(component_id='confu-id', component_property='value'),
    State(component_id='NGS-perr-id', component_property='value'),
    State(component_id='IRIS-opt-id', component_property='value'),
    State(component_id='IRIS-surf-id', component_property='value'),
    State(component_id='quas-stat-id', component_property='value'),
    State(component_id='tel-opt-id', component_property='value'),
    State(component_id='rot-err-id', component_property='value'),
    State(component_id='act-spike-id', component_property='value'),
    State(component_id='vib-id', component_property='value'),
    State(component_id='coup-atm-id', component_property='value'),
    State(component_id='diff-ref-id', component_property='value'),
    State(component_id='disp-obj-id', component_property='value'),
    State(component_id='disp-atm-id', component_property='value'),
    State(component_id='disp-adc-id', component_property='value'),
    State(component_id='disp-var-id', component_property='value'),
    State(component_id='halo-id', component_property='value'),
    State(component_id='turb-var-id', component_property='value'),
    State(component_id='pos-err-id', component_property='value'),
    State(component_id='ab-grav-id', component_property='value'),
    State(component_id='other-id', component_property='value'),
    State(component_id='astrometry-type-id', component_property='value')
    ]
)

#def page_1_dropdown(value):
#    return 'You have selected "{}"'.format(value)


def update_output_div(n_clicks,wavelength,SNR_sci,SNR_fie,SNR_ref,rNGS,rref,T,dt,Nsci,Nfield,Nref,Nngs,rref_sci,rdsci,Ncal,pix_blur,pix_irr,dect_non,PSF,confusion,NGS_perr,IRIS_opt,IRIS_surf,
                        quasi_stat,tel_opt,rot_err,act_spike,vib,coup_atm,diff_ref,disp_obj,disp_atm,disp_adc,disp_var,halo,turb_var,pos_err,ab_grav,other,astrometry_type):
    # The variables are already imported from input.py. Update the variables the are fed from the UI
    
    if wavelength==0.000000928:
                arr_Zbb=np.loadtxt('Zbb.csv',delimiter=',')
                f = interpolate.interp2d(arr_Zbb[:,0],arr_Zbb[:,1],arr_Zbb[:,2], kind='linear')
    elif wavelength==0.00000109:
                arr_Ybb=np.loadtxt('Ybb.csv',delimiter=',')
                f = interpolate.interp2d(arr_Ybb[:,0],arr_Ybb[:,1],arr_Ybb[:,2], kind='linear')         
    elif wavelength==0.00000127:
                arr_Jbb=np.loadtxt('Jbb.csv',delimiter=',')
                f= interpolate.interp2d(arr_Jbb[:,0],arr_Jbb[:,1],arr_Jbb[:,2], kind='linear')          
    elif wavelength==0.000001629:
                arr_Hbb=np.loadtxt('Hbb.csv',delimiter=',')
                f = interpolate.interp2d(arr_Hbb[:,0],arr_Hbb[:,1],arr_Hbb[:,2], kind='linear')         
    else:
                arr_Kbb=np.loadtxt('Kbb.csv',delimiter=',')
                f= interpolate.interp2d(arr_Kbb[:,0],arr_Kbb[:,1],arr_Kbb[:,2], kind='linear')                                                          

    global_inputs['wavelength'] = wavelength
    global_inputs['SNR_sci'] = f(SNR_sci,T)
    global_inputs['SNR_fie'] = f(SNR_fie,T)
    global_inputs['SNR_ref'] = f(SNR_ref,T)
    global_inputs['rngs'] = rNGS
    global_inputs['rref'] = rref
    global_inputs['T'] = T
    global_inputs['dt_epoch'] = dt
    
    field['Nsci'] = Nsci
    field['Nfield'] = Nfield
    field['Nref'] = Nref
    field['Nngs'] = Nngs
    field['rref-sci'] = rref_sci
    field['rdref'] = rdsci

    sigma_sci['Focal-plane measurement errors']['Noise calibration errors'] = Ncal
    sigma_sci['Focal-plane measurement errors']['Pixel blur'] = pix_blur
    sigma_sci['Focal-plane measurement errors']['Pixel irregularities'] = pix_irr
    sigma_sci['Focal-plane measurement errors']['Detector non-linearity'] = dect_non
    sigma_sci['Focal-plane measurement errors']['PSF reconstruction'] = PSF
    sigma_sci['Focal-plane measurement errors']['Confusion'] = confusion

    sigma_NGS['Opto-mechanical errors']['NGS position errors'] = NGS_perr

    sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS optics'] = IRIS_opt
    sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS surfaces'] = IRIS_surf
    sigma_sci['Opto-mechanical errors']['Quasi_static distortions'] = quasi_stat
    sigma_sci['Opto-mechanical errors']['Telescope optics'] = tel_opt
    sigma_sci['Opto-mechanical errors']['Rotator errors'] = rot_err
    sigma_sci['Opto-mechanical errors']['Actuators diffr spikes'] = act_spike
    sigma_sci['Opto-mechanical errors']['Vibrations'] = vib
    sigma_sci['Opto-mechanical errors']['Coupling atm effects'] = coup_atm

    sigma_sci['Atmospheric refraction errors']['Achromatic differential refraction'] = diff_ref
    sigma_sci['Atmospheric refraction errors']['Dispersion obj spectra'] = disp_obj
    sigma_sci['Atmospheric refraction errors']['Dispersion atm conditions'] = disp_atm
    sigma_sci['Atmospheric refraction errors']['Dispersion ADC position'] = disp_adc
    sigma_sci['Atmospheric refraction errors']['Dispersion variability'] = disp_var

    sigma_sci['Residual turbulence errors']['Halo effect'] = halo
    sigma_sci['Residual turbulence errors']['Turb conditions variability'] = turb_var

    RefObjNCatErr['Position errors'] = pos_err
    RefObjNCatErr['Aberration grav deflection'] = ab_grav
    RefObjNCatErr['Other'] = other

    # send the unpdated inputs to calculate the astrometry error
    Final_error = { 'Focal-plane measurement errors': 0,
                        'Opto-mechanical errors': 0,
                        'Atmospheric refraction errors': 0,
                        'Residual turbulence errors': 0,
                        'Pixel coordinate error': 0,
                        'Total plate scale error': 0,
                        'Astrometry error': 0}
    if int(n_clicks)>=1:
        Final_error = Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,astrometry_type)
    return 'Final astrometry error is {} µas'.format(Final_error['Astrometry error'])


@app.callback(Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='Calculate', component_property='n_clicks')],
    [State(component_id='wavelength-id', component_property='value'),
    State(component_id='SNR-sci-id', component_property='value'),
    State(component_id='SNR-fie-id', component_property='value'),
    State(component_id='SNR-ref-id', component_property='value'),
    State(component_id='RNGS-id', component_property='value'),
    State(component_id='rref-id', component_property='value'),
    State(component_id='T-id', component_property='value'),
    State(component_id='dt-id', component_property='value'),
    State(component_id='Nsci-id', component_property='value'),
    State(component_id='Nfield-id', component_property='value'),
    State(component_id='Nref-id', component_property='value'),
    State(component_id='Nngs-id', component_property='value'),
    State(component_id='rref-sci-id', component_property='value'),
    State(component_id='rdsci-id', component_property='value'),
    State(component_id='Ncal-id', component_property='value'),
    State(component_id='pix-blur-id', component_property='value'),
    State(component_id='pix-irr-id', component_property='value'),
    State(component_id='dect-non-id', component_property='value'),
    State(component_id='PSF-id', component_property='value'),
    State(component_id='confu-id', component_property='value'),
    State(component_id='NGS-perr-id', component_property='value'),
    State(component_id='IRIS-opt-id', component_property='value'),
    State(component_id='IRIS-surf-id', component_property='value'),
    State(component_id='quas-stat-id', component_property='value'),
    State(component_id='tel-opt-id', component_property='value'),
    State(component_id='rot-err-id', component_property='value'),
    State(component_id='act-spike-id', component_property='value'),
    State(component_id='vib-id', component_property='value'),
    State(component_id='coup-atm-id', component_property='value'),
    State(component_id='diff-ref-id', component_property='value'),
    State(component_id='disp-obj-id', component_property='value'),
    State(component_id='disp-atm-id', component_property='value'),
    State(component_id='disp-adc-id', component_property='value'),
    State(component_id='disp-var-id', component_property='value'),
    State(component_id='halo-id', component_property='value'),
    State(component_id='turb-var-id', component_property='value'),
    State(component_id='pos-err-id', component_property='value'),
    State(component_id='ab-grav-id', component_property='value'),
    State(component_id='other-id', component_property='value'),
    State(component_id='astrometry-type-id', component_property='value')
    ]
)

def update_figure(n_clicks,wavelength,SNR_sci,SNR_fie,SNR_ref,rNGS,rref,T,dt,Nsci,Nfield,Nref,Nngs,rref_sci,rdsci,Ncal,pix_blur,pix_irr,dect_non,PSF,confusion,NGS_perr,IRIS_opt,IRIS_surf,
                        quasi_stat,tel_opt,rot_err,act_spike,vib,coup_atm,diff_ref,disp_obj,disp_atm,disp_adc,disp_var,halo,turb_var,pos_err,ab_grav,other,astrometry_type):

    if wavelength==0.000000928:
                arr_Zbb=np.loadtxt('Zbb.csv',delimiter=',')
                f = interpolate.interp2d(arr_Zbb[:,0],arr_Zbb[:,1],arr_Zbb[:,2], kind='cubic')
    elif wavelength==0.00000109:
                arr_Ybb=np.loadtxt('Ybb.csv',delimiter=',')
                f = interpolate.interp2d(arr_Ybb[:,0],arr_Ybb[:,1],arr_Ybb[:,2], kind='cubic')          
    elif wavelength==0.00000127:
                arr_Jbb=np.loadtxt('Jbb.csv',delimiter=',')
                f= interpolate.interp2d(arr_Jbb[:,0],arr_Jbb[:,1],arr_Jbb[:,2], kind='cubic')           
    elif wavelength==0.000001629:
                arr_Hbb=np.loadtxt('Hbb.csv',delimiter=',')
                f = interpolate.interp2d(arr_Hbb[:,0],arr_Hbb[:,1],arr_Hbb[:,2], kind='cubic')          
    else:
                arr_Kbb=np.loadtxt('Kbb.csv',delimiter=',')
                f= interpolate.interp2d(arr_Kbb[:,0],arr_Kbb[:,1],arr_Kbb[:,2], kind='cubic')   

    global_inputs['wavelength'] = wavelength
    global_inputs['SNR_sci'] = f(SNR_sci,T)
    global_inputs['SNR_fie'] = f(SNR_fie,T)
    global_inputs['SNR_ref'] = f(SNR_ref,T)
    global_inputs['rngs'] = rNGS
    global_inputs['rref'] = rref
    global_inputs['T'] = T
    global_inputs['dt_epoch'] = dt
    
    field['Nsci'] = Nsci
    field['Nfield'] = Nfield
    field['Nref'] = Nref
    field['Nngs'] = Nngs
    field['rref-sci'] = rref_sci
    field['rdref'] = rdsci

    sigma_sci['Focal-plane measurement errors']['Noise calibration errors'] = Ncal
    sigma_sci['Focal-plane measurement errors']['Pixel blur'] = pix_blur
    sigma_sci['Focal-plane measurement errors']['Pixel irregularities'] = pix_irr
    sigma_sci['Focal-plane measurement errors']['Detector non-linearity'] = dect_non
    sigma_sci['Focal-plane measurement errors']['PSF reconstruction'] = PSF
    sigma_sci['Focal-plane measurement errors']['Confusion'] = confusion

    sigma_NGS['Opto-mechanical errors']['NGS position errors'] = NGS_perr

    sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS optics'] = IRIS_opt
    sigma_sci['Opto-mechanical errors']['NFIAROS_IRIS surfaces'] = IRIS_surf
    sigma_sci['Opto-mechanical errors']['Quasi_static distortions'] = quasi_stat
    sigma_sci['Opto-mechanical errors']['Telescope optics'] = tel_opt
    sigma_sci['Opto-mechanical errors']['Rotator errors'] = rot_err
    sigma_sci['Opto-mechanical errors']['Actuators diffr spikes'] = act_spike
    sigma_sci['Opto-mechanical errors']['Vibrations'] = vib
    sigma_sci['Opto-mechanical errors']['Coupling atm effects'] = coup_atm

    sigma_sci['Atmospheric refraction errors']['Achromatic differential refraction'] = diff_ref
    sigma_sci['Atmospheric refraction errors']['Dispersion obj spectra'] = disp_obj
    sigma_sci['Atmospheric refraction errors']['Dispersion atm conditions'] = disp_atm
    sigma_sci['Atmospheric refraction errors']['Dispersion ADC position'] = disp_adc
    sigma_sci['Atmospheric refraction errors']['Dispersion variability'] = disp_var

    sigma_sci['Residual turbulence errors']['Halo effect'] = halo
    sigma_sci['Residual turbulence errors']['Turb conditions variability'] = turb_var

    RefObjNCatErr['Position errors'] = pos_err
    RefObjNCatErr['Aberration grav deflection'] = ab_grav
    RefObjNCatErr['Other'] = other
    x_arr=np.arange(SNR_sci-5,SNR_sci+5,1)
    y_arr=[]
    for x in x_arr:
                global_inputs['SNR_sci'] = f(x,T)
                # print x,T,f(x,T)
                err=Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,astrometry_type)
                y_arr.append(err['Astrometry error'][0])
    traces = []
    traces.append(go.Scatter(
                x=x_arr,
                y=y_arr,
                mode='lines+markers',
                opacity=0.7,
                marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                },
                
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            title= go.layout.Title(text="Magnitude v/s Astrometric Error"),
            xaxis={'title': 'Magnitude(Vega)'},
            yaxis={'title': 'Astrometric Error'},
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
