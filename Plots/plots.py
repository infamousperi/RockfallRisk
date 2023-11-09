import plotly.express as px
import plotly.graph_objects as go
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



