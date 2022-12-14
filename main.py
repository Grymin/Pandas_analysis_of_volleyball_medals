import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import seaborn as sns
pd.set_option('display.max_columns', None)

# url addresses
dfm_url = 'https://en.wikipedia.org/wiki/FIVB_Volleyball_Men%27s_World_Championship'

# reading html
dfm = pd.read_html(dfm_url, )[4]

# dropping nans
dfm.dropna(how='all', axis=0, inplace=True)
dfm.dropna(how='all', axis=1, inplace=True)

# Renaming columns - to deal with blank spaces in names on the website
dfm.columns = ['Year', 'Host', 'Pos1', 'G1score', 'Pos2', 'Pos3', 'G2score', 'Pos4', 'Teams']

# Delete " Details" from Year cells and set year as int
dfm.Year.replace('[a-zA-Z]', '', regex=True, inplace=True)
dfm.Year = dfm.Year.astype(int)

# set index
dfm.set_index('Year', verify_integrity=True, inplace=True)

# dropping cols which are not used
dfm.drop(labels=['Host', 'G1score', 'G2score', 'Teams', 'Pos4'], axis=1, inplace=True)

# Histogram of total medal places
dfm_melted = dfm.melt(var_name='position', value_name='country')
dfm_medals_tot = dfm_melted.country.value_counts().sort_index()
dfm_medals_tot.plot(kind='bar')
plt.title('TOTAL MEDALS')
plt.show()

# Histogram of individual medal places
medals_pos = dfm_melted.groupby(['country', 'position']).size().unstack(fill_value=0)
medals_pos.plot(kind='bar', stacked=True)
plt.title('MEDALS')
plt.show()

# Pivotted table
df_to_pivot = dfm.stack().reset_index()
df_to_pivot.columns = ['Year', 'Pos', 'Country']
df_pivoted = df_to_pivot.pivot(index='Country', columns='Year', values='Pos')
# remove 'Pos' from position
df_pivoted.replace('[a-zA-Z]', '', regex=True, inplace=True)
# names of columns - for sorting
cols = df_pivoted.columns.to_list()[::-1]
# sorting and filling nan
df_pivoted.sort_values(cols, inplace=True)
df_pivoted.fillna(np.nan, inplace=True)
df_pivoted = df_pivoted.astype(float)

# Heatmap
sns.set(rc={"figure.figsize": (8, 5)}) #width=3, #height=4
gold = (1.0, 0.84, 0.0, 1.0)
silver = (0.70, 0.70, 0.70, 1.0)
bronze = (0.6, 0.3, 0.0, 1.0)
myColors = (gold, silver, bronze)
cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))
ax = sns.heatmap(df_pivoted, cmap=cmap, linewidth=0.5, linecolor='gray', )
colorbar = ax.collections[0].colorbar
colorbar.set_ticks([1.33, 2.0, 2.67])
colorbar.set_ticklabels(['gold', 'silver', 'bronze'])
# changing size
ax.set_yticklabels(ax.get_yticklabels(), size=6)
ax.set_xticklabels(ax.get_xticklabels(), size=6)
plt.show()
