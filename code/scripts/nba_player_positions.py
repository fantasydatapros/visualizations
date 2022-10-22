# General Packages
import numpy as np
import pandas as pd
import pybaseball as pyb
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib as mpl
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

#fonts to be used in the animation
REGULAR_FONT_FAMILY = Path(mpl.get_data_path(), "fonts/ttf/Exo-Regular.ttf")
BOLD_FONT_FAMILY = Path(mpl.get_data_path(), "fonts/ttf/Exo-Bold.ttf")
BG_COLOR = '#0f1f44'
FONT_COLOR = "#b3c1e1"
#set font colors to white in animations
mpl.rcParams['text.color'] = FONT_COLOR

data = pd.read_csv('data/nba_player_position.csv', index_col=0)

# Create a figure and a 3D Axes
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111, projection='3d')
fig.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.xaxis.set_pane_color(BG_COLOR)
ax.yaxis.set_pane_color(BG_COLOR)
ax.zaxis.set_pane_color(BG_COLOR)
# make the grid lines transparent
ax.xaxis._axinfo["grid"]['color'] =  BG_COLOR
ax.yaxis._axinfo["grid"]['color'] =  BG_COLOR
ax.zaxis._axinfo["grid"]['color'] =  BG_COLOR

ax.tick_params(color=FONT_COLOR, labelcolor=FONT_COLOR)
for spine in ax.spines.values():
    spine.set_edgecolor(FONT_COLOR)

ax.xaxis.line.set_color(FONT_COLOR)
ax.yaxis.line.set_color(FONT_COLOR)
ax.zaxis.line.set_color(FONT_COLOR)

# Create an init function and the animate functions.
# Both are explained in the tutorial. Since we are changing
# the the elevation and azimuth and no objects are really
# changed on the plot we don't have to return anything from
# the init and animate function. (return value is explained
# in the tutorial.
cols_unique = ['blue',  'green',  'red']
def init():
    guard = ax.scatter(data[data['pos2']=='Guard']['REB'], data[data['pos2']=='Guard']['AST'], data[data['pos2']=='Guard']['height_in'], marker='o', s=20, color='#ffc331', alpha=0.6,label='Guard')
    
    center = ax.scatter(data[data['pos2']=='Center']['REB'], data[data['pos2']=='Center']['AST'], data[data['pos2']=='Center']['height_in'], marker='o', s=20, color='#a32629', alpha=0.6,label='Center')
    
    forward = ax.scatter(data[data['pos2']=='Forward']['REB'], data[data['pos2']=='Forward']['AST'], data[data['pos2']=='Forward']['height_in'], marker='o', s=20, color='#6DB0F7', alpha=0.6,label='Forward')
    
    ax.legend(
        ['Guard', 'Center', 'Forward'], 
        loc='upper left', 
        bbox_to_anchor=(1.15, 0.75), 
        facecolor=BG_COLOR,
        prop=BOLD_FONT_FAMILY
    )
    
    ax.set_xlabel('REB / MIN', color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    ax.set_ylabel('AST / MIN', color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    ax.set_zlabel('Height (In)', color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    
    return fig,

def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,

# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)
# Save
anim.save('output/animations/NBA Player Positions.mp4', fps=30, extra_args=['-vcodec', 'libx264'])