import numpy as np
from numpy.lib.twodim_base import tri
import plotly
import plotly.graph_objects as go
from IPython.core.display import HTML
import matplotlib

import GenerateHeightMap as genMap
import Erode
import InteractingErode

def matplotlib_to_plotly(cmap, pl_entries):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])

    return pl_colorscale

terrain_cmap = matplotlib.cm.get_cmap('terrain')
terrain = matplotlib_to_plotly(terrain_cmap, 255)


mapSize = 100

heightMap = genMap.generateMapTest(4,mapSize)

erodedMap = heightMap.copy()


erodedMap = InteractingErode.Erode(70000,erodedMap)






plotly.offline.init_notebook_mode(connected=True)
figErode = go.Figure(data=[go.Surface(colorscale=terrain,z=erodedMap)])
figErode.update_layout(title='Eroded')
htmlErode= plotly.offline.plot(figErode, filename='Eroded.html',include_plotlyjs='cdn')
HTML(htmlErode)

fig = go.Figure(data=[go.Surface(colorscale=terrain,z=heightMap)])
fig.update_layout(title='Not Eroded')
html= plotly.offline.plot(fig, filename='notEroded.html',include_plotlyjs='cdn')


HTML(html)

