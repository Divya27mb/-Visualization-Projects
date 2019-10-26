#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

from bokeh.io import show, curdoc, output_file
from bokeh.plotting import figure,output_notebook

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel , FactorRange
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs , Select

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application


#output_file("visualization.html")
#output_notebook()


df = pd.read_csv('stats.csv')
attri = list(df.columns)[1:len(df.columns)-1]
factors = []
factors.extend(list(zip(['General']*5,attri[:5])))
factors.extend(list(zip(['Attack']*10,attri[5:15])))
factors.extend(list(zip(['Defence']*13,attri[15:28])))
factors.extend(list(zip(['Team Play']*7,attri[28:34])))
factors.extend(list(zip(['Others']*8,attri[34:42])))



def make_dataset(years,team1,team2):
    Teams = list(set(df['team']))
    Two = ["team1","team2"]


#       print(years,team1, team2)
    first_team = list(df.loc[df['team'].isin([team1]) & df['season'].isin(years)].sum())[1:len(df.columns)-1]
    second_team = list(df.loc[df['team'].isin([team2]) & df['season'].isin(years)].sum())[1:len(df.columns)-1]
    first = []
    second = []
    for i in range(len(first_team)):
        first.append((first_team[i]/(first_team[i]+second_team[i]))*100)
        second.append((second_team[i]/(first_team[i]+second_team[i]))*100)

#         print(first)
#         print(second)

    plt_data = {'Attributes' : factors,
            "team1": first,
            "team2": second
            }



    return [Two,ColumnDataSource(plt_data)]

# Styling for a plot
# def style(p):
#     # Title 
#     p.title.align = 'center'
#     p.title.text_font_size = '20pt'
#     p.title.text_font = 'serif'

#     # Axis titles
#     p.xaxis.axis_label_text_font_size = '14pt'
#     p.xaxis.axis_label_text_font_style = 'bold'
#     p.yaxis.axis_label_text_font_size = '14pt'
#     p.yaxis.axis_label_text_font_style = 'bold'

#     # Tick labels
#     p.xaxis.major_label_text_font_size = '12pt'
#     p.yaxis.major_label_text_font_size = '12pt'

#     return p

# Function to make the plot
def make_plot(src):
    # Blank plot with correct labels

    #print(FactorRange(*factors))
    p = figure(y_range=FactorRange(*factors), plot_height=1000, x_range=(0,100), title="Comparison",
           toolbar_location=None,tools="hover", tooltips="@Attributes: @$name")
#         print("asdfasdfasdfasdfas"*3)
#         print(src[0])
    p.hbar_stack(src[0],y='Attributes', height= 0.5, color=["#c9d9d3", "#718dbf"], source= src[1])



    p.y_range.range_padding = 0.01
    p.ygrid.grid_line_color = '#ffffff'
    p.axis.minor_tick_line_color = '#ffffff'
    p.outline_line_color = '#ffffff'

    return p

# Update the plot based on selections
def update(attr, old, new):
    selected_years = [seasons.labels[i] for i in seasons.active]

#        print(select_1.value,select_2.value)
    new_src = make_dataset(selected_years,
                           select_1.value,
                           select_2.value
                           )

    src[1].data.update(new_src[1].data)
#         print(new_src[0][0])


seasons = CheckboxGroup(labels=list(set(df['season'])), active = [0,1])
seasons.on_change('active', update)

select_1 = Select(title="Team1:", value="Chelsea", options=list(set(df['team'])))
select_1.on_change('value',update)


select_2 = Select(title="Team2:", value="Manchester United", options=list(set(df['team'])))
select_2.on_change('value',update)


# Find the initially selected carrieres
#initial_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]
src = make_dataset([seasons.labels[i] for i in seasons.active],
                    select_1.value,
                    select_2.value
                        )

p = make_plot(src)

# Put controls in a single element
controls = WidgetBox(seasons,select_1,select_2)

# Create a row layout
layout = row(controls, p)

# Make a tab with the layout 
tab = Panel(child=layout, title = 'Project')
tabs = Tabs(tabs=[tab])
curdoc().add_root(tabs)


