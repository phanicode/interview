# run file as python new.py uv1.csv locations.yaml\
# python new.py csv_filename yaml_filename
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
import yaml
import sys


def main():
    print(sys.argv)
    if len(sys.argv)>3:
        print("you have entered too many arguemnts")
        return False
    with open(sys.argv[2], 'r') as f:
        uvfitscode_color = yaml.load(f)
    output_file('newtest1.html')
    # these are the column values
    csv_fields= [a.strip() for a in """time(UTC),T1,T2,U(lambda),
    V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy)""".split(',')]
    df=table = pd.read_csv(sys.argv[1], names=csv_fields,skiprows=2)
    p = bp.figure(plot_width=400, plot_height=400,output_backend="webgl")
    
    for uv_fitscode, color in uvfitscode_color.items():
        read_all_uv(uv_fitscode, color, p, df)
    show(p)



# either do this or manually add all csv files into one in order to replicate 
# EHT paper


# TODO : Convert this into RGB values
# Eg: bc.HSL(f * i, 0.75, 0.5).to_rgb()
# TODO : Add hover capabilities
# https://www.kite.com/python/examples/2926/yaml-dump-a-dictionary-to-a-yaml-document


# all_location_list=['AA','AP','AZ','JC','LM','PV','SM']
# all_color_list=['red','green','blue','yellow','pink','grey','black']
# TODO: Make this a dictionaryy for better readability/sites
def read_all_uv(uv_fitscode, point_color,p,df):
    """Reads the uv_fitscode

        uv_fitscode: two lettered string like AA, AZ, AP
        point_color: color of the glyph
    """
    first_loc=df.loc[df['T1']==uv_fitscode]
    second_loc=df.loc[df['T2']==uv_fitscode]
    first_loc.append(second_loc, ignore_index=True)
    p.circle(first_loc["U(lambda)"],first_loc["V(lambda)"], size=2, color=point_color)




if __name__ == "__main__":
    main()

