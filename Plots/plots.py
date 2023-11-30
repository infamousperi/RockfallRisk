import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import Calculations.preperations as prep

order = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']


def show_scatter_stones(df, title):
    fig = px.scatter(df, x='Mass [kg]', y='Velocity [m/s]', size='Kinetic Energy [kJ]', color='Kinetic Energy [kJ]',
                     title="Scatter-Diagram of Separation Zone " + str(title), range_color=(0, 500))
    fig.show()


def show_compared_instances_by_time(df1, df2):
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", x=df1['Time'], name="Separation Zone 1"))
    fig.add_trace(go.Histogram(histfunc="count", x=df2['Time'], name="Separation Zone 2"))

    fig.update_xaxes(categoryorder='array', categoryarray=order)
    fig.update_layout(title_text='Rockfall Instances by Timestamp',
                      yaxis_title_text='Count',
                      xaxis_title_text='Time')
    fig.show()


def show_event_timeing(df1, df2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['Date'], y=df1['Time'], marker=dict(size=8), name="Separation Zone 1"))
    fig.add_trace(go.Scatter(x=df2['Date'], y=df2['Time'], marker=dict(size=4), name="Separation Zone 2"))

    date_order = prep.create_date_order()
    fig.update_yaxes(categoryorder='array', categoryarray=order)
    fig.update_xaxes(categoryorder='array', categoryarray=date_order)
    fig.update_traces(mode="markers", hovertemplate=None)
    fig.update_layout(title_text='Rockfall Instances Timeline',
                      xaxis_title_text='Date',
                      yaxis_title_text='Time')
    fig.show()


def show_histogram_velocity(df1, df2):
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Histogram(x=df1['Velocity [m/s]'], name="Separation Zone 1"), row=1, col=1)
    fig.add_trace(go.Histogram(x=df2['Velocity [m/s]'], name="Separation Zone 2"), row=1, col=2)

    fig.update_traces(xbins=dict(size=1))
    fig.update_layout(title_text='Rockfall Histogram By Velocity')
    fig.update_xaxes(title_text='Velocity [m/s]', row=1, col=1)
    fig.update_xaxes(title_text='Velocity [m/s]', row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.show()


def show_histogram_mass(df1, df2):
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Histogram(x=df1['Mass [kg]'], name="Separation Zone 1"), row=1, col=1)
    fig.add_trace(go.Histogram(x=df2['Mass [kg]'], name="Separation Zone 2"), row=1, col=2)

    fig.update_traces(xbins=dict(size=100))
    fig.update_layout(title_text='Rockfall Histogram By Mass')
    fig.update_xaxes(title_text='Mass [kg]', row=1, col=1)
    fig.update_xaxes(title_text='Mass [kg]', row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.show()


def show_box_velocity(df1, df2):
    fig = go.Figure()
    fig.add_trace(go.Box(x=df1['Velocity [m/s]'], name="Separation Zone 1"))
    fig.add_trace(go.Box(x=df2['Velocity [m/s]'], name="Separation Zone 2"))

    fig.update_layout(title_text='Rockfall Boxplot By Velocity')
    fig.show()


def show_box_mass(df1, df2):
    fig = go.Figure()
    fig.add_trace(go.Box(x=df1['Mass [kg]'], name="Separation Zone 1"))
    fig.add_trace(go.Box(x=df2['Mass [kg]'], name="Separation Zone 2"))

    fig.update_layout(title_text='Rockfall Boxplot By Mass')
    fig.show()


def show_kJ_distribution(df1, df2):
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Histogram(x=df1['Kinetic Energy [kJ]'], name="Separation Zone 1"), row=1, col=1)
    fig.add_trace(go.Histogram(x=df2['Kinetic Energy [kJ]'], name="Separation Zone 2"), row=2, col=1)

    fig.update_traces(xbins=dict(size=5))
    fig.update_layout(title_text='KJ Distribution')
    fig.update_xaxes(title_text='Kinetic Energy [kJ]', range=[0, 400], row=1, col=1)
    fig.update_xaxes(title_text='Kinetic Energy [kJ]', range=[0, 400], row=2, col=1)
    fig.update_yaxes(title_text="Count", range=[0, 20], row=1, col=1)
    fig.update_yaxes(title_text="Count", range=[0, 20], row=2, col=1)
    fig.show()


def show_ectf_velocity(df):
    fig = px.ecdf(df, x='Velocity [m/s]')
    fig.show()

def show_density_velocity(df):
    fig = px.histogram(df, x='Velocity [m/s]', histnorm='probability density')
    fig.show()

def show_distplot_velocity(df):
    fig = ff.create_distplot([df['Velocity [m/s]']], ['Velocity [m/s]'])
    fig.show()