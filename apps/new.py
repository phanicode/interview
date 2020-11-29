# bokeh serve --show new.py or python demo2.py ( both run bokeh servers)

from bokeh.models.layouts import Panel, Row, Tabs
from bokeh.models.widgets.buttons import Button

import interview.widget.select as Select

import os
import pandas as pd
import numpy  as np
import bokeh.layouts        as bl
import bokeh.models         as bm
import bokeh.plotting       as bp
import os
import interview.widget as iw
import yaml
import ehtim as eh
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def mirror_uv(df):
    """T1 <-> T2 => u, v -> -u, -v; amp  -> amp, phase -> -phase.
    Returns new array with the additive inverse of the phase, u, v
    and swapped T1 and T2 indexes
    """
    # deepcopy ensures anti-aliasing but check if necessary as it is in different scope.
    df2=df.copy()
    col_list=list(df2)
    # TODO: adjust for column name ( something like for elem in column if U in elem then....)

    col_list[1], col_list[2] = col_list[2], col_list[1]
    # TODO: integrate this with U V and phase
    # TODO: Use YAML file
    df2.columns=col_list
    df2["U(lambda)"]*=-1
    df2["V(lambda)"]*=-1
    df2["Iphase(d)"]*=-1
    return df2


csv_fields= [a.strip() for a in """time(UTC),T1,T2,U(lambda),
V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy),sqrtu2v2""".split(',')]
file_list=[]
for root, dirs, files in os.walk('./uvfitsfiles'):
    for file in files:
        if file.endswith('.uvfits'):
            file_list.append(os.path.join(root, file))
            


df = pd.concat( map (lambda file : pd.DataFrame(eh.obsdata.load_uvfits(file).avg_coherent(inttime=300).
unpack(['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma']))\
,file_list) )

df['r'] = np.sqrt(df.u**2 + df.v**2)
df.columns=csv_fields
with open('./yaml_files/locations.yaml', 'r') as f:
    uvfitscode_color = yaml.load(f)
# auto load the csv headers into the hovertool
tool_tips_list=[]
for title in csv_fields:
    if "(" in title or ")" in title:
    # account for proper format brackets in titles
        tool_tips_list.append((title,"@"+"{"+title+"}"))
    else:
        tool_tips_list.append((title,"@"+title))
hover = bm.HoverTool(tooltips=tool_tips_list)
fig = bp.figure(title="u vs v graph",
    plot_height=800, plot_width=800
    ,x_axis_label="U(lambda)",y_axis_label= "V(lambda)",
    toolbar_location="right", tools=[hover,
    "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
    output_backend="webgl")
fig2 = bp.figure(title="r vs Y",
    plot_height=800, plot_width=800
    ,x_axis_label="r",y_axis_label= "Y value",
    toolbar_location="right", tools=[hover,
    "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
    output_backend="webgl",y_axis_type="log")
    
fig3 = bp.figure(title="Time Series",
    plot_height=1600, plot_width=1600
    ,x_axis_label="Time(UTC)",y_axis_label= "Y value",
    toolbar_location="right", tools=[hover,
    "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
     output_backend="webgl")
fig3.sizing_mode = 'scale_both'
df=df.assign(colors="black")
for sites,color in uvfitscode_color.items():
    df.loc[((df["T1"] == sites[0]) | (df["T1"] == sites[1])) & ((df["T2"] == sites[0]) | (df["T2"] == sites[1])),"colors"]=color
    
df_final=pd.concat([df,mirror_uv(df)])
src1 = bm.ColumnDataSource(df_final)
fig.x_range.flipped= True
plt1=fig.circle(x="U(lambda)", y="V(lambda)", color="colors",
                    source=src1, size=6)
plt2=fig2.circle(x="sqrtu2v2",y="Iamp(Jy)" ,\
        color="colors",source=src1, size=6)
plt3=fig3.circle(x="time(UTC)",y="Iamp(Jy)" ,\
        color="colors",source=src1, size=6)
        
selected_circle = bm.Circle(fill_alpha=1, fill_color="firebrick")
plt1.selection_glyph=selected_circle

plt3.selection_glyph=selected_circle

plt2.selection_glyph=selected_circle


opts_all={
    "time(UTC)": "time",
    "T1": "Site 1",
    "T2": "Site 2",
    "U(lambda)": "u",
    "V(lambda)": "v",
    "Iamp(Jy)": "Amplitude",        
    "Iphase(d)"   : "Phase",
    "sqrtu2v2": "r"
}


# define interaction
def print_datapoints():
    indices=src1.selected.indices
    results=df_final.iloc[indices, :-1]
    results.to_csv("temp.csv", mode='a', header=False)

btn = Button(label='Write selected points to CSV', button_type='success')
btn.on_click(print_datapoints)

select_x1  = iw.Select(plt1, 'x', opts_all)
select_y1  = iw.Select(plt1, 'y', opts_all)

inputs1  = bm.Column(btn,select_x1, select_y1)
select_y2  = iw.Select(plt2, 'y', opts_all)
scatter = bl.row(inputs1, fig,select_y2,fig2)
select_x3  = iw.Select(plt3, 'x', opts_all)
select_y3  = iw.Select(plt3, 'y', opts_all)
inputs3  = bm.Column(btn,select_x3, select_y3)
timeseries= bl.row(inputs3, fig3,)


all = bl.column(iw.Tabs({"Visibility and domain":scatter,
                         "Time Series": timeseries},
                        width=1024))
bp.curdoc().add_root(all)
bp.curdoc().title = "Demo 2"


bm.Glyph()
