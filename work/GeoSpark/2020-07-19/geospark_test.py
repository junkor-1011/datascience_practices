#!/usr/bin/env python
# coding: utf-8

# GeoSpark Test
# =================
# 
# Ref:
# - https://datasystemslab.github.io/GeoSpark/tutorial/geospark-sql-python/

# In[1]:


from pyspark_utils import get_or_create_geospark_session
spark = get_or_create_geospark_session()
spark


# In[2]:


spark.sql("show databases").toPandas()


# In[3]:


import geopandas as gpd
# import pandas as pd


# prepare `japan_ver82` from [esri-japan](https://www.esrij.com/products/japan-shp/)

# In[4]:


gpdf = gpd.read_file('japan_ver82/japan_ver82.shp')
gpdf[:5]


# In[5]:


get_ipython().run_cell_magic('time', '', 'gdf = spark.createDataFrame(gpdf)\ngdf.show()\ngdf.dtypes')


# In[6]:


get_ipython().run_cell_magic('time', '', 'spark.sql("create database if not exists tmp")\nspark.sql("drop table if exists tmp.japan_ver82")\ngdf.write.saveAsTable("tmp.japan_ver82")')


# In[7]:


get_ipython().run_cell_magic('time', '', '# check\n_table = "tmp.japan_ver82"\nspark.table(_table).show(5)\ndisplay(spark.table(_table).limit(5).toPandas())\ndisplay(spark.table(_table).dtypes)\ndel _table')

