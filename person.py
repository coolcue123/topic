from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure,show


def __init__(data={}):

    x_list =[]
    y_list =[]
    for i in list(data.keys()):
        x_list.append(i)
        y_list.append(data[i])
    p = figure(x_range=x_list, title="分析柱狀圖")

    p.vbar(x=x_list, top=y_list, width=0.5, color=Spectral6)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    show(p)