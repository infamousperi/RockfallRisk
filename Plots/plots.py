import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import Calculations.preperations as prep
import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import iplot

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


def show_histogram(df1, df2, plot_info, binsize):
    title = plot_info[0]
    column = plot_info[1]

    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Histogram(x=df1[column], name="Separation Zone 1"), row=1, col=1)
    fig.add_trace(go.Histogram(x=df2[column], name="Separation Zone 2"), row=1, col=2)

    fig.update_traces(xbins=dict(size=binsize))
    fig.update_layout(title_text='Rockfall Histogram By ' + title)
    fig.update_xaxes(title_text=column, row=1, col=1)
    fig.update_xaxes(title_text=column, row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.show()


def show_histogram_kinetic_energy(df1, df2):
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Histogram(x=df1['Kinetic Energy [kJ]'], name="Separation Zone 1"), row=1, col=1)
    fig.add_trace(go.Histogram(x=df2['Kinetic Energy [kJ]'], name="Separation Zone 2"), row=2, col=1)

    fig.update_traces(xbins=dict(size=5))
    fig.update_layout(title_text='Rockfall Histogram By Kinetic Energy')
    fig.update_xaxes(title_text='Kinetic Energy [kJ]', range=[0, 400], row=1, col=1)
    fig.update_xaxes(title_text='Kinetic Energy [kJ]', range=[0, 400], row=2, col=1)
    fig.update_yaxes(title_text="Count", range=[0, 20], row=1, col=1)
    fig.update_yaxes(title_text="Count", range=[0, 20], row=2, col=1)
    fig.show()


def show_box(df1, df2, plot_info):
    title = plot_info[0]
    column = plot_info[1]

    fig = go.Figure()
    fig.add_trace(go.Box(x=df1[column], name="Separation Zone 1"))
    fig.add_trace(go.Box(x=df2[column], name="Separation Zone 2"))

    fig.update_layout(title_text='Rockfall Boxplot By ' + title)
    fig.show()


def show_dist_plot(df1, df2, plot_info):
    title = plot_info[1]
    column = plot_info[1]
    hist_data = [df1[column], df2[column]]
    group_labels = ['Separation Zone 1', 'Separation Zone 2']

    fig = ff.create_distplot(hist_data, group_labels)

    fig.update_layout(title_text='Distribution of ' + title)
    fig.update_traces(autobinx=True, selector={'type': 'histogram'})
    fig.update_layout(height=700, width=800)
    fig.show()


def show_time_between_events(df1, df2):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df1['DateTime'], y=df1['TimeDiffHours'],
                             mode='lines+markers',
                             name="Separation Zone 1"))

    fig.add_trace(go.Scatter(x=df2['DateTime'], y=df2['TimeDiffHours'],
                             mode='lines+markers',
                             name="Separation Zone 2"))

    fig.update_layout(title='Time Between Events over Time',
                      xaxis_title='DateTime of Event',
                      yaxis_title='Hours',
                      legend_title='Metrics')
    fig.show()


def show_simulated_data(df1, df2, plot_info, n_years):
    title = plot_info[0]
    column = plot_info[1]

    mean_zone1 = np.mean(df1[column])
    mean_zone2 = np.mean(df2[column])

    std_dev_zone1 = np.std(df1[column])
    std_dev_zone2 = np.std(df2[column])

    plt.figure(figsize=(12, 8))

    plt.hist(df1, bins='auto', edgecolor='black', density=True, alpha=0.5,
             label='M.C.-Simulation Zone 1')
    plt.hist(df2, bins='auto', edgecolor='black', density=True, alpha=0.5,
             label='M.C.-Simulation Zone 2')

    plt.axvline(np.median(df1), color='green', linestyle='dashed', linewidth=2,
                label=f'Median Zone 1: {np.median(df1):.2f}')

    plt.axvline(np.median(df2), color='green', linestyle='dashed', linewidth=2,
                label=f'Median Zone 2: {np.median(df2):.2f}')

    plt.title('Monte Carlo-Simulationen: '+title+' Zone 1 und Zone 2 (' + str(n_years) + ' Jahre)')
    plt.xlabel(column)
    plt.ylabel('Häufigkeit')
    plt.legend()
    plt.show()

