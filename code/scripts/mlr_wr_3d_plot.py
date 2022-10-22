import pandas as pd
import numpy as np
import matplotlib as mpl
from pathlib import Path

from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import matplotlib.pyplot as plt
import sklearn.linear_model

from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

#fonts to be used in the animation
REGULAR_FONT_FAMILY = Path(mpl.get_data_path(), "fonts/ttf/Exo-Regular.ttf")
BOLD_FONT_FAMILY = Path(mpl.get_data_path(), "fonts/ttf/Exo-Bold.ttf")
BG_COLOR = '#0f1f44'
FONT_COLOR = "#b3c1e1"
SECONDARY_COLOR = "#ffc331"
#set font colors to white in animations
mpl.rcParams['text.color'] = FONT_COLOR

df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2022/10-Machine%20Learning%20-%20Regression/1-Gridiron%20AI%20Curated%20Dataset%20-%202022.csv')

df = df.groupby(['player_id', 'tm', 'player', 'pos', 'season'], as_index=False)\
    .agg({
    'offensive_snapcount': np.sum,
    'offensive_snapcount_percentage': np.mean,
    'passing_rating': np.mean,
    'passing_yds': np.sum,
    'passing_td': np.sum,
    'passing_att': np.sum,
    'receiving_yds': np.sum,
    'receiving_td': np.sum,
    'receiving_rec': np.sum,
    'receiving_tar': np.sum,
    'rushing_att': np.sum,
    'standard_fantasy_points': np.sum,
    'ppr_fantasy_points': np.sum,
    'half_ppr_fantasy_points': np.sum
})

df = df.loc[(df['season'] >= 2012)]

pd.set_option('chained_assignment', None)

lag_features = ['rushing_att', 
               'receiving_tar', 
               'offensive_snapcount', 
               'offensive_snapcount_percentage',
                'ppr_fantasy_points',
                'passing_rating',
                'passing_att', 
                'passing_td']

for lag in range(1, 6):
    shifted = df.groupby('player_id').shift(lag)
    for column in lag_features:
        df[f'lag_{column}_{lag}'] = shifted[column]

df = df.fillna(-1)

wr_df = df.loc[(df['pos'] == 'WR') & (df['season'] < 2021)]
wr_df = wr_df.loc[wr_df['lag_offensive_snapcount_1'] > 50]

wr_df['lag_offensive_snapcount_norm'] = (wr_df['lag_offensive_snapcount_1'] - wr_df['lag_offensive_snapcount_1'].min()) / (wr_df['lag_offensive_snapcount_1'].max() - wr_df['lag_offensive_snapcount_1'].min())
wr_df['lag_receiving_tar_norm'] = (wr_df['lag_receiving_tar_1'] - wr_df['lag_receiving_tar_1'].min()) / (wr_df['lag_receiving_tar_1'].max() - wr_df['lag_receiving_tar_1'].min())

X = wr_df[['lag_receiving_tar_norm', 'lag_offensive_snapcount_norm']].values#, 'lag_ppr_fantasy_points_1']].values
y = wr_df['ppr_fantasy_points'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_train[:,0], X_train[:,1], y_train, marker='.', color=SECONDARY_COLOR)
ax.set_xlabel("Receiving Targets", font=REGULAR_FONT_FAMILY, color=FONT_COLOR)
ax.set_ylabel("Offensive Snapcount", font=REGULAR_FONT_FAMILY, color=FONT_COLOR)
ax.set_zlabel("PPR Fantasy Points", font=REGULAR_FONT_FAMILY, color=FONT_COLOR)
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

model = sklearn.linear_model.LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

coefs = model.coef_
intercept = model.intercept_
xs = np.tile(np.arange(2), (2,1))
ys = np.tile(np.arange(2), (2,1)).T
zs = xs*coefs[0]+ys*coefs[1]+intercept

def init():

    X = wr_df[['lag_receiving_tar_norm', 'lag_offensive_snapcount_norm']].values#, 'lag_ppr_fantasy_points_1']].values
    y = wr_df['ppr_fantasy_points'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)


    ax.scatter(X_train[:,0], X_train[:,1], y_train, marker='o', s=10, color=SECONDARY_COLOR, edgecolor=SECONDARY_COLOR)
    ax.set_xlabel("Receiving Targets")
    ax.set_ylabel("Offensive Snapcount")
    ax.set_zlabel("PPR Fantasy Points")

    model = sklearn.linear_model.LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    coefs = model.coef_
    intercept = model.intercept_
    xs = np.tile(np.arange(2), (2,1))
    ys = np.tile(np.arange(2), (2,1)).T
    zs = xs*coefs[0]+ys*coefs[1]+intercept

    ax.plot_surface(xs,ys,zs, alpha=0.2,color=FONT_COLOR)
    return fig,

def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,


# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)

anim.save('output/animations/MLR WR Output.mp4', fps=30, extra_args=['-vcodec', 'libx264'])