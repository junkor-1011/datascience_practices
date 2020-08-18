#!/usr/bin/env python
# coding: utf-8

# In[2]:


import osmnx as ox
import geopandas as gpd
import pandas as pd
import numpy as np


# In[7]:


get_ipython().run_cell_magic('time', '', 'cf = \'["highway"~"motorway|motorway_link"]\'\nG1 = ox.graph_from_place(\n    [\n        "Chiba, Japan",\n    ],\n    simplify=True,\n    custom_filter=cf,\n)\nG2 = ox.graph_from_place(\n    [\n        "Osaka, Japan",\n    ],\n    simplify=True,\n    custom_filter=cf,\n)')


# In[8]:


nodes1, edges1 = ox.graph_to_gdfs(G1)
nodes2, edges2 = ox.graph_to_gdfs(G2)

nodes = pd.concat([nodes1, nodes2])
edges = pd.concat([edges1, edges2])

display(nodes)
display(edges)


# In[11]:


edges2 = edges[['highway', 'length', 'geometry']].copy()


# In[12]:


edges2['highway'] = edges2['highway'].map(lambda x: None if type(x) == list else x)
edges2 = edges2.dropna()
edges2


# In[14]:


edges2.to_file("edges_highway/edges.shp")


# In[15]:


nodes[['highway', 'geometry']].to_file("nodes_highway/nodes.shp")


# In[16]:


get_ipython().system(' tar czvf edges_highway.tar.gz edges_highway')


# In[17]:


get_ipython().system(' tar czvf nodes_highway.tar.gz nodes_highway')

