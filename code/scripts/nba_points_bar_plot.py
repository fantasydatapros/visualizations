import pandas as pd
import bar_chart_race as bcr
import warnings

warnings.filterwarnings('ignore')

df_weekly = pd.read_csv('data/nba_points_bar_plot.csv', index_col=0)

bcr.bar_chart_race(df=df_weekly, 
                   n_bars=15, 
                   sort='desc',
                   period_length=1000,
                   interpolate_period=False,
                   steps_per_period=10,
                   fixed_max=True,
                   filename='output/animations/NBA Points Bar Plot.mp4')