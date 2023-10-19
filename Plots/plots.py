import plotly.express as px
import plotly.graph_objects as go

order = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']


def show_scatter_stones(df, title):
    fig = px.scatter(df, x='Mass [kg]', y='Velocity [m/s]', size='Kinetic Energy [kJ]', color='Kinetic Energy [kJ]',
                     title="Scatter-Diagram of Separation Zone " + str(title))
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
