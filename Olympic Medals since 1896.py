#!/usr/bin/env python
# coding: utf-8

# # Olympic medals 1896-2022 

# ## 1. Importing Libraries and loading data

# In[154]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pycountry


# ### Loading data from csv

# In[155]:


data_url="https://github.com/madrian98/OlimpicMedals/blob/main/Data/olympics_medals_country_wise.csv?raw=true"
data=pd.read_csv(data_url,thousands=',')


# ### Data information

# In[156]:


data.info()


# In[157]:


data.head()


# In[158]:


data.isna().sum()


# In[159]:


data.describe()


# ## 2. Data pre-processing

# In[160]:


#remove white spaces in column names
data.columns = [c.replace(' ', '') for c in data.columns]
#drop 'ioc code' column
data=data.drop(columns="ioc_code")
data.head()


# In[161]:


#countries to list
country_list = data['countries'].to_list()
#creating ISO country codes for each country (if exist) with usage of pycountry library
country_codes = {}
for country in country_list:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        country_code = country_data[0].alpha_3
        country_codes.update({country: country_code})
    except:
        country_codes.update({country: ' '})

#adding country code to dataframe for each coutnry
for c, i in country_codes.items():
    data.loc[(data['countries'] == c), 'iso_code'] = i 
data.head()


# ### Splitting data into 2 dataframes ( summer and winter olimpics )

# In[162]:


#summer
summer = data[['countries', 'iso_code', 'summer_participations', 'summer_gold', 'summer_silver', 'summer_bronze', 'summer_total']]
summer = summer.sort_values(by='summer_gold', ascending=False)
summer.head()


# In[163]:


#winter
winter = data[['countries', 'iso_code', 'winter_participations', 'winter_gold', 'winter_silver', 'winter_bronze', 'winter_total']]
winter = winter.sort_values(by='winter_gold', ascending=False)
winter.head()


# ## 3. Data visualisation

# ### 3.1 Olimpics participation

# In[164]:


cols = ['summer_participations','winter_participations','total_participation']
colors = ['reds', 'blues', 'thermal']
hovers=[[],[],[]]
lims = [(0, 30), (0, 30), (0, 60)]
labels = ['World summer olimpics participations','World winter olimpics participations', 'World total olimpics participations']
for i, l, h, j, _ in zip(cols, lims,hovers, range(len(colors)), labels):
    fig = px.choropleth(data_frame = data,locations= "iso_code", color= str(i),range_color=l,hover_name= "countries", hover_data=h,
                        color_continuous_scale= colors[j],labels={i:''},title=_)
    fig.update_layout(title_x=0.5)
    fig.show()


# ### Notes:
# - Dataset is strictly focused on olimpic medals.Countries without any medal scored in either summer&winter olimpic are excluded from it ,despite the fact , theirs athletes possibly have participated in olimpic events.

# ### 3.2 Olimpic medals

# In[165]:


colors = ['#C9B037','#D7D7D7','#6A3805']
legendnames = {'summer_gold':'Gold medal', 'summer_silver':'Silver medal','summer_bronze':'Bronze medal'}
summer=summer.head(10)
fig = px.bar(summer, x="countries", y=["summer_gold", "summer_silver", "summer_bronze"],title="Top summer olimpic countries", labels={
                     "value": "Medals count",
                     "countries": "Country name",
                     "variable": "Legend"
                 },color_discrete_sequence=colors)
fig.for_each_trace(lambda t: t.update(name = legendnames[t.name],
                                      legendgroup = legendnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, legendnames[t.name])
                                     )
                  )
fig.update_layout(title_x=0.5,
                 )
fig.show()


# In[166]:


colors = ['#C9B037','#D7D7D7','#6A3805']
legendnames = {'winter_gold':'Gold medal', 'winter_silver':'Silver medal','winter_bronze':'Bronze medal'}
winter=winter.head(10)
fig = px.bar(winter, x="countries", y=["winter_gold", "winter_silver", "winter_bronze"],title="Top winter olimpic countries", labels={
                     "value": "Medals count",
                     "countries": "Country name",
                     "variable": "Legend"
                 },color_discrete_sequence=colors)
fig.for_each_trace(lambda t: t.update(name = legendnames[t.name],
                                      legendgroup = legendnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, legendnames[t.name])
                                     )
                  )
fig.update_layout(title_x=0.5,
                 )
fig.show()


# In[167]:


data=data.sort_values(by='total_gold', ascending=False)
colors = ['#C9B037','#D7D7D7','#6A3805']
legendnames = {'total_gold':'Gold medal', 'total_silver':'Silver medal','total_bronze':'Bronze medal'}
data=data.head(10)
fig = px.bar(data, x="countries", y=["total_gold", "total_silver", "total_bronze"],title="Top olimpic countries", labels={
                     "value": "Medals count",
                     "countries": "Country name",
                     "variable": "Legend"
                 },color_discrete_sequence=colors)
fig.for_each_trace(lambda t: t.update(name = legendnames[t.name],
                                      legendgroup = legendnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, legendnames[t.name])
                                     )
                  )
fig.update_layout(title_x=0.5,
                 )
fig.show()

