#!/usr/bin/env python
# coding: utf-8

# In[83]:


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# In[84]:


df = pd.read_csv('log_file.csv', header=None, names=[
                 'DateTime', 'Total_Time', 'Time_per_Sum'])


# In[85]:


df['DateTime'] = pd.to_datetime(df['DateTime'], format="%d-%m-%Y %H:%M")
df['DateTicks'] = df['DateTime'].dt.strftime('%d %b-%y')
df['Date'] = df['DateTime'].apply(lambda d: d.date())


# In[86]:


medians = df.groupby('Date')['Time_per_Sum'].median().sort_values()
color_palette = sns.color_palette("coolwarm_r", n_colors=len(medians))
color_dict = {median: color for median, color in zip(medians, color_palette)}


# In[106]:


_, ax = plt.subplots(1, 1, figsize=(10, 5))
sns.boxplot(x='Date', y='Time_per_Sum', data=df,
            palette=color_dict.values(), ax=ax)
ax.set_title(
    f'Two-Digit Addition Speed | Current: {round(df["Time_per_Sum"].iloc[-1],1)} sec')
ax.set_xticklabels(df['DateTicks'].unique(), rotation=90, fontdict = {'fontsize':6})

# Set the background color of the plot area
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', colors='gray')
ax.tick_params(axis='y', colors='gray')

# Set the facecolor of the figure
fig = plt.gcf()
fig.patch.set_facecolor('white')

# Set the grid lines
ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

# Add a gray boundary box for the plot area
for spine in ax.spines.values():
    spine.set_edgecolor('lightgray')
    spine.set_linewidth(1)

# Set the y-axis label
ax.set_ylabel('Time per sum (sec)')

# Save the figure as a PNG file
plt.savefig('boxplot.png', dpi=300, bbox_inches='tight')


# In[ ]:
