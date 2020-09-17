import sys
import pandas as pd
import numpy  as np

import bokeh.layouts        as bl
import bokeh.models         as bm
import bokeh.colors         as bc
import bokeh.models.widgets as bw
import bokeh.plotting       as bp
import datetime
import os
import interview.widget as iw
from eat.io import hops, util
from bokeh.io import output_file, show
import matplotlib.pyplot as plt

output_file('newtest.html')
# these are the column values
csv_fields= [a.strip() for a in """time(UTC),T1,T2,U(lambda),
V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy)""".split(',')]

def gitcsv_read(file_name):
    table = pd.read_csv(file_name, names=csv_fields,skiprows=2)
    return table
df=gitcsv_read('uv1.csv')
# either do this or manually add all csv files into one in order to replicate 
# EHT paper
p = bp.figure(plot_width=400, plot_height=400,output_backend="webgl")

# TODO : Convert this into RGB values
# Eg: bc.HSL(f * i, 0.75, 0.5).to_rgb()
# TODO : Add hover capabilities
# https://www.kite.com/python/examples/2926/yaml-dump-a-dictionary-to-a-yaml-document


all_location_list=['AA','AP','AZ','JC','LM','PV','SM']
all_color_list=['red','green','blue','yellow','pink','grey','black']
# TODO: Make this a dictionaryy for better readability/sites
def read_all_uv(location, point_color):
    a=df.loc[df['T1']==location]
    print(a.head())
    b=df.loc[df['T2']==location]
    a.append(b, ignore_index=True)
    p.circle(a["U(lambda)"],a["V(lambda)"], size=2, color=point_color)

for i in range(len(all_color_list)):
    read_all_uv(all_location_list[i], all_color_list[i])



show(p)

