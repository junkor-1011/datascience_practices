#!/usr/bin/env python
# coding: utf-8

# GeoPandasによる全国市区町村界、都道府県界データの作成
# ===============================================
# 
# 例えばESRIジャパンの提供する全国市区町村界データは使いやすいもののArcGIS以外では使えないという使用規約になっている。
# 
# そこで、[国土数値情報](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html)のデータを使って近いものを再現する。
# 
# 
# **ToDo: Code Cleaning**
# 
# ## References
# 
# ### 手法の参考
# - https://hayatoiijima.jimdofree.com/2017/11/14/%E9%83%BD%E9%81%93%E5%BA%9C%E7%9C%8C%E5%A2%83%E3%81%AE%E3%81%BF%E3%81%AEshp%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9/
# - https://www.esrij.com/gis-guide/other-dataformat/free-gis-data/
# - http://xnissy.hatenablog.com/entry/20160205/1454666764
# - https://note.com/kinari_iro/n/nfee9bc97b6d7
# 
# ### データソース
# - [国土数値情報ダウンロード](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html)
# - [e-Stat](https://www.e-stat.go.jp/gis)
# - [全国市区町村界データ](https://www.esrij.com/products/japan-shp/)
#     - [ArcGIS](https://www.esrij.com/products/arcgis/)以外では使用不可

# In[1]:


import geopandas as gpd

display(gpd.__version__)


# - [国土数値情報](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html)から「全国, 世界測地系」のデータをダウンロード
#     - 例えば"N03-190101_GML.zip"などのファイル名
#     - 400MB近くある（年々増えてる?）ので注意

# In[2]:


gdf = gpd.read_file("data/N03-19_190101.shp")
gdf


# ## 市区町村界
# 
# - `N03_007`でdissolveする
#     - `N03_004`だと「中央区」や「北区」などで重複しそうなので
# - また、`N03_007`に関する欠損値も落としておく
#     - 全く異なる都道府県、市区町村同士のデータが結合してしまう可能性がある
# 
# Ref:
# - https://geopandas.org/aggregation_with_dissolve.html

# In[3]:


get_ipython().run_cell_magic('time', '', "gdf_dissolved = gdf.dropna(subset=['N03_007']).dissolve(by='N03_007')\ngdf_dissolved")


# - データ数的に大丈夫そうだが、一応描画して確認

# In[4]:


get_ipython().run_cell_magic('time', '', 'gdf_dissolved.plot()')


# ### 保存
# 
# Ref:
# - https://geopandas.org/io.html#writing-spatial-data
# 
# 

# #### shape

# In[21]:


get_ipython().system(' mkdir city_shape')


# In[5]:


get_ipython().run_cell_magic('time', '', 'gdf_dissolved.to_file("city_shape/shikuchousonkai.shp", encoding=\'utf-8\')')


# In[6]:


get_ipython().run_cell_magic('time', '', '\n# check\ngpd.read_file("city_shape/shikuchousonkai.shp")')


# #### GeoJSON

# In[7]:


get_ipython().run_cell_magic('time', '', 'gdf_dissolved.to_file("city_shikuchousonkai.geojson", driver="GeoJSON", encoding=\'utf-8\')')


# In[8]:


get_ipython().run_cell_magic('time', '', '\n# check\ngpd.read_file("city_shikuchousonkai.geojson")')


# #### geobuf
# 
# Ref:
# - [geobuf](https://github.com/pygeobuf/pygeobuf#usage)

# In[9]:


get_ipython().system(' pip install geobuf')


# In[10]:


import json
import geobuf


# In[11]:


pbf = geobuf.encode(
    json.loads(gdf_dissolved.to_json())
)


# In[13]:


get_ipython().run_cell_magic('time', '', 'with open("shikuchousonkai.buf", "wb") as f:\n    f.write(pbf)')


# In[14]:


gdf_prefecture = gpd.read_file("city_shape/shikuchousonkai.shp")

gdf_prefecture


# - データ量が多いので、もう少し間引く必要がありそう
#     - https://geopandas.org/geometric_manipulations.html#GeoSeries.simplify

# In[25]:


get_ipython().run_cell_magic('time', '', "gdf_prefecture2 = gdf_prefecture.copy()\ngdf_prefecture2['geometry'] = gdf_prefecture2['geometry'].simplify(tolerance=0.00085)\n\ngdf_prefecture2")


# In[26]:


get_ipython().run_cell_magic('time', '', 'gdf_prefecture2.plot()')


# In[27]:


get_ipython().run_cell_magic('time', '', 'gdf_prefecture2.to_file("city_shikuchousonkai_simple.geojson", driver=\'GeoJSON\', encoding=\'utf-8\')')


# In[28]:


get_ipython().run_cell_magic('time', '', 'gdf_prefecture2.to_file("city_shape_simple/shikuchousonkai.shp", encoding=\'utf-8\')')


# ## 都道府県界
# 
# 大元のデータを都道府県でdissolveしても良いが、市区町村界の結果を使う（未確認だが、計算量が減りそうな気がするので）

# In[29]:


gdf_prefecture2_dissolved = gdf_prefecture2.dissolve('N03_001')
gdf_prefecture2_dissolved


# In[30]:


gds = gdf_prefecture2_dissolved.copy().geometry

gds


# In[31]:


gds.plot()


# In[53]:


get_ipython().run_cell_magic('time', '', 'gds_simple = gds.simplify(tolerance=0.035,  preserve_topology=False)')


# In[54]:


gds_simple


# In[55]:


gds_simple.plot()


# In[57]:


gds_simple.to_file("prefecture.geojson", driver='GeoJSON')


# In[60]:


import folium
m = folium.Map()

folium.GeoJson(gds_simple.to_json()).add_to(m)
m.save("prefecture_test.html")


# - [prefecture_test.html](./prefecture_test.html)
# 
# 
# うまくsimplifyをしないと境界ががたつくので難しい

# -------
# 
# # make attribution
# 
# - [利用規約](https://nlftp.mlit.go.jp/ksj/other/agreement.html)に従う必要がある
# -　加工しているので、加工している旨は書かないといけない
# 
# Attribution Example:
# - <a href='https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html' target='_blank'>「国土数値情報(行政区域データ)」(国土交通省)</a>を元にして作成
# 

# In[ ]:




