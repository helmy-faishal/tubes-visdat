#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.layouts import Column, row
from bokeh.models import DateSlider, Select


# In[22]:


# Memuat Dataset
df = pd.read_csv('./data/Daily-Update-IDN-COVID19.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)


# In[23]:


label_columns = {
    'Kasus kumulatif':'Cumulative_cases' ,
    'Kasus sembuh':'Recovered_cases' ,
    'Total kematian':'Total_death' ,
    'Pasien dalam perawatan':'Patient_under_treatment',
    'Kasus baru per hari':'New_case_perDay',
    'Kasus sembuh per hari':'Recovered-cases_perDay',
    'Kasus pengobatan per hari':'Treatment_cases_perDay' ,
}


# In[24]:


source = ColumnDataSource(data={
    'x': df.loc["2020-03-02":].index,
    'y': df.loc["2020-03-02":]['Cumulative_cases'],
})


# In[25]:


plot = figure(
    title='Data Covid19 dari tanggal 2020-03-02', 
    x_axis_label='Tanggal', 
    y_axis_label='Kasus kumulatif',
    x_axis_type="datetime",
    plot_height=700, 
    plot_width=1000,
)

plot.line(x='x', y='y', source=source)


# In[26]:


def update_plot(attr, old, new):
    date = slider.value_as_date
    y = y_select.value

    plot.yaxis.axis_label = y

    new_data = {
    'x'       : list(df.loc[date:].index),
    'y'       : df.loc[date:][label_columns[y]],
    }
    source.data = new_data
    
    plot.title.text = f'Data Covid19 dari tanggal  {date}'


# In[27]:


slider = DateSlider(
    start=pd.to_datetime('2020-03-02'), 
    end=pd.to_datetime("2020-11-12"), 
    step=int(24*60*60*1000), 
    value=pd.to_datetime('2020-03-02'), 
    title='Mulai dari tanggal ')

slider.on_change('value',update_plot)


# In[28]:


y_select = Select(
    options=list(label_columns.keys()),
    value='Kasus kumulatif',
    title='Lihat berdasarkan'
)

y_select.on_change('value', update_plot)


# In[29]:


layout = row(Column(slider, y_select), plot)
curdoc().add_root(layout)


# In[30]:


# bokeh serve --show tubes-visdat.py

