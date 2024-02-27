import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


# First some MPG Data Exploration
st.cache_data #si fanno mettere i dati in una cache perchè streamline non è buono per i grandi dato e non conviene far caricare sempre i file
def load_data(path):
    df = pd.read_csv(path)
    return df


mpg_df_raw = load_data(path="./data/mpg.csv")#copiare i file nella cartella data prima di lanciare
#tutto quello che va nella cache non può più essere ricaricato e sovrascritto quindi non conviene lavorare su quello caricato, creiamo una copia
mpg_df = deepcopy(mpg_df_raw) 

# Add title and header
st.title("Introduction to Streamlit")#crea un titolo e un sottotitolo
st.header("MPG Data Exploration")
#per importare tabelle/dataframe--> st.table(data=mpg_df)
#per creare una tenda laterale con tutte le opzioni:
# --> st.sidebar.checknox("Show Dataframe")
if st.checkbox("Show Dataframe"):#pulsante per mostrare o meno la tabella
 st.subheader("This is my dataset")
 st.dataframe(data=mpg_df)#se uso dataframe più bello e compatto

#metofdo più avanzato per creare colonne, gli passo la lista con numero colonne con la larghezza
left_column, middle_column, right_column=st.columns([3,1,1])#la 1 colonna è 3 volte le altre di destra
#left_column,right_column=st.columns(2)#creo 2 colonne per mettere la barra dopo in una delle 2 colonne/divide la pagina in colonne

#facciamo un plot
years=['All']+sorted(pd.unique(mpg_df['year']))
year=left_column.selectbox("choose a year",years)#creo una tendina multipla con gli anni, quello che viene scelte viene passato come variabile year
#ho richiamato la colonna
show_means=middle_column.radio(label='Show Class Means', options=['Yes', 'No'])#bottone con 2 opzioi Yes e No

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

if year=='All':
   reduced_df=mpg_df
else:
   reduced_df=mpg_df[mpg_df['year']==year]

means=means = reduced_df.groupby('class').mean(numeric_only=True)

m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
if show_means == "Yes": #inserisco un vottone con yes or no per scegliere se visualizzare le medie
   ax.scatter(means['displ'], means['hwy'], alpha=0.7, color="red")
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

st.pyplot(m_fig)#per mostrare il grafico, come 

# aggiungo un grafico in  Plotly
p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers"))
    p_fig.update_layout(showlegend=False)

#Select which plot to show
if plot_type == "Matplotlib":
   st.pyplot(m_fig)
else:
   st.plotly_chart(p_fig)

#si possono aggiungere URL
#url="https://...."
#st.write("Data Source:",url)
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)


# Another header
st.header("Maps")

#per le mappe
st.subheader('Streamlit Map')
ds_geo=px.data.carshare()

#st.dataframe(ds_geo.head()) #per mostrare a schermo

#gli do le cordinate geografiche del dataframe
ds_geo['lat']=ds_geo['centroid_lat']
ds_geo['lon']=ds_geo['centroid_lon']

st.map(ds_geo)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

plotly_map = go.Figure(go.Choroplethmapbox(geojson=counties,
                                           locations=df.fips,
                                           z=df.unemp,
                                           colorscale="Viridis",
                                           zmin=0, zmax=12,
                                           marker={"opacity": 0.5, "line_width": 0}))
plotly_map.update_layout(mapbox_style="carto-positron",
                         mapbox_zoom=3,
                         mapbox_center={"lat": 37.0902, "lon": -95.7129},
                         margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(plotly_map)
