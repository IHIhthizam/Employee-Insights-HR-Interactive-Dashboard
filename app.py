##-----------------------------------NUHAN (1)------------------------------------##

#Required libraries

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

#Load and preprocess the dataset
# Load the dataset
df = pd.read_csv(r"preprocessed_data.csv")

# Preprocess the dataset
df['Joining Date'] = pd.to_datetime(df['Joining Date'])
df['Experience'] = df['Experience'].fillna(0)

# Filtering (Tab 1)
def filter_data(selected_statuses, start_year, end_year):
    return df[
        (df['Status'].isin(selected_statuses)) &
        (df['Joining Date'].dt.year >= start_year) &
        (df['Joining Date'].dt.year <= end_year)]

#---------------------------Tabs-------------------------------------

min = df['Joining Date'].dt.year.min()
max = df['Joining Date'].dt.year.max()

# Tab 1 - Employees Over Time
tab_1 = html.Div([
    html.Label("Select Status", className='status_label'),
    dcc.Dropdown(
        id='status_dropdown',
        options=[{'label': 'Active', 'value': 'Active'}, {'label': 'Inactive', 'value': 'Inactive'}],
        value=['Active'],
        multi=True,
        placeholder="Select one or more statuses",
        className='status_dropdown'),

    html.Label("Select Year Range", className='year_label'),
    dcc.RangeSlider(
        id='year_range_slider',
        min=min,
        max=max,
        step=1,
        value=[min, max],
        marks={year: {'label': str(year), 'style': {'color': '#ffffff'}} for year in range(min, max + 1)}, className='year_range'),

    dcc.Graph(id='line_chart', className='line_chart')
])


##-----------------------------------NUHAN - END (1)------------------------------------##

##-----------------------------------LAHIRU (1)------------------------------------##

# Tab 2 - Correlation Analysis
tab_2 = html.Div([
    html.Label("Select Variable for Correlation with Work Hours Per Week"),
    dcc.RadioItems(
        id='scatter_plot_variable',
        options=[
            {'label': 'Work Hours Per Week', 'value': 'Work_Hours_Per_Week'},
            {'label': 'Training Hours', 'value': 'Training_Hours'},
            {'label': 'Monthly Income', 'value': 'Monthly Income'}],
        value='Work_Hours_Per_Week',labelStyle={'display': 'block'}),

    dcc.Graph(id="scatter_plot", className='scatter_plot')
])

# Tab 3 - Department-Wise Analysis
tab_3 = html.Div([
    html.H3("Department-Wise Analysis", style={'textAlign': 'center', 'color': '#ffffff'}),
    html.Div([
        dcc.Graph(id='pie_chart', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='line_chart_2', style={'width': '50%', 'display': 'inline-block'})], className='tab3_charts', style={'textAlign': 'center'})])


##-----------------------------------LAHIRU - END (1)------------------------------------##
##-----------------------------------IHTHIZAM (1)------------------------------------##


# Tab 4 - Employees & Department
tab_4 = html.Div([
    dcc.Graph(id='pie_chart_status', style={'width': '35%', 'display': 'inline-block'}),
    dcc.Graph(id='bar_chart_department_status', style={'width': '32.5%', 'display': 'inline-block'}),
    dcc.Graph(id='line_chart_tenure', style={'width': '32.5%', 'display': 'inline-block'})], className='tab4_charts', style={'textAlign': 'center'})

#------------------------------Layout of the app------------------------------

layout_of_app = [
    html.H1("Employee Insights Dashboard", className='head_section'),
    html.H3("The Employee Insights Dashboard is an interactive dashboard that visualizes workforce data, highlighting trends, productivity patterns, and employee turnover.", className='sub_head_section'),

    dcc.Tabs(id='tabs', value='tab_1', className="tabs", children=[
        dcc.Tab(label='Employees Over Time', value='tab_1', children=tab_1, className='tab_content'),
        dcc.Tab(label='Correlation Analysis', value='tab_2', children=tab_2, className='tab_content'),
        dcc.Tab(label='Department-wise Analysis', value='tab_3', children=tab_3, className='tab_content'),
        dcc.Tab(label='Employees & Depatment', value='tab_4', children=tab_4, className='tab_content')
    ]),

    html.Footer([
        html.Div("Group Members", className='footer_section'),
        html.Div("Ihthizam - COHNDDS241F-012 | Nuhan - COHNDDS241F-013 | Lahiru - COHNDDS241F-002", className='footer_section')
    ])
]


#------------------------------Create the Dash app--------------------------------------

app = dash.Dash()
app.layout = html.Div(layout_of_app)
app.title = 'Employee Insights Dashboard'
##-----------------------------------IHTHIZAM - END (1)------------------------------------##

##-----------------------------------NUHAN (2)------------------------------------##
#-------------------------------Callbacks------------------------------------
# Tab 1 - Employees Over Time
@app.callback(
    Output('line_chart', 'figure'),
    [Input('status_dropdown', 'value'), Input('year_range_slider', 'value')])

def update_line_chart(selected_statuses, selected_years):
    start_year, end_year = selected_years
    filtered_df = filter_data(selected_statuses, start_year, end_year)

    # If no status is selected
    if filtered_df.empty:
        return px.line(title="No data available for the selected filters")

    # Extract year from Joining Date and group data
    filtered_df['Year'] = filtered_df['Joining Date'].dt.year
    grouped_df = filtered_df.groupby(['Year', 'Status']).size().reset_index(name='Employee Count')

    # Create the line chart
    fig = px.line(
        grouped_df,
        x='Year',
        y='Employee Count',
        color='Status',
        title="Number of Employees Over Time",
        labels={'Year': 'Year', 'Employee Count': 'Number of Employees', 'Status': 'Status'}
    )
    fig.update_layout(plot_bgcolor='#374149', paper_bgcolor='#374149', font_color='white')
    fig.update_traces(line=dict(color='#38b6ff', width=4), selector=dict(name='Active'))
    fig.update_traces(line=dict(color='#ef43cf', width=4), selector=dict(name='Inactive'))

    return fig
##-----------------------------------NUHAN - END (2)------------------------------------##
##-----------------------------------LAHIRU(2)------------------------------------##

# Tab 2 - Correlation Analysis
@app.callback(
    Output('scatter_plot', 'figure'),
    [Input('scatter_plot_variable', 'value')])

def update_scatter_plot(selected_variable):
    correlation = df['Productivity_%'].corr(df[selected_variable])

    fig = px.scatter(
        df,
        x='Productivity_%',
        y=selected_variable,
        color='Department',
        title=f"Scatter Plot: Productivity Percentage vs. {selected_variable} (Corr: {correlation:.2f})",
        labels={'Productivity_%': 'Productivity (%)', selected_variable: selected_variable},
        hover_data=['Name', 'Age', 'Gender'],
        color_discrete_map={'HR': '#ef43cf', 'Sales': '#f6f6f6', 'IT': '#38b6ff'}
    )

    fig.update_layout(
        xaxis_title="Productivity (%)",
        yaxis_title=selected_variable,
        legend_title="Department",
        plot_bgcolor='#374149', paper_bgcolor='#374149', font_color='white')

    return fig
##-----------------------------------LAHIRU - END (2)------------------------------------##

##-----------------------------------IHTHIZAM (2)------------------------------------##

# Tab 3 - Department-Wise Analysis
@app.callback(
    [Output('line_chart_2', 'figure'), Output('pie_chart', 'figure')],
    [Input('pie_chart', 'hoverData')])

def update_interactive_charts(hover_data):
    department = None
    if hover_data and 'points' in hover_data and len(hover_data['points']) > 0:
        department = hover_data['points'][0].get('label', None)

    pie_fig = px.pie(
        df,
        names='Department',
        title="Percentage of Workers by Department",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel)
    
    pie_fig.update_layout(plot_bgcolor='#374149', paper_bgcolor='#374149', font_color='white')
    

    if department:
        filtered_df = df[df['Department'] == department]
    else:
        filtered_df = df

    if not filtered_df.empty:
        filtered_df['Year'] = filtered_df['Joining Date'].dt.year
        grouped_df = filtered_df.groupby('Year')['Monthly Income'].mean().reset_index()

        line_fig = px.line(
            grouped_df,
            x='Year',
            y='Monthly Income',
            title=f"Average Monthly Income Over Years{' for ' + department if department else ''}",
            markers=True,
            labels={'Year': 'Year', 'Monthly Income': 'Average Monthly Income'},
            color_discrete_sequence=["#FFA07A"])
        
        line_fig.update_layout(plot_bgcolor='#374149', paper_bgcolor='#374149', font_color='white')

    else:
        
        line_fig = px.line(title="No data available for the selected department")

    return line_fig, pie_fig

# Tab 4 - Employees & Department
@app.callback(
    [Output('pie_chart_status', 'figure'), Output('bar_chart_department_status', 'figure'), Output('line_chart_tenure', 'figure')],
    [Input('pie_chart_status', 'hoverData')])

def update_tab4_turnover_charts(hover_data):
    status = None

    if hover_data and 'points' in hover_data and len(hover_data['points']) > 0:
        status = hover_data['points'][0].get('label', None)

    pie_fig = px.pie(
        df,
        names='Status',
        title="Employee Status Distribution",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel)
    
    pie_fig.update_layout(plot_bgcolor='#374149', paper_bgcolor='#374149', font_color='white')

    if status:
        filtered_df = df[df['Status'] == status]

    else:
        
        filtered_df = df

    bar_fig = px.bar(
        filtered_df.groupby('Department').size().reset_index(name='Count'),
        x='Department',
        y='Count',
        color='Department',
        title=f"Number of Employees by Department{' for ' + status if status else ''}",
        labels={'Count': 'Number of Employees'},
        color_discrete_sequence=px.colors.qualitative.Plotly)
    
    bar_fig.update_layout(plot_bgcolor='#374149', paper_bgcolor='#374149', font_color='white')

    if not filtered_df.empty:
        filtered_df['Year'] = filtered_df['Joining Date'].dt.year
        tenure_df = filtered_df.groupby(['Year', 'Department'])['Experience'].mean().reset_index()

        line_fig = px.line(
            tenure_df,
            x='Year',
            y='Experience',
            color='Department',
            title=f"Average Tenure Over Years{' for ' + status if status else ''}",
            markers=True,
            labels={'Year': 'Year', 'Experience': 'Average Tenure (Years)'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        line_fig.update_layout(plot_bgcolor='#374149', paper_bgcolor='#374149', font_color='white')

    else:
        
        line_fig = px.line(title="No data available for the selected status")

    return pie_fig, bar_fig, line_fig


#--------------------------------Run the app------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

##-----------------------------------IHTHIZAM - END (2)------------------------------------##