from pathlib import Path

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

this_path = Path(__file__).parent.absolute()
df = pd.read_csv(this_path / 'database.csv')

# === PLOT 1 - POSICAO DOS EVENTOS (MAPA DO GLOBO INTERATIVO)
fig = go.Figure()
plot_configuration = {
    'Earthquake': {
        'color': 'rgb(0,0,255)'
    }, 
    'Nuclear Explosion': {
        'color': 'rgb(255,0,0)'
    }, 
    'Explosion': {
        'color': 'rgb(200,50,0)'
    }, 
    'Rock Burst': {
        'color': 'rgb(0,255,0)'
    },
    'Unknown': {
        'color': 'rgb(200,200,200)'
    }
}
for type_name, type_df in df.groupby('Type'):
    config = plot_configuration.get(type_name, plot_configuration['Unknown'])
    fig.add_trace(go.Scattergeo(
            lon = type_df['Longitude'],
            lat = type_df['Latitude'],
            text = type_df['Magnitude'],
            name = type_name,
            marker = dict(
                size = type_df['Magnitude']*1.2,
                color = config['color'],
                line_width = 1,
                opacity = 0.5
            )))
fig.show()

# === PLOT 2 - LOCALIZACAO DE TESTES NUCLEARES EM FUNCAO DO TEMPO
fig2 = px.scatter_geo(df[df["Type"]=="Nuclear Explosion"], lat="Latitude", lon="Longitude", 
                      color="Magnitude", range_color=[df['Magnitude'].min(),df['Magnitude'].max()],
                      hover_name="Magnitude", size="Magnitude",
                      animation_frame="Date",
                      projection="natural earth")
fig2.show()

# === PLOT 3 - PROFUNDIDADE EM FUNCAO DA COORDENADA DOS TERREMOTOS
filtro_terremoto = df['Type'] == 'Earthquake'
df_terremotos = df[filtro_terremoto]
df_terremotos.plot(  
    title="Profundidades",
    kind="scatter",
    x="Longitude", y="Latitude",
    alpha=0.3,
    figsize=(15,15),
    s=1.5,
    c="Depth",
    cmap=plt.get_cmap("jet"),
    colorbar=True,
    label="Depth"
)
plt.legend()
plt.show()

# === 
df.boxplot("Magnitude")
df.groupby("Magnitude Type").hist("Magnitude")
plt.show()