# General Packages
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import matplotlib.font_manager as font_manager

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

#animation settings
POINT_OPACITY = 1
MARKER = 'o'
POINT_SIZE = 15
SLIDER_COLOR = '#ffc331'
SINKER_COLOR= 'pink'
FASTBALL_COLOR = '#a32629'
CHANGEUP_COLOR = '#54b2fd'
CURVEBALL_COLOR = 'white'
CUTTER_COLOR = '#202f52'

#import the data and prepare
pitches = pd.read_csv('data/pitch_data.csv', index_col=0)
pitches = pitches[pitches['pitch_name']!='Split-Finger']
pitches = pitches[pitches['pitch_name']!='Knuckle Curve']
pitches = pitches[pitches['p_throws']=='R']
pitches = pitches[:500]

sliders = pitches.loc[pitches['pitch_name'] == 'Slider']
sinkers = pitches.loc[pitches['pitch_name'] == 'Sinker']
fastballs = pitches.loc[pitches['pitch_name'] == '4-Seam Fastball']
changeups = pitches.loc[pitches['pitch_name'] == 'Changeup']
curveballs = pitches.loc[pitches['pitch_name'] == 'Curveball']
cutters = pitches.loc[pitches['pitch_name'] == 'Cutter']

fig = plt.figure(figsize=(10, 6))
fig.set_facecolor(BG_COLOR)

ax = fig.add_subplot(111, projection='3d')
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

ax.w_xaxis.line.set_color(FONT_COLOR)
ax.w_yaxis.line.set_color(FONT_COLOR)
ax.w_zaxis.line.set_color(FONT_COLOR)

def init():

    ax.scatter(sliders['release_speed'], sliders['pfx_x'], sliders['pfx_z'], marker=MARKER, s=POINT_SIZE, alpha=POINT_OPACITY, color=SLIDER_COLOR)
    ax.scatter(sinkers['release_speed'], sinkers['pfx_x'], sinkers['pfx_z'], marker=MARKER, s=POINT_SIZE, alpha=POINT_OPACITY, color=SINKER_COLOR)
    ax.scatter(fastballs['release_speed'], fastballs['pfx_x'], fastballs['pfx_z'], marker=MARKER, s=POINT_SIZE, alpha=POINT_OPACITY, color=FASTBALL_COLOR)
    ax.scatter(changeups['release_speed'], changeups['pfx_x'], changeups['pfx_z'], marker=MARKER, s=POINT_SIZE, alpha=POINT_OPACITY, color=CHANGEUP_COLOR)
    ax.scatter(curveballs['release_speed'], curveballs['pfx_x'], curveballs['pfx_z'], marker=MARKER, s=POINT_SIZE, alpha=POINT_OPACITY, color=CURVEBALL_COLOR)
    ax.scatter(cutters['release_speed'], cutters['pfx_x'], cutters['pfx_z'], marker=MARKER, s=POINT_SIZE, alpha=POINT_OPACITY, color=CUTTER_COLOR)

    ax.set_xticklabels(ax.get_xticklabels(), color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    ax.set_yticklabels(ax.get_yticklabels(), color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    ax.set_zticklabels(ax.get_yticklabels(), color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    ax.grid(False, color=FONT_COLOR, alpha=0.6)

    ax.set_xlabel('Speed (MPH)', color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    ax.set_ylabel('Horizontal Mov', color=FONT_COLOR, font=REGULAR_FONT_FAMILY)
    ax.set_zlabel('Vertical Mov', color=FONT_COLOR, font=REGULAR_FONT_FAMILY)

    ax.legend(
        ['Slider', 'Sinker', 'Fastball', 'Changeup', 'Curveball', 'Cutter'], 
        loc='upper left', 
        bbox_to_anchor=(1.15, 0.75), 
        facecolor=BG_COLOR,
        prop=BOLD_FONT_FAMILY
    )

    return fig,

def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,

# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=40, blit=True)
# Save
anim.save('output/Pitch Type Classification.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
