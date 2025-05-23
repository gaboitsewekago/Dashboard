import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import StringIO

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# User database for authentication (hardcoded for simplicity)
USERS = {'admin': 'admin123'}

# Load the dataset
def load_data():
    import os
    from pathlib import Path
    
    try:
        data_path = os.path.join(os.path.dirname(__file__), "data", "data.csv")
        print(f"Attempting to load data from specific path: {specific_path}")
        
        if os.path.exists(specific_path):
            data = pd.read_csv(specific_path)
            print(f"Data loaded successfully from specific path with {len(data)} records")
            
            date_columns = ['signup_date', 'posting_date', 'request_date', 'query_date']
            for col in date_columns:
                if col in data.columns:
                    data[col] = pd.to_datetime(data[col], errors='coerce')
            
            return data
        else:
            print(f"File not found at specific path: {specific_path}")
    except Exception as e:
        print(f"Error loading data from specific path: {e}")
    
    try:
        documents_path = os.path.join(Path.home(), "Documents")
        dash_apps_path = os.path.join(documents_path, "Dash_apps")
        data_path = os.path.join(dash_apps_path, "data.csv")
        
        print(f"Attempting to load data from: {data_path}")
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            print(f"Data loaded successfully from Documents/Dash_apps with {len(data)} records")
            
            date_columns = ['signup_date', 'posting_date', 'request_date', 'query_date']
            for col in date_columns:
                if col in data.columns:
                    data[col] = pd.to_datetime(data[col], errors='coerce')
            
            return data
    except Exception as e:
        print(f"Error loading data from Documents/Dash_apps: {e}")
    
    try:
        data_url = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/data-wQWq5huWVt0YY39XjCV5PfjOTPz1Gs.csv"
        print(f"Attempting to load data from URL: {data_url}")
        
        response = requests.get(data_url)
        response.raise_for_status()
        
        data_string = StringIO(response.text)
        data = pd.read_csv(data_string)
        
        date_columns = ['signup_date', 'posting_date', 'request_date', 'query_date']
        for col in date_columns:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col], errors='coerce')
        
        print(f"Data loaded successfully from URL with {len(data)} records")
        return data
    
    except Exception as e:
        print(f"Error loading data from URL: {e}")
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            local_path = os.path.join(script_dir, 'ai_solutions_data-copy.csv')
            print(f"Attempting to load local data from {local_path}")
            data = pd.read_csv(local_path)
            print(f"Data loaded successfully from fallback path with {len(data)} records")
            return data
        except Exception as e:
            print(f"Failed to load local data: {e}")
            print("Returning empty DataFrame.")
            return pd.DataFrame()

# Load the data
df = load_data()

# Print data info for debugging
print("Data loaded successfully. Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Sample data:")
print(df.head())

# Define the app layout with styled login screen and dashboard
app.layout = html.Div([
    dcc.Store(id='session', data=False, storage_type='session'),
    
    # Styled login screen
    html.Div(id='login-screen', children=[
        html.Div([
            html.H2("AI-Solutions Dashboard Login", 
                    style={
                        'textAlign': 'center', 
                        'color': '#1E3A8A', 
                        'marginBottom': '20px',
                        'fontSize': '28px',
                        'fontWeight': 'bold',
                        'fontFamily': 'Arial, sans-serif'
                    }),
            html.Div([
                html.Label("Username:", 
                          style={
                              'display': 'block', 
                              'marginBottom': '8px', 
                              'color': '#374151',
                              'fontSize': '16px',
                              'fontWeight': '500'
                          }),
                dcc.Input(
                    id='username', 
                    type='text', 
                    placeholder='Enter username',
                    style={
                        'width': '100%', 
                        'padding': '12px', 
                        'border': '2px solid #E5E7EB', 
                        'borderRadius': '8px',
                        'fontSize': '16px',
                        'transition': 'all 0.3s ease',
                        'backgroundColor': '#F9FAFB',
                        ':focus': {
                            'borderColor': '#14B8A6',
                            'boxShadow': '0 0 0 3px rgba(20, 184, 166, 0.2)',
                            'outline': 'none'
                        }
                    }
                )
            ], style={'marginBottom': '20px'}),
            html.Div([
                html.Label("Password:", 
                          style={
                              'display': 'block', 
                              'marginBottom': '8px', 
                              'color': '#374151',
                              'fontSize': '16px',
                              'fontWeight': '500'
                          }),
                dcc.Input(
                    id='password', 
                    type='password', 
                    placeholder='Enter password',
                    style={
                        'width': '100%', 
                        'padding': '12px', 
                        'border': '2px solid #E5E7EB', 
                        'borderRadius': '8px',
                        'fontSize': '16px',
                        'transition': 'all 0.3s ease',
                        'backgroundColor': '#F9FAFB',
                        ':focus': {
                            'borderColor': '#14B8A6',
                            'boxShadow': '0 0 0 3px rgba(20, 184, 166, 0.2)',
                            'outline': 'none'
                        }
                    }
                )
            ], style={'marginBottom': '25px'}),
            html.Button(
                'Login', 
                id='login-button', 
                n_clicks=0, 
                style={
                    'width': '100%', 
                    'backgroundColor': '#14B8A6', 
                    'color': '#F9FAFB', 
                    'padding': '14px', 
                    'border': 'none',
                    'borderRadius': '8px', 
                    'fontSize': '18px', 
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease',
                    'textTransform': 'uppercase',
                    ':hover': {
                        'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
                        'transform': 'scale(1.05)'
                    }
                }
            ),
            html.Div(
                id='login-message', 
                style={
                    'color': '#F87171', 
                    'marginTop': '15px', 
                    'textAlign': 'center', 
                    'minHeight': '20px',
                    'fontSize': '14px',
                    'opacity': '0',
                    'transition': 'opacity 0.3s ease'
                }
            )
        ], style={
            'backgroundColor': '#F9FAFB',
            'padding': '40px',
            'borderRadius': '12px',
            'boxShadow': '0 8px 16px rgba(0,0,0,0.1)',
            'width': '90%',
            'maxWidth': '450px',
            'margin': '150px auto 0 auto',
            'borderLeft': '4px solid #14B8A6'
        })
    ], style={
        'display': 'block', 
        'minHeight': '100vh', 
        'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
        'padding': '20px'
    }),
    
    # Dashboard (initially hidden)
    html.Div(id='dashboard', children=[
        html.Button(
            'Logout', 
            id='logout-button', 
            n_clicks=0, 
            style={
                'position': 'absolute', 
                'top': '15px', 
                'right': '15px', 
                'backgroundColor': '#F87171', 
                'color': '#F9FAFB', 
                'padding': '8px 16px',
                'border': 'none',
                'borderRadius': '6px',
                'fontSize': '16px',
                'fontWeight': '500',
                'cursor': 'pointer',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'backgroundColor': '#DC2626',
                    'transform': 'scale(1.05)'
                }
            }
        ),
        
        # Dashboard header
        html.H1("AI-Solutions Marketing Analytics Dashboard", 
                style={
                    'textAlign': 'center', 
                    'color': '#1E3A8A', 
                    'marginTop': '40px', 
                    'marginBottom': '20px',
                    'fontSize': '36px',
                    'fontWeight': '700',
                    'fontFamily': 'Arial, sans-serif',
                    'position': 'relative',
                    ':after': {
                        'content': '""',
                        'position': 'absolute',
                        'bottom': '-10px',
                        'left': '50%',
                        'transform': 'translateX(-50%)',
                        'width': '100px',
                        'height': '4px',
                        'backgroundColor': '#14B8A6',
                        'borderRadius': '2px'
                    }
                }),
        
        html.Div([
            html.H4("Dataset will be saved to:", 
                    style={
                        'textAlign': 'center', 
                        'marginBottom': '10px',
                        'color': '#374151',
                        'fontSize': '18px',
                        'fontWeight': '600'
                    }),
            html.Div(
                html.P("C:\\Users\\kagog\\Documents\\Dash_apps\\sample_dash_apps\\.sample_virtual_env\\exported_data.csv",
                      style={
                          'textAlign': 'center', 
                          'backgroundColor': '#F9FAFB', 
                          'padding': '15px', 
                          'borderRadius': '8px',
                          'color': '#374151',
                          'fontSize': '14px',
                          'border': '2px solid #14B8A6'
                      }),
                style={
                    'width': '80%', 
                    'maxWidth': '600px', 
                    'margin': '0 auto',
                    'boxShadow': '0 4px 8px rgba(0,0,0,0.05)'
                }
            ),
            html.Div([
                html.Button(
                    "Export Dataset", 
                    id="export-button", 
                    style={
                        'backgroundColor': '#A3E635', 
                        'color': '#1E3A8A', 
                        'border': 'none', 
                        'padding': '12px 24px', 
                        'borderRadius': '8px', 
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease',
                        ':hover': {
                            'backgroundColor': '#84CC16',
                            'transform': 'scale(1.05)',
                            'boxShadow': '0 4px 8px rgba(0,0,0,0.2)'
                        }
                    }
                )
            ], style={'textAlign': 'center', 'margin': '30px 0'})
        ]),
        
        dcc.Tabs(id="tabs", value='dataset-overview', children=[
            dcc.Tab(
                label="Dataset Overview", 
                value='dataset-overview',
                style={
                    'padding': '12px 20px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': '#374151',
                    'backgroundColor': '#E5E7EB',
                    'border': 'none',
                    'borderRadius': '8px 8px 0 0',
                    'marginRight': '5px',
                    'transition': 'all 0.3s ease',
                    ':hover': {
                        'backgroundColor': '#D1D5DB',
                        'color': '#1E3A8A'
                    }
                },
                selected_style={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'borderRadius': '8px 8px 0 0',
                    ':hover': {
                        'backgroundColor': '#0D9488'
                    }
                }
            ),
            dcc.Tab(
                label="User Distribution", 
                value='user-distribution',
                style={
                    'padding': '12px 20px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': '#374151',
                    'backgroundColor': '#E5E7EB',
                    'border': 'none',
                    'borderRadius': '8px 8px 0 0',
                    'marginRight': '5px',
                    'transition': 'all 0.3s ease',
                    ':hover': {
                        'backgroundColor': '#D1D5DB',
                        'color': '#1E3A8A'
                    }
                },
                selected_style={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'borderRadius': '8px 8px 0 0',
                    ':hover': {
                        'backgroundColor': '#0D9488'
                    }
                }
            ),
            dcc.Tab(
                label="Job Posting Analysis", 
                value='job-posting',
                style={
                    'padding': '12px 20px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': '#374151',
                    'backgroundColor': '#E5E7EB',
                    'border': 'none',
                    'borderRadius': '8px 8px 0 0',
                    'marginRight': '5px',
                    'transition': 'all 0.3s ease',
                    ':hover': {
                        'backgroundColor': '#D1D5DB',
                        'color': '#1E3A8A'
                    }
                },
                selected_style={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'borderRadius': '8px 8px 0 0',
                    ':hover': {
                        'backgroundColor': '#0D9488'
                    }
                }
            ),
            dcc.Tab(
                label="Job Types Analysis", 
                value='job-types',
                style={
                    'padding': '12px 20px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': '#374151',
                    'backgroundColor': '#E5E7EB',
                    'border': 'none',
                    'borderRadius': '8px 8px 0 0',
                    'marginRight': '5px',
                    'transition': 'all 0.3s ease',
                    ':hover': {
                        'backgroundColor': '#D1D5DB',
                        'color': '#1E3A8A'
                    }
                },
                selected_style={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'borderRadius': '8px 8px 0 0',
                    ':hover': {
                        'backgroundColor': '#0D9488'
                    }
                }
            ),
            dcc.Tab(
                label="Demo Requests", 
                value='demo-requests',
                style={
                    'padding': '12px 20px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': '#374151',
                    'backgroundColor': '#E5E7EB',
                    'border': 'none',
                    'borderRadius': '8px 8px 0 0',
                    'marginRight': '5px',
                    'transition': 'all 0.3s ease',
                    ':hover': {
                        'backgroundColor': '#D1D5DB',
                        'color': '#1E3A8A'
                    }
                },
                selected_style={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'borderRadius': '8px 8px 0 0',
                    ':hover': {
                        'backgroundColor': '#0D9488'
                    }
                }
            ),
            dcc.Tab(
                label="Promotional Events", 
                value='promotional-events',
                style={
                    'padding': '12px 20px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': '#374151',
                    'backgroundColor': '#E5E7EB',
                    'border': 'none',
                    'borderRadius': '8px 8px 0 0',
                    'marginRight': '5px',
                    'transition': 'all 0.3s ease',
                    ':hover': {
                        'backgroundColor': '#D1D5DB',
                        'color': '#1E3A8A'
                    }
                },
                selected_style={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'borderRadius': '8px 8px 0 0',
                    ':hover': {
                        'backgroundColor': '#0D9488'
                    }
                }
            ),
            dcc.Tab(
                label="Virtual Assistant Queries", 
                value='virtual-assistant',
                style={
                    'padding': '12px 20px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': '#374151',
                    'backgroundColor': '#E5E7EB',
                    'border': 'none',
                    'borderRadius': '8px 8px 0 0',
                    'marginRight': '5px',
                    'transition': 'all 0.3s ease',
                    ':hover': {
                        'backgroundColor': '#D1D5DB',
                        'color': '#1E3A8A'
                    }
                },
                selected_style={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'borderRadius': '8px 8px 0 0',
                    ':hover': {
                        'backgroundColor': '#0D9488'
                    }
                }
            )
        ], style={
            'marginTop': '30px', 
            'backgroundColor': '#F9FAFB', 
            'padding': '10px',
            'borderRadius': '8px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.05)'
        }),
        
        html.Div(id='tab-content', style={'padding': '20px', 'backgroundColor': '#F9FAFB'})
    ], style={'display': 'none', 'minHeight': '100vh', 'backgroundColor': '#F9FAFB'})
])

# Callback to show/hide login screen based on session
@app.callback(
    Output('login-screen', 'style'),
    [Input('session', 'data')]
)
def show_login(session):
    return {
        'display': 'none'
    } if session else {
        'display': 'block', 
        'minHeight': '100vh', 
        'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
        'padding': '20px'
    }

# Callback to show/hide dashboard based on session
@app.callback(
    Output('dashboard', 'style'),
    [Input('session', 'data')]
)
def show_dashboard(session):
    return {
        'display': 'block', 
        'minHeight': '100vh', 
        'backgroundColor': '#F9FAFB'
    } if session else {
        'display': 'none'
    }

# Combined callback for login and logout
@app.callback(
    [Output('session', 'data'), Output('login-message', 'children'), Output('login-message', 'style')],
    [Input('login-button', 'n_clicks'), Input('logout-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def handle_auth(login_clicks, logout_clicks, username, password):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    error_style = {
        'color': '#F87171', 
        'marginTop': '15px', 
        'textAlign': 'center', 
        'minHeight': '20px',
        'fontSize': '14px',
        'opacity': '1',
        'transition': 'opacity 0.3s ease'
    }
    
    if triggered_id == 'login-button' and login_clicks:
        if username in USERS and USERS[username] == password:
            return True, None, error_style
        else:
            return False, 'Invalid credentials', error_style
    elif triggered_id == 'logout-button' and logout_clicks:
        return False, None, error_style
    
    return dash.no_update, dash.no_update, dash.no_update

# Existing callbacks for dashboard functionality
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'dataset-overview':
        return render_dataset_overview()
    elif tab == 'user-distribution':
        return render_user_distribution()
    elif tab == 'job-posting':
        return render_job_posting()
    elif tab == 'job-types':
        return render_job_types()
    elif tab == 'demo-requests':
        return render_demo_requests()
    elif tab == 'promotional-events':
        return render_promotional_events()
    elif tab == 'virtual-assistant':
        return render_virtual_assistant()
    return html.Div(
        "This tab is under construction",
        style={
            'textAlign': 'center',
            'color': '#374151',
            'fontSize': '18px',
            'padding': '20px'
        }
    )

def render_dataset_overview():
    return html.Div([
        html.H2(
            "Dataset Overview", 
            style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'color': '#1E3A8A',
                'fontSize': '28px',
                'fontWeight': '600',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        html.Div([
            html.Div([
                html.H4(
                    "Dataset Summary",
                    style={
                        'color': '#374151',
                        'fontSize': '20px',
                        'fontWeight': '500',
                        'marginBottom': '10px'
                    }
                ),
                html.P(
                    f"Total Records: {len(df)}",
                    style={'color': '#374151', 'fontSize': '16px'}
                ),
                html.P(
                    f"Number of Columns: {len(df.columns)}",
                    style={'color': '#374151', 'fontSize': '16px'}
                ),
                html.P(
                    f"Time Range: {df['query_date'].min()} to {df['query_date'].max()}" 
                    if 'query_date' in df.columns else "Time Range: Not Available",
                    style={'color': '#374151', 'fontSize': '16px'}
                ),
            ], style={
                'marginBottom': '30px', 
                'backgroundColor': '#FFFFFF', 
                'padding': '20px', 
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.05)'
            }),
            html.H4(
                "Complete Dataset", 
                style={
                    'marginTop': '20px',
                    'color': '#1E3A8A',
                    'fontSize': '20px',
                    'fontWeight': '500'
                }
            ),
            dash_table.DataTable(
                id='dataset-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=15,
                style_table={
                    'overflowX': 'auto',
                    'borderRadius': '8px',
                    'backgroundColor': '#FFFFFF'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'minWidth': '100px', 
                    'width': '150px', 
                    'maxWidth': '200px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'color': '#374151',
                    'fontSize': '14px'
                },
                style_header={
                    'backgroundColor': '#14B8A6',
                    'color': '#F9FAFB',
                    'fontWeight': '600',
                    'fontSize': '14px',
                    'textAlign': 'left',
                    'padding': '10px'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#F9FAFB'
                    },
                    {
                        'if': {'state': 'selected'},
                        'backgroundColor': 'rgba(20, 184, 166, 0.2)',
                        'border': '1px solid #14B8A6'
                    }
                ],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
            )
        ])
    ])

def render_user_distribution():
    return html.Div([
        html.H2(
            "User Distribution Analysis", 
            style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'color': '#1E3A8A',
                'fontSize': '28px',
                'fontWeight': '600'
            }
        ),
        html.P(
            "Click on a continent to see country-level distribution", 
            style={
                'textAlign': 'center', 
                'fontStyle': 'italic',
                'color': '#374151',
                'fontSize': '16px',
                'marginBottom': '20px'
            }
        ),
        dcc.Store(id='selected-continent', data=None),
        html.Button(
            'Back to Continents',
            id='user-back-button',
            n_clicks=0,
            style={
                'display': 'none',
                'backgroundColor': '#14B8A6',
                'color': '#F9FAFB',
                'padding': '10px 20px',
                'border': 'none',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '500',
                'marginBottom': '15px',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
                    'transform': 'scale(1.05)'
                }
            }
        ),
        dcc.Graph(id='continent-distribution')
    ])

@app.callback(
    [Output('continent-distribution', 'figure'),
     Output('user-back-button', 'style'),
     Output('selected-continent', 'data')],
    [Input('continent-distribution', 'clickData'),
     Input('user-back-button', 'n_clicks')],
    [State('selected-continent', 'data')]
)
def update_user_distribution(clickData, back_clicks, selected_continent):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    continent_data = df[df['data_type'] == 'assistant data'].groupby('continent').size().reset_index(name='count')
    primary_fig = px.bar(
        continent_data, 
        x='continent', 
        y='count',
        title='User Distribution by Continent',
        labels={'count': 'Number of Users', 'continent': 'Continent'},
        color='continent',
        color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A', '#FBBF24', '#8B5CF6'],
        template='plotly_white'
    ).update_layout(
        title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
        xaxis_title={'font': {'size': 14, 'color': '#374151'}},
        yaxis_title={'font': {'size': 14, 'color': '#374151'}},
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font={'family': 'Arial, sans-serif'}
    )
    button_style = {
        'display': 'none',
        'backgroundColor': '#14B8A6',
        'color': '#F9FAFB',
        'padding': '10px 20px',
        'border': 'none',
        'borderRadius': '6px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '500',
        'marginBottom': '15px',
        'transition': 'all 0.3s ease'
    }
    
    if triggered_id == 'continent-distribution' and clickData:
        continent = clickData['points'][0]['x']
        filtered_df = df[(df['data_type'] == 'assistant data') & (df['continent'] == continent)]
        country_data = filtered_df.groupby('country').size().reset_index(name='count')
        drilldown_fig = px.bar(
            country_data, 
            x='country', 
            y='count',
            title=f'User Distribution by Country in {continent}',
            labels={'count': 'Number of Users', 'country': 'Country'},
            color='country',
            color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A', '#FBBF24', '#8B5CF6'],
            template='plotly_white'
        ).update_layout(
            title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
            xaxis_title={'font': {'size': 14, 'color': '#374151'}},
            yaxis_title={'font': {'size': 14, 'color': '#374151'}},
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font={'family': 'Arial, sans-serif'}
        )
        button_style['display'] = 'block'
        return drilldown_fig, button_style, continent
    
    elif triggered_id == 'user-back-button' and back_clicks:
        return primary_fig, {
            'display': 'none',
            'backgroundColor': '#14B8A6',
            'color': '#F9FAFB',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '6px',
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '500',
            'marginBottom': '15px',
            'transition': 'all 0.3s ease'
        }, None
    
    return primary_fig, button_style, selected_continent

def render_job_posting():
    return html.Div([
        html.H2(
            "Job Posting Analysis", 
            style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'color': '#1E3A8A',
                'fontSize': '28px',
                'fontWeight': '600'
            }
        ),
        html.P(
            "Click on a day to see time period distribution", 
            style={
                'textAlign': 'center', 
                'fontStyle': 'italic',
                'color': '#374151',
                'fontSize': '16px',
                'marginBottom': '20px'
            }
        ),
        dcc.Store(id='selected-day', data=None),
        html.Button(
            'Back to Days',
            id='job-back-button',
            n_clicks=0,
            style={
                'display': 'none',
                'backgroundColor': '#14B8A6',
                'color': '#F9FAFB',
                'padding': '10px 20px',
                'border': 'none',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '500',
                'marginBottom': '15px',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
                    'transform': 'scale(1.05)'
                }
            }
        ),
        dcc.Graph(id='day-distribution')
    ])

@app.callback(
    [Output('day-distribution', 'figure'),
     Output('job-back-button', 'style'),
     Output('selected-day', 'data')],
    [Input('day-distribution', 'clickData'),
     Input('job-back-button', 'n_clicks')],
    [State('selected-day', 'data')]
)
def update_job_posting(clickData, back_clicks, selected_day):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    job_data = df[df['data_type'].str.contains('job', case=False, na=False)]
    day_data = job_data.groupby('day').size().reset_index(name='count')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_data['day'] = pd.Categorical(day_data['day'], categories=day_order, ordered=True)
    day_data = day_data.sort_values('day')
    primary_fig = px.bar(
        day_data, 
        x='day', 
        y='count',
        title='Job Posting Distribution by Day of Week',
        labels={'count': 'Number of Job Postings', 'day': 'Day of Week'},
        color='day',
        color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A', '#FBBF24', '#8B5CF6', '#EC4899'],
        template='plotly_white'
    ).update_layout(
        title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
        xaxis_title={'font': {'size': 14, 'color': '#374151'}},
        yaxis_title={'font': {'size': 14, 'color': '#374151'}},
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font={'family': 'Arial, sans-serif'}
    )
    button_style = {
        'display': 'none',
        'backgroundColor': '#14B8A6',
        'color': '#F9FAFB',
        'padding': '10px 20px',
        'border': 'none',
        'borderRadius': '6px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '500',
        'marginBottom': '15px',
        'transition': 'all 0.3s ease'
    }
    
    if triggered_id == 'day-distribution' and clickData:
        day = clickData['points'][0]['x']
        filtered_df = df[(df['data_type'].str.contains('job', case=False, na=False)) & (df['day'] == day)]
        time_data = filtered_df.groupby('time_period').size().reset_index(name='count')
        drilldown_fig = px.bar(
            time_data, 
            x='time_period', 
            y='count',
            title=f'Job Posting Distribution by Time Period on {day}',
            labels={'count': 'Number of Job Postings', 'time_period': 'Time Period'},
            color='time_period',
            color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A'],
            template='plotly_white'
        ).update_layout(
            title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
            xaxis_title={'font': {'size': 14, 'color': '#374151'}},
            yaxis_title={'font': {'size': 14, 'color': '#374151'}},
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font={'family': 'Arial, sans-serif'}
        )
        button_style['display'] = 'block'
        return drilldown_fig, button_style, day
    
    elif triggered_id == 'job-back-button' and back_clicks:
        return primary_fig, {
            'display': 'none',
            'backgroundColor': '#14B8A6',
            'color': '#F9FAFB',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '6px',
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '500',
            'marginBottom': '15px',
            'transition': 'all 0.3s ease'
        }, None
    
    return primary_fig, button_style, selected_day

def render_job_types():
    return html.Div([
        html.H2(
            "Job Types Analysis", 
            style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'color': '#1E3A8A',
                'fontSize': '28px',
                'fontWeight': '600'
            }
        ),
        html.P(
            "Click on a continent to see regional job type distribution", 
            style={
                'textAlign': 'center', 
                'fontStyle': 'italic',
                'color': '#374151',
                'fontSize': '16px',
                'marginBottom': '20px'
            }
        ),
        dcc.Store(id='selected-job-continent', data=None),
        html.Button(
            'Back to Continents',
            id='job-type-back-button',
            n_clicks=0,
            style={
                'display': 'none',
                'backgroundColor': '#14B8A6',
                'color': '#F9FAFB',
                'padding': '10px 20px',
                'border': 'none',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '500',
                'marginBottom': '15px',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
                    'transform': 'scale(1.05)'
                }
            }
        ),
        dcc.Graph(id='job-type-continent')
    ])

@app.callback(
    [Output('job-type-continent', 'figure'),
     Output('job-type-back-button', 'style'),
     Output('selected-job-continent', 'data')],
    [Input('job-type-continent', 'clickData'),
     Input('job-type-back-button', 'n_clicks')],
    [State('selected-job-continent', 'data')]
)
def update_job_types(clickData, back_clicks, selected_continent):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    job_continent_data = df[df['data_type'].str.contains('job', case=False, na=False)].groupby(['continent', 'job_type']).size().reset_index(name='count')
    pivot_data = job_continent_data.pivot_table(index='continent', columns='job_type', values='count', fill_value=0).reset_index()
    melted_data = pd.melt(pivot_data, id_vars=['continent'], var_name='job_type', value_name='count')
    primary_fig = px.bar(
        melted_data, 
        x='continent', 
        y='count', 
        color='job_type',
        title='Job Types Distribution by Continent',
        labels={'count': 'Number of Jobs Types', 'continent': 'Continent', 'job_type': 'Job Type'},
        barmode='group',
        color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A'],
        template='plotly_white'
    ).update_layout(
        title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
        xaxis_title={'font': {'size': 14, 'color': '#374151'}},
        yaxis_title={'font': {'size': 14, 'color': '#374151'}},
        legend_title={'font': {'size': 12, 'color': '#374151'}},
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font={'family': 'Arial, sans-serif'}
    )
    button_style = {
        'display': 'none',
        'backgroundColor': '#14B8A6',
        'color': '#F9FAFB',
        'padding': '10px 20px',
        'border': 'none',
        'borderRadius': '6px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '500',
        'marginBottom': '15px',
        'transition': 'all 0.3s ease'
    }
    
    if triggered_id == 'job-type-continent' and clickData:
        continent = clickData['points'][0]['x']
        filtered_df = df[(df['data_type'].str.contains('job', case=False, na=False)) & (df['continent'] == continent)]
        country_job_data = filtered_df.groupby(['country', 'job_type']).size().reset_index(name='count')
        drilldown_fig = px.bar(
            country_job_data, 
            x='country', 
            y='count', 
            color='job_type',
            title=f'Job Types Distribution by Country in {continent}',
            labels={'count': 'Number of Jobs', 'country': 'Country', 'job_type': 'Job Type'},
            barmode='group',
            color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A'],
            template='plotly_white'
        ).update_layout(
            title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
            xaxis_title={'font': {'size': 14, 'color': '#374151'}},
            yaxis_title={'font': {'size': 14, 'color': '#374151'}},
            legend_title={'font': {'size': 12, 'color': '#374151'}},
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font={'family': 'Arial, sans-serif'}
        )
        button_style['display'] = 'block'
        return drilldown_fig, button_style, continent
    
    elif triggered_id == 'job-type-back-button' and back_clicks:
        return primary_fig, {
            'display': 'none',
            'backgroundColor': '#14B8A6',
            'color': '#F9FAFB',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '6px',
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '500',
            'marginBottom': '15px',
            'transition': 'all 0.3s ease'
        }, None
    
    return primary_fig, button_style, selected_continent

def render_demo_requests():
    return html.Div([
        html.H2(
            "Demo Requests Analysis", 
            style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'color': '#1E3A8A',
                'fontSize': '28px',
                'fontWeight': '600'
            }
        ),
        html.P(
            "Click on a continent to see country-level demo request distribution", 
            style={
                'textAlign': 'center', 
                'fontStyle': 'italic',
                'color': '#374151',
                'fontSize': '16px',
                'marginBottom': '20px'
            }
        ),
        dcc.Store(id='selected-demo-continent', data=None),
        html.Button(
            'Back to Continents',
            id='demo-back-button',
            n_clicks=0,
            style={
                'display': 'none',
                'backgroundColor': '#14B8A6',
                'color': '#F9FAFB',
                'padding': '10px 20px',
                'border': 'none',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '500',
                'marginBottom': '15px',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
                    'transform': 'scale(1.05)'
                }
            }
        ),
        dcc.Graph(id='demo-continent')
    ])

@app.callback(
    [Output('demo-continent', 'figure'),
     Output('demo-back-button', 'style'),
     Output('selected-demo-continent', 'data')],
    [Input('demo-continent', 'clickData'),
     Input('demo-back-button', 'n_clicks')],
    [State('selected-demo-continent', 'data')]
)
def update_demo_requests(clickData, back_clicks, selected_continent):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    demo_continent_data = df[df['demo_type'].notna()].groupby('continent').size().reset_index(name='count')
    primary_fig = px.bar(
        demo_continent_data, 
        x='continent', 
        y='count',
        title='Demo Requests Distribution by Continent',
        labels={'count': 'Number of Demo Requests', 'continent': 'Continent'},
        color='continent',
        color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A', '#FBBF24', '#8B5CF6'],
        template='plotly_white'
    ).update_layout(
        title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
        xaxis_title={'font': {'size': 14, 'color': '#374151'}},
        yaxis_title={'font': {'size': 14, 'color': '#374151'}},
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font={'family': 'Arial, sans-serif'}
    )
    button_style = {
        'display': 'none',
        'backgroundColor': '#14B8A6',
        'color': '#F9FAFB',
        'padding': '10px 20px',
        'border': 'none',
        'borderRadius': '6px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '500',
        'marginBottom': '15px',
        'transition': 'all 0.3s ease'
    }
    
    if triggered_id == 'demo-continent' and clickData:
        continent = clickData['points'][0]['x']
        filtered_df = df[(df['demo_type'].notna()) & (df['continent'] == continent)]
        country_data = filtered_df.groupby(['country', 'demo_type']).size().reset_index(name='count')
        drilldown_fig = px.bar(
            country_data, 
            x='country', 
            y='count', 
            color='demo_type',
            title=f'Demo Requests by Country in {continent}',
            labels={'count': 'Number of Demo Requests', 'country': 'Country', 'demo_type': 'Demo Type'},
            barmode='group',
            color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A'],
            template='plotly_white'
        ).update_layout(
            title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
            xaxis_title={'font': {'size': 14, 'color': '#374151'}},
            yaxis_title={'font': {'size': 14, 'color': '#374151'}},
            legend_title={'font': {'size': 12, 'color': '#374151'}},
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font={'family': 'Arial, sans-serif'}
        )
        button_style['display'] = 'block'
        return drilldown_fig, button_style, continent
    
    elif triggered_id == 'demo-back-button' and back_clicks:
        return primary_fig, {
            'display': 'none',
            'backgroundColor': '#14B8A6',
            'color': '#F9FAFB',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '6px',
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '500',
            'marginBottom': '15px',
            'transition': 'all 0.3s ease'
        }, None
    
    return primary_fig, button_style, selected_continent

def render_promotional_events():
    return html.Div([
        html.H2(
            "Promotional Events Analysis", 
            style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'color': '#1E3A8A',
                'fontSize': '28px',
                'fontWeight': '600'
            }
        ),
        html.P(
            "Click on a day to see time period distribution", 
            style={
                'textAlign': 'center', 
                'fontStyle': 'italic',
                'color': '#374151',
                'fontSize': '16px',
                'marginBottom': '20px'
            }
        ),
        dcc.Store(id='selected-promo-day', data=None),
        html.Button(
            'Back to Days',
            id='promo-back-button',
            n_clicks=0,
            style={
                'display': 'none',
                'backgroundColor': '#14B8A6',
                'color': '#F9FAFB',
                'padding': '10px 20px',
                'border': 'none',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '500',
                'marginBottom': '15px',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
                    'transform': 'scale(1.05)'
                }
            }
        ),
        dcc.Graph(id='promo-day')
    ])

@app.callback(
    [Output('promo-day', 'figure'),
     Output('promo-back-button', 'style'),
     Output('selected-promo-day', 'data')],
    [Input('promo-day', 'clickData'),
     Input('promo-back-button', 'n_clicks')],
    [State('selected-promo-day', 'data')]
)
def update_promotional_events(clickData, back_clicks, selected_day):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    promo_day_data = df[df['event_type'] == 'promotional event data'].groupby('day').size().reset_index(name='count')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    promo_day_data['day'] = pd.Categorical(promo_day_data['day'], categories=day_order, ordered=True)
    promo_day_data = promo_day_data.sort_values('day')
    primary_fig = px.bar(
        promo_day_data, 
        x='day', 
        y='count',
        title='Promotional Event Requests by Day of Week',
        labels={'count': 'Number of Promotional events Requests', 'day': 'Day of Week'},
        color='day',
        color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A', '#FBBF24', '#8B5CF6', '#EC4899'],
        template='plotly_white'
    ).update_layout(
        title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
        xaxis_title={'font': {'size': 14, 'color': '#374151'}},
        yaxis_title={'font': {'size': 14, 'color': '#374151'}},
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font={'family': 'Arial, sans-serif'}
    )
    button_style = {
        'display': 'none',
        'backgroundColor': '#14B8A6',
        'color': '#F9FAFB',
        'padding': '10px 20px',
        'border': 'none',
        'borderRadius': '6px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '500',
        'marginBottom': '15px',
        'transition': 'all 0.3s ease'
    }
    
    if triggered_id == 'promo-day' and clickData:
        day = clickData['points'][0]['x']
        filtered_df = df[(df['event_type'] == 'promotional event data') & (df['day'] == day)]
        time_data = filtered_df.groupby('time_period').size().reset_index(name='count')
        drilldown_fig = px.bar(
            time_data, 
            x='time_period', 
            y='count',
            title=f'Promotional Event Requests by Time Period on {day}',
            labels={'count': 'Number of Requests', 'time_period': 'Time Period'},
            color='time_period',
            color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A'],
            template='plotly_white'
        ).update_layout(
            title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
            xaxis_title={'font': {'size': 14, 'color': '#374151'}},
            yaxis_title={'font': {'size': 14, 'color': '#374151'}},
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font={'family': 'Arial, sans-serif'}
        )
        button_style['display'] = 'block'
        return drilldown_fig, button_style, day
    
    elif triggered_id == 'promo-back-button' and back_clicks:
        return primary_fig, {
            'display': 'none',
            'backgroundColor': '#14B8A6',
            'color': '#F9FAFB',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '6px',
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '500',
            'marginBottom': '15px',
            'transition': 'all 0.3s ease'
        }, None
    
    return primary_fig, button_style, selected_day

def render_virtual_assistant():
    return html.Div([
        html.H2(
            "Virtual Assistant Queries Analysis", 
            style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'color': '#1E3A8A',
                'fontSize': '28px',
                'fontWeight': '600'
            }
        ),
        html.P(
            "Click on a continent to see country-level virtual assistant request distribution", 
            style={
                'textAlign': 'center', 
                'fontStyle': 'italic',
                'color': '#374151',
                'fontSize': '16px',
                'marginBottom': '20px'
            }
        ),
        dcc.Store(id='selected-va-continent', data=None),
        html.Button(
            'Back to Continents',
            id='va-back-button',
            n_clicks=0,
            style={
                'display': 'none',
                'backgroundColor': '#14B8A6',
                'color': '#F9FAFB',
                'padding': '10px 20px',
                'border': 'none',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '500',
                'marginBottom': '15px',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'background': 'linear-gradient(135deg, #1E3A8A, #14B8A6)',
                    'transform': 'scale(1.05)'
                }
            }
        ),
        dcc.Graph(id='va-continent')
    ])

@app.callback(
    [Output('va-continent', 'figure'),
     Output('va-back-button', 'style'),
     Output('selected-va-continent', 'data')],
    [Input('va-continent', 'clickData'),
     Input('va-back-button', 'n_clicks')],
    [State('selected-va-continent', 'data')]
)
def update_virtual_assistant(clickData, back_clicks, selected_continent):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    va_continent_data = df[df['data_type'] == 'assistant data'].groupby('continent').size().reset_index(name='count')
    primary_fig = px.bar(
        va_continent_data, 
        x='continent', 
        y='count',
        title='Virtual Assistant Requests by Continent',
        labels={'count': 'Number of Virtual assistant Requests', 'continent': 'Continent'},
        color='continent',
        color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A', '#FBBF24', '#8B5CF6'],
        template='plotly_white'
    ).update_layout(
        title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
        xaxis_title={'font': {'size': 14, 'color': '#374151'}},
        yaxis_title={'font': {'size': 14, 'color': '#374151'}},
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font={'family': 'Arial, sans-serif'}
    )
    button_style = {
        'display': 'none',
        'backgroundColor': '#14B8A6',
        'color': '#F9FAFB',
        'padding': '10px 20px',
        'border': 'none',
        'borderRadius': '6px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '500',
        'marginBottom': '15px',
        'transition': 'all 0.3s ease'
    }
    
    if triggered_id == 'va-continent' and clickData:
        continent = clickData['points'][0]['x']
        filtered_df = df[(df['data_type'] == 'assistant data') & (df['continent'] == continent)]
        country_data = filtered_df.groupby('country').size().reset_index(name='count')
        drilldown_fig = px.bar(
            country_data, 
            x='country', 
            y='count',
            title=f'Virtual Assistant Requests by Country in {continent}',
            labels={'count': 'Number of Requests', 'country': 'Country'},
            color='country',
            color_discrete_sequence=['#14B8A6', '#F87171', '#A3E635', '#1E3A8A', '#FBBF24', '#8B5CF6'],
            template='plotly_white'
        ).update_layout(
            title={'x': 0.5, 'font': {'size': 20, 'color': '#1E3A8A'}},
            xaxis_title={'font': {'size': 14, 'color': '#374151'}},
            yaxis_title={'font': {'size': 14, 'color': '#374151'}},
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font={'family': 'Arial, sans-serif'}
        )
        button_style['display'] = 'block'
        return drilldown_fig, button_style, continent
    
    elif triggered_id == 'va-back-button' and back_clicks:
        return primary_fig, {
            'display': 'none',
            'backgroundColor': '#14B8A6',
            'color': '#F9FAFB',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '6px',
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '500',
            'marginBottom': '15px',
            'transition': 'all 0.3s ease'
        }, None
    
    return primary_fig, button_style, selected_continent

@app.callback(
    Output('export-button', 'children'),
    Input('export-button', 'n_clicks'),
    prevent_initial_call=True
)
def export_dataset(n_clicks):
    if n_clicks:
        return "Dataset Exported!"
    return "Export Dataset"

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)