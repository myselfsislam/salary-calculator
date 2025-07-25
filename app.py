import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.graph_objects as go
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Salary data by location and grade
SALARY_DATA = {
    'BLR': {'A1': 600000, 'A2': 800000, 'A3': 1000000, 'B1': 1200000, 'B2': 1400000, 'B3': 1600000},
    'MEX': {'A1': 450000, 'A2': 600000, 'A3': 750000, 'B1': 900000, 'B2': 1050000, 'B3': 1200000},
    'LIS': {'A1': 2400000, 'A2': 3200000, 'A3': 4000000, 'B1': 4800000, 'B2': 5600000, 'B3': 6400000},
    'LON': {'A1': 4800000, 'A2': 6400000, 'A3': 8000000, 'B1': 9600000, 'B2': 11200000, 'B3': 12800000},
    'ROM': {'A1': 1800000, 'A2': 2400000, 'A3': 3000000, 'B1': 3600000, 'B2': 4200000, 'B3': 4800000},
    'ARG': {'A1': 350000, 'A2': 470000, 'A3': 590000, 'B1': 710000, 'B2': 830000, 'B3': 950000},
    'AUS': {'A1': 5500000, 'A2': 7300000, 'A3': 9100000, 'B1': 10900000, 'B2': 12700000, 'B3': 14500000},
    'MAD': {'A1': 2200000, 'A2': 2900000, 'A3': 3600000, 'B1': 4300000, 'B2': 5000000, 'B3': 5700000},
    'MTV': {'A1': 12000000, 'A2': 16000000, 'A3': 20000000, 'B1': 24000000, 'B2': 28000000, 'B3': 32000000},
    'TLV': {'A1': 4000000, 'A2': 5300000, 'A3': 6600000, 'B1': 8000000, 'B2': 9300000, 'B3': 10600000}
}

# Currency data by location
CURRENCY_DATA = {
    'BLR': {'symbol': 'Rs', 'rate': 1, 'name': 'INR'},
    'MEX': {'symbol': 'MX$', 'rate': 0.6, 'name': 'MXN'},
    'LIS': {'symbol': 'EUR', 'rate': 0.011, 'name': 'EUR'},
    'LON': {'symbol': 'GBP', 'rate': 0.0095, 'name': 'GBP'},
    'ROM': {'symbol': 'RON', 'rate': 0.055, 'name': 'RON'},
    'ARG': {'symbol': 'AR$', 'rate': 0.105, 'name': 'ARS'},
    'AUS': {'symbol': 'AU$', 'rate': 0.018, 'name': 'AUD'},
    'MAD': {'symbol': 'EUR', 'rate': 0.011, 'name': 'EUR'},
    'MTV': {'symbol': 'USD', 'rate': 0.012, 'name': 'USD'},
    'TLV': {'symbol': 'ILS', 'rate': 0.044, 'name': 'ILS'}
}

# Workdays data by location
WORKDAYS_DATA = {
    'ARG': 236,
    'AUS': 252,
    'BLR': 236,
    'LIS': 220,
    'LON': 227,
    'MAD': 230,
    'MEX': 241,
    'MTV': 252,
    'ROM': 233,
    'TLV': 224
}

LOCATION_OPTIONS = [
    {'label': '🇮🇳 Bangalore, India', 'value': 'BLR'},
    {'label': '🇲🇽 Mexico City, Mexico', 'value': 'MEX'},
    {'label': '🇵🇹 Lisbon, Portugal', 'value': 'LIS'},
    {'label': '🇬🇧 London, UK', 'value': 'LON'},
    {'label': '🇷🇴 Bucharest, Romania', 'value': 'ROM'},
    {'label': '🇦🇷 Buenos Aires, Argentina', 'value': 'ARG'},
    {'label': '🇦🇺 Sydney, Australia', 'value': 'AUS'},
    {'label': '🇪🇸 Madrid, Spain', 'value': 'MAD'},
    {'label': '🇺🇸 Mountain View, USA', 'value': 'MTV'},
    {'label': '🇮🇱 Tel Aviv, Israel', 'value': 'TLV'}
]

GRADE_OPTIONS = [
    {'label': 'A1 - Graduate Engineer', 'value': 'A1'},
    {'label': 'A2 - Engineer', 'value': 'A2'},
    {'label': 'B1 - Senior Engineer', 'value': 'B1'},
    {'label': 'B2 - Team Lead', 'value': 'B2'},
    {'label': 'C1 - Manager', 'value': 'C1'},
    {'label': 'C2 - Senior Manager', 'value': 'C2'},
    {'label': 'C3 - Director', 'value': 'C3'}
]

# Helper functions - defined before layout
def create_metric_card(icon, title, value, subtitle, variant="primary"):
    # Only values use rgb(59, 130, 246), headers remain original color
    value_color = "rgb(59, 130, 246)"
    
    return html.Div([
        html.Div([
            html.Span(icon, style={
                'fontSize': '1.2rem',
                'marginRight': '8px',
                'color': '#374151'  # Original gray color for icon
            }),
            html.Span(title, style={
                'fontSize': '0.85rem',
                'fontWeight': '600',
                'color': '#374151',  # Original gray color for title
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '4px'
        }),
        html.Div(value, style={
            'fontSize': '1.3rem',
            'fontWeight': '800',
            'color': value_color,  # Blue color for values only
            'lineHeight': '1.2',
            'marginBottom': '2px',
            'fontFamily': 'system-ui, monospace'
        }),
        html.Div(subtitle, style={
            'fontSize': '0.7rem',
            'color': '#6b7280',  # Original gray color for subtitle
            'fontWeight': '500'
        })
    ], style={
        'padding': '12px 0',
        'borderBottom': '1px solid #f3f4f6',
        'textAlign': 'left'
    })

def create_glossary_metric(icon, title, description, formula, example):
    return html.Div([
        html.Div([
            html.Span(icon, style={'fontSize': '1.3rem', 'marginRight': '10px'}),
            html.Span(title, style={
                'fontSize': '1.1rem',
                'fontWeight': '700',
                'color': '#1f2937'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '12px'
        }),
        html.P(description, style={
            'fontSize': '0.9rem',
            'color': '#4b5563',
            'marginBottom': '12px',
            'lineHeight': '1.5'
        }),
        html.Div([
            html.Div("Formula:", style={
                'fontSize': '0.8rem',
                'fontWeight': '600',
                'color': '#374151',
                'marginBottom': '4px'
            }),
            html.Code(formula, style={
                'fontSize': '0.8rem',
                'background': '#f1f5f9',
                'padding': '8px',
                'borderRadius': '4px',
                'display': 'block',
                'color': 'rgb(59, 130, 246)',
                'fontFamily': 'SF Mono, Monaco, monospace'
            })
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Div("Example:", style={
                'fontSize': '0.8rem',
                'fontWeight': '600',
                'color': '#374151',
                'marginBottom': '4px'
            }),
            html.Div(example, style={
                'fontSize': '0.75rem',
                'color': '#6b7280',
                'fontStyle': 'italic'
            })
        ])
    ], style={
        'background': '#ffffff',
        'border': '1px solid #e5e7eb',
        'borderRadius': '8px',
        'padding': '16px',
        'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)'
    })

# Define the layout
app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1("🌟Compensation Intelligence Platform", style={
                'fontSize': '3rem',
                'fontWeight': '800',
                'background': 'linear-gradient(135deg, #9333ea, #3b82f6, #10b981)',
                'WebkitBackgroundClip': 'text',
                'WebkitTextFillColor': 'transparent',
                'marginBottom': '8px',
                'letterSpacing': '-0.02em',
                'textAlign': 'center'
            }),
        ], style={'textAlign': 'center', 'marginBottom': '24px'}),
        
        # Main Layout Grid
        html.Div([
            # Left Panel - Configuration
            html.Div([
                html.H2("⚙️ Configuration Matrix", style={
                    'fontSize': '1.4rem',
                    'fontWeight': '700',
                    'color': '#1f2937',
                    'marginBottom': '24px',
                    'background': 'linear-gradient(135deg, #9333ea, #3b82f6)',
                    'WebkitBackgroundClip': 'text',
                    'WebkitTextFillColor': 'transparent'
                }),
                
                html.Div([
                    # Location
                    html.Div([
                        html.Label("🌍 Global Hub", style={
                            'fontWeight': '600', 
                            'marginBottom': '8px', 
                            'color': '#1f2937', 
                            'display': 'block',
                            'fontSize': '0.95rem'
                        }),
                        dcc.Dropdown(
                            id='location-dropdown',
                            options=LOCATION_OPTIONS,
                            value='BLR',
                            style={'marginBottom': '16px', 'fontSize': '14px'}
                        )
                    ], style={'marginBottom': '16px'}),
                    
                    # Grade
                    html.Div([
                        html.Label("🎯 Skill Tier", style={
                            'fontWeight': '600', 
                            'marginBottom': '8px', 
                            'color': '#1f2937', 
                            'display': 'block',
                            'fontSize': '0.95rem'
                        }),
                        dcc.Dropdown(
                            id='grade-dropdown',
                            options=GRADE_OPTIONS,
                            value='A2',
                            style={'marginBottom': '16px', 'fontSize': '14px'}
                        )
                    ], style={'marginBottom': '16px'}),
                    
                    # Experience
                    html.Div([
                        html.Label("⚡ Experience (Years)", style={
                            'fontWeight': '600', 
                            'marginBottom': '8px', 
                            'color': '#1f2937', 
                            'display': 'block',
                            'fontSize': '0.95rem'
                        }),
                        dcc.Input(
                            id='experience-slider',
                            type='number',
                            min=0, max=20, step=0.5, value=1.5,
                            placeholder="1.5",
                            style={
                                'width': '100%',
                                'height': '36px',
                                'padding': '8px 12px',
                                'border': '1px solid #d1d5db',
                                'borderRadius': '6px',
                                'fontSize': '14px',
                                'background': '#ffffff',
                                'boxSizing': 'border-box'
                            }
                        )
                    ], style={'marginBottom': '16px'}),
                    
                    # Margin
                    html.Div([
                        html.Label("📊 Target Margin (%)", style={
                            'fontWeight': '600', 
                            'marginBottom': '8px', 
                            'color': '#1f2937', 
                            'display': 'block',
                            'fontSize': '0.95rem'
                        }),
                        dcc.Input(
                            id='margin-slider',
                            type='number',
                            min=0, max=100, step=1, value=35,
                            placeholder="35",
                            style={
                                'width': '100%',
                                'height': '36px',
                                'padding': '8px 12px',
                                'border': '1px solid #d1d5db',
                                'borderRadius': '6px',
                                'fontSize': '14px',
                                'background': '#ffffff',
                                'boxSizing': 'border-box'
                            }
                        )
                    ], style={'marginBottom': '16px'}),
                    
                    # Annual CTC
                    html.Div([
                        html.Label("💰 Annual CTC", style={
                            'fontWeight': '600', 
                            'marginBottom': '8px', 
                            'color': '#1f2937', 
                            'display': 'block',
                            'fontSize': '0.95rem'
                        }),
                        dcc.Input(
                            id='annual-ctc',
                            type='number',
                            min=0, step=1000, value=1000000,
                            placeholder="1000000",
                            style={
                                'width': '100%',
                                'height': '36px',
                                'padding': '8px 12px',
                                'border': '1px solid #d1d5db',
                                'borderRadius': '6px',
                                'fontSize': '14px',
                                'background': '#ffffff',
                                'boxSizing': 'border-box'
                            }
                        )
                    ], style={'marginBottom': '16px'}),
                    
                    # Hours
                    html.Div([
                        html.Label("🔥 Billable Hours/Day", style={
                            'fontWeight': '600', 
                            'marginBottom': '8px', 
                            'color': '#1f2937', 
                            'display': 'block',
                            'fontSize': '0.95rem'
                        }),
                        dcc.Input(
                            id='hours-slider',
                            type='number',
                            min=1, max=12, step=0.5, value=4,
                            placeholder="4",
                            style={
                                'width': '100%',
                                'height': '36px',
                                'padding': '8px 12px',
                                'border': '1px solid #d1d5db',
                                'borderRadius': '6px',
                                'fontSize': '14px',
                                'background': '#ffffff',
                                'boxSizing': 'border-box'
                            }
                        )
                    ], style={'marginBottom': '16px'}),
                    
                    # Days
                    html.Div([
                        html.Label("📅 Annual Workdays", style={
                            'fontWeight': '600', 
                            'marginBottom': '8px', 
                            'color': '#1f2937', 
                            'display': 'block',
                            'fontSize': '0.95rem'
                        }),
                        dcc.Input(
                            id='days-slider',
                            type='number',
                            min=200, max=300, step=1, value=236,
                            placeholder="236",
                            disabled=True,
                            style={
                                'width': '100%',
                                'height': '36px',
                                'padding': '8px 12px',
                                'border': '1px solid #d1d5db',
                                'borderRadius': '6px',
                                'fontSize': '14px',
                                'background': '#f9fafb',
                                'color': '#6b7280',
                                'boxSizing': 'border-box'
                            }
                        )
                    ], style={'marginBottom': '16px'})
                ], style={
                    'display': 'flex',
                    'flexDirection': 'column'
                })
            ], style={
                'background': '#ffffff',
                'border': '1px solid #e5e7eb',
                'borderRadius': '12px',
                'padding': '24px',
                'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)'
            }),
            
            # Right Panel - Results
            html.Div([
                html.Div([
                    html.H3("💰 Compensation Matrix", style={
                        'fontSize': '1.4rem',
                        'fontWeight': '700',
                        'color': '#1f2937',
                        'marginBottom': '8px',
                        'textAlign': 'center'
                    }),
                    html.Button("📚 View Glossary", 
                        id="glossary-button",
                        style={
                            'fontSize': '0.85rem',
                            'color': 'rgb(59, 130, 246)',
                            'background': 'transparent',
                            'border': '1px solid rgb(59, 130, 246)',
                            'borderRadius': '6px',
                            'padding': '4px 8px',
                            'cursor': 'pointer',
                            'fontWeight': '600',
                            'marginBottom': '16px',
                            'transition': 'all 0.2s ease'
                        }
                    )
                ], style={
                    'textAlign': 'center',
                    'marginBottom': '20px'
                }),
                html.Div(id="results-grid", style={
                    'display': 'grid',
                    'gridTemplateColumns': '1fr 1fr 1fr',
                    'gap': '16px 20px',
                    'alignItems': 'start'
                })
            ], style={
                'background': '#ffffff',
                'border': '1px solid #e5e7eb',
                'borderRadius': '12px',
                'padding': '24px',
                'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
                'height': 'fit-content',
                'position': 'sticky',
                'top': '20px'
            }),
            
            # Glossary Modal
            html.Div([
                html.Div([
                    html.Div([
                        html.Button("✕", 
                            id="close-glossary",
                            style={
                                'position': 'absolute',
                                'top': '20px',
                                'right': '20px',
                                'background': 'transparent',
                                'border': 'none',
                                'fontSize': '1.5rem',
                                'cursor': 'pointer',
                                'color': '#6b7280',
                                'fontWeight': 'bold'
                            }
                        ),
                        html.Div([
                            html.H2("📚 Compensation Matrix Glossary", style={
                                'fontSize': '2rem',
                                'fontWeight': '700',
                                'color': '#1f2937',
                                'marginBottom': '20px',
                                'textAlign': 'center'
                            }),
                            html.P("Comprehensive guide to understanding all calculations and metrics used in the compensation analysis.", style={
                                'fontSize': '1rem',
                                'color': '#6b7280',
                                'textAlign': 'center',
                                'marginBottom': '30px',
                                'maxWidth': '600px',
                                'margin': '0 auto 30px auto'
                            }),
                            
                            # Metrics explanations
                            html.Div([
                                create_glossary_metric("", "Annual Base Salary", 
                                    "Primary annual compensation before benefits and bonuses, calculated based on location, grade, and experience.",
                                    "Base Salary = (Grade Base Salary × Experience Multiplier) × Currency Rate",
                                    "Experience Multiplier = 1 + (Years of Experience × 0.1)"),
                                
                                create_glossary_metric("", "Monthly Draw",
                                    "Monthly salary amount, calculated by dividing the annual base salary by 12 months.",
                                    "Monthly Draw = Annual Base Salary ÷ 12",
                                    "Example: £124,800 ÷ 12 = £10,400"),
                                
                                create_glossary_metric("", "USD Equivalent",
                                    "Annual salary converted to US Dollars for global comparison, using standard conversion rates.",
                                    "USD Equivalent = Local Salary (INR) ÷ 83",
                                    "Example: ₹13,12,000 ÷ 83 = $15,807"),
                                
                                create_glossary_metric("", "Total CTC",
                                    "Cost to Company including benefits, taxes, and additional compensation components.",
                                    "Total CTC = Annual Base Salary × 1.3",
                                    "Includes 30% overhead for benefits and taxes"),
                                
                                create_glossary_metric("", "Total Annual Hours",
                                    "Total working hours in a year, calculated based on location-specific working days.",
                                    "Total Hours = Annual Workdays × 8 hours",
                                    "Example: 227 days × 8 = 1,816 hours"),
                                
                                create_glossary_metric("", "Annual Billable Hours",
                                    "Hours that can be directly billed to clients, based on daily billable capacity.",
                                    "Billable Hours = Annual Workdays × Daily Billable Hours",
                                    "Example: 227 × 4 = 908 hours"),
                                
                                create_glossary_metric("", "Internal Hourly Cost",
                                    "Cost per hour for the company, including all employee expenses divided by total working hours.",
                                    "Hourly Cost = Annual Base Salary ÷ Total Annual Hours",
                                    "Example: £124,800 ÷ 1,816 = £68.73/hour"),
                                
                                create_glossary_metric("", "Minimum Hourly Rate",
                                    "Break-even hourly billing rate required to achieve the target profit margin.",
                                    "Min Rate = Cost per Billable Hour ÷ (1 - Target Margin ÷ 100)",
                                    "Cost per Billable Hour = (Annual Salary USD) ÷ Annual Billable Hours"),
                                
                                create_glossary_metric("", "Client Billing Rate",
                                    "Recommended premium billing rate for clients, with additional markup for competitive positioning.",
                                    "Client Rate = Minimum Hourly Rate × 1.75",
                                    "Includes 75% markup over minimum rate"),
                                
                                create_glossary_metric("", "Actual Profit Margin",
                                    "Real profit percentage achieved at the recommended client billing rate.",
                                    "Profit Margin = ((Client Rate - Cost per Hour) ÷ Client Rate) × 100",
                                    "Shows actual profitability at recommended rates"),
                                
                                create_glossary_metric("", "Monthly Revenue Projection",
                                    "Expected monthly revenue generated from this resource at full billable capacity.",
                                    "Monthly Revenue = Client Rate × Daily Billable Hours × (Workdays ÷ 12)",
                                    "Projected earnings at full capacity")
                                
                            ], style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))',
                                'gap': '20px',
                                'marginBottom': '30px'
                            }),
                            
                            # Key assumptions
                            html.Div([
                                html.H3("🔍 Key Assumptions", style={
                                    'fontSize': '1.3rem',
                                    'fontWeight': '700',
                                    'color': '#1f2937',
                                    'marginBottom': '15px'
                                }),
                                html.Ul([
                                    html.Li("Experience multiplier adds 10% to base salary for each year"),
                                    html.Li("Total CTC includes 30% overhead for benefits and taxes"),
                                    html.Li("USD conversion uses standard rate of 83 INR = 1 USD"),
                                    html.Li("Working days vary by location based on local practices"),
                                    html.Li("Standard working day is 8 hours for capacity calculations"),
                                    html.Li("Client billing rate includes 75% markup over minimum rate"),
                                    html.Li("All calculations rounded for practical use")
                                ], style={
                                    'color': '#4b5563',
                                    'fontSize': '0.9rem',
                                    'lineHeight': '1.6'
                                })
                            ], style={
                                'background': '#f8fafc',
                                'padding': '20px',
                                'borderRadius': '8px',
                                'border': '1px solid #e2e8f0'
                            })
                            
                        ], style={
                            'height': '80vh',
                            'overflowY': 'auto',
                            'padding': '20px'
                        })
                    ], style={
                        'background': '#ffffff',
                        'borderRadius': '12px',
                        'width': '90%',
                        'maxWidth': '1200px',
                        'maxHeight': '90vh',
                        'position': 'relative',
                        'boxShadow': '0 20px 60px rgba(0, 0, 0, 0.3)'
                    })
                ], style={
                    'position': 'fixed',
                    'top': '0',
                    'left': '0',
                    'width': '100%',
                    'height': '100%',
                    'background': 'rgba(0, 0, 0, 0.5)',
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'zIndex': '1000',
                    'backdropFilter': 'blur(5px)'
                })
            ], id="glossary-modal", style={'display': 'none'})
            
        ], style={
            'display': 'grid',
            'gridTemplateColumns': '320px 1fr',
            'gap': '24px',
            'alignItems': 'start'
        })
        
    ], style={'maxWidth': '1800px', 'margin': '0 auto'})
    
], style={
    'backgroundColor': '#f8fafc',
    'minHeight': '100vh',
    'padding': '16px',
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    'color': '#1f2937'
})

# Add JavaScript for ESC key functionality
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                document.addEventListener('keydown', function(event) {
                    if (event.key === 'Escape') {
                        const modal = document.getElementById('glossary-modal');
                        if (modal && modal.style.display !== 'none') {
                            modal.style.display = 'none';
                        }
                    }
                });
            });
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback to update workdays based on location
@app.callback(
    Output('days-slider', 'value'),
    [Input('location-dropdown', 'value')]
)
def update_workdays(location):
    if location in WORKDAYS_DATA:
        return WORKDAYS_DATA[location]
    return 236

# Callback to toggle glossary modal
@app.callback(
    Output('glossary-modal', 'style'),
    [Input('glossary-button', 'n_clicks'),
     Input('close-glossary', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_glossary(open_clicks, close_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {'display': 'none'}
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'glossary-button':
        return {
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'background': 'rgba(0, 0, 0, 0.5)',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'zIndex': '1000',
            'backdropFilter': 'blur(5px)'
        }
    else:
        return {'display': 'none'}

# Main calculation callback
@app.callback(
    Output('results-grid', 'children'),
    [Input('location-dropdown', 'value'),
     Input('grade-dropdown', 'value'),
     Input('experience-slider', 'value'),
     Input('margin-slider', 'value'),
     Input('annual-ctc', 'value'),
     Input('hours-slider', 'value'),
     Input('days-slider', 'value')],
    prevent_initial_call=False
)
def update_calculations(location, grade, experience, target_margin, annual_ctc, billable_hours, work_days):
    # Validate inputs and set defaults if None or invalid
    try:
        experience = float(experience) if experience is not None else 1.5
        target_margin = float(target_margin) if target_margin is not None else 35
        annual_ctc = float(annual_ctc) if annual_ctc is not None else 1000000
        billable_hours = float(billable_hours) if billable_hours is not None else 4
        
        # Use location-specific workdays
        if location in WORKDAYS_DATA:
            work_days = WORKDAYS_DATA[location]
        else:
            work_days = float(work_days) if work_days is not None else 236
        
        # Ensure values are within reasonable ranges
        experience = max(0, min(20, experience))
        target_margin = max(0, min(100, target_margin))
        annual_ctc = max(0, annual_ctc)
        billable_hours = max(1, min(12, billable_hours))
        work_days = max(200, min(300, work_days))
        
    except (ValueError, TypeError):
        # If any conversion fails, use default values
        experience = 1.5
        target_margin = 35
        annual_ctc = 1000000
        billable_hours = 4
        work_days = WORKDAYS_DATA.get(location, 236)
    
    # Validate location and grade
    if location not in CURRENCY_DATA or grade not in SALARY_DATA.get(location, {}):
        location = 'BLR'
        grade = 'A2'
    
    # Get currency and salary data
    currency = CURRENCY_DATA[location]
    base_salary = SALARY_DATA[location][grade]
    
    # Calculate salary metrics using user-provided CTC or calculated base salary
    if annual_ctc and annual_ctc > 0:
        # Use user-provided CTC
        local_salary_inr = annual_ctc
        local_salary = round(local_salary_inr * currency['rate'])
        ctc = annual_ctc
    else:
        # Use calculated base salary
        experience_multiplier = 1 + (experience * 0.1)
        local_salary_inr = round(base_salary * experience_multiplier)
        local_salary = round(local_salary_inr * currency['rate'])
        ctc = round(local_salary * 1.3)
    
    monthly_salary = round(local_salary / 12)
    usd_salary = round(local_salary_inr / 83)
    annual_hours = work_days * 8
    annual_billable_hours = work_days * billable_hours
    hourly_cost = round((local_salary / annual_hours) * 100) / 100
    
    ctc_usd = round(local_salary_inr * 1.3 / 83)
    
    # Billing calculations
    cost_per_billable_hour_usd = (local_salary_inr / 83) / annual_billable_hours
    min_hourly_rate = round((cost_per_billable_hour_usd / (1 - target_margin/100)) * 100) / 100
    cust_rate = round(min_hourly_rate * 1.75 * 100) / 100
    actual_margin = round(((cust_rate - cost_per_billable_hour_usd) / cust_rate) * 10000) / 100
    monthly_bill_rate = round(cust_rate * billable_hours * (work_days/12))
    
    # Create results cards
    results_cards = [
        create_metric_card("💎", "Annual Base", f"{currency['symbol']} {local_salary:,}", "Primary Compensation", "primary"),
        create_metric_card("🌙", "Monthly Draw", f"{currency['symbol']} {monthly_salary:,}", "Per Month", "secondary"),
        create_metric_card("🦅", "USD Equivalent", f"${usd_salary:,}", "Global Standard", "accent"),
        create_metric_card("🏆", "Total CTC", f"{currency['symbol']} {ctc:,}", f"${ctc_usd:,} USD", "primary"),
        create_metric_card("⏱️", "Total Hours", f"{annual_hours:,}", "Annual Capacity", "secondary"),
        create_metric_card("🔥", "Billable Hours", f"{annual_billable_hours:,}", "Revenue Hours", "accent"),
        create_metric_card("⚡", "Hourly Cost", f"{currency['symbol']} {hourly_cost}", "Internal Rate", "primary"),
        create_metric_card("📊", "Min Rate", f"${min_hourly_rate}", "Break-even Point", "secondary"),
        create_metric_card("🚀", "Client Rate", f"${cust_rate}/hr", "Premium Billing", "highlight"),
        create_metric_card("📈", "Profit Margin", f"{actual_margin}%", "Net Profitability", "accent"),
        create_metric_card("💰", "Monthly Revenue", f"${monthly_bill_rate:,}", "Projected Income", "highlight")
    ]
    
    return results_cards

if __name__ == '__main__':
    app.run(debug=True, port=8050)
