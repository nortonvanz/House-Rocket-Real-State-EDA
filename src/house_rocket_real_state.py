import pandas as pd
import streamlit as st
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster
import geopandas
import plotly.express as px
from datetime import datetime
from PIL import Image

# ============================================================================================================================================
    # DATA EXTRACTION
# ============================================================================================================================================
# Extract data
@st.cache(allow_output_mutation=True) # Speed up reading with cache
def get_data(path):
    data = pd.read_csv( path )
    return data

# Extract geofile
@st.cache( allow_output_mutation=True ) # Read geopandas file, used on Price Density Map
def get_geofile( url ):
    geofile = geopandas.read_file( url )
    return geofile

# ============================================================================================================================================
    # DATA TRANSFORMATION
# ============================================================================================================================================
st.set_page_config(	layout="wide")

c1, c2 = st.columns((1,3))
# image
with c1:
    photo = Image.open('house_rocket_img.jpg')
    st.image(photo, width=300)

#headers
with c2:
    HR_format = '<p style="font-family:sans-serif;' \
                'font-size: 50px;' \
                'font-weight: bold;' \
                'text-align: center;' \
                '"</p> House Rocket </p>'
    st.markdown(HR_format, unsafe_allow_html=True)
    HR_format = '<p style="font-family:sans-serif;' \
                'font-size: 30px;' \
                'font-weight: bold;' \
                'text-align: center;' \
                '"</p> Data Analysis </p>'
    st.markdown(HR_format, unsafe_allow_html=True)

# ========================================================================
# Usefull Functions Functions
# ========================================================================

def perc_diff(bigger, smaller):
    """ Calculates the percentual difference between two int or float numbers
    :param bigger: greater value
    :param smaller: smaller value
    :return: dif_perc  """
    dif_perc = round(((bigger - smaller) / smaller * 100), 2)
    return dif_perc

def set_feature ( data ):
    """ Converts sqft_lot in m2_lot
    :param data: dataset with column 'sqft_lot'
    :return: dataset with column 'price_m2'
    """""
    data['m2_lot'] = (data['sqft_lot'] / 10.764)
    data['price_m2'] = data['price'] / data['m2_lot']
    return data

# ========================================================================
# Create session: "Data Overview"
# ========================================================================
def overview_data( data ):
    # 1. Filtros dos imóveis por um ou várias regiões.
    # Objetivo: Visualizar imóveis por código postal (zipcode)
    # Obs: várias lat/lot neste dataset tem mesmo zipcode, logo podemos utilizar como agrupador de região.
    # Ação do Usuário: Digitar um ou mais códigos desejados.
    # A visualização: Uma tabela com todos os atributos e filtrada por código postal.

    # 2. Escolher uma ou mais variáveis para visualizar.
    # Objetivo: Visualizar características do imóvel.
    # Ação do Usuário: Digitar características desejadas.
    # A visualização: Uma tabela com todos os atributos selecionados.

# Filters: Overview -------------------------------------------------------

    st.sidebar.title('Data Overview')
    f_attributes = st.sidebar.multiselect('Enter Columns', data.columns)

    f_zipcode = st.sidebar.multiselect('Enter zipcode',
                                       data['zipcode'].unique())

    # Attributes + zipcode -> need rows and cols
    if (f_zipcode != []) & (f_attributes != []):
        # data_overview is used just for the first table
        data_overview = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
        # data is used for the other components that not first table
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

        # just zipcode -> just filter rows, all colums
    elif (f_zipcode != []) & (f_attributes == []):
        data_overview = data.loc[data['zipcode'].isin(f_zipcode), :]
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

        # just attributes -> just filter cols, all rows
    elif (f_zipcode == []) & (f_attributes != []):
        data_overview = data.loc[:, f_attributes]

        # no attributes -> returns original ds
    else:
        data_overview = data.copy()

# Table: Data Overview ----------------------------------------------------

    st.title('Data Overview')

    # Show all columns
    st.write(data_overview.head(), height=400)


# Table: Averages by Zip Code ---------------------------------------------

    # 3. Observar o número total de imóveis, a média de preço, a média da sala de estar e
    # também a média do preço por metro quadrado em cada um dos códigos postais.
    # Objetivo: Visualizar médias de algumas métricas por região.
    # Ação do Usuário: Digitar as métricas desejadas.
    # A visualização: Uma tabela com todos os atributos selecionados.

    # Create 2 columns with same size
    c1, c2 = st.columns((1, 1))

    # Average metrics
    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # Merge dataframes by zipcode
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')

    # Rename columns
    df.columns = ['zipcode', 'total houses', 'price', 'sqrt living, ', 'price/m2']

    # Show dataframe in c1 (left)
    c1.header('Averages by Zip Code')
    c1.dataframe(df, height=300)

# Table: Descriptive Attributes ----------------------------------------------

    # 4. Analisar cada uma das colunas de um modo mais descritivo.
    # Objetivo: Visualizar métricas descritivas (média, mediana, desvio padrão) de cada um dos atributos escolhidos.
    # Ação do Usuário: Digitar as métricas desejadas.
    # A visualização: Uma tabela com métricas descritivas por atributo.

    # Calculate descriptive metrics
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    # Concat columns on same dataframe
    df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()

    # Rename columns
    df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

    # Show dataframe in c2 (right)
    c2.header('Descriptive Attributes')
    c2.dataframe(df1, height=300)

    return None


# ========================================================================
# Create session: "Region Overview"
# ========================================================================
def portifolio_density ( data, geofile ):

    # 5. Uma mapa com a densidade de portfólio por região e também densidade de preço.
    # Densidade: concentração de alguma coisa.
    # Objetivo: Visualizar a densidade de portfólio no mapa, ou seja, o número de imóveis por região e por preço.
    # Ação do Usuário: Nenhuma ação.
    # A visualização: Um mapa com a densidade de imóveis por região.

    st.title('Region Overview')
    c1, c2 = st.columns((1, 1))

# Map: Portfolio Density ------------------------------------------------

    c1.header('Portfolio Density')
    df = data.head(500)

    # Base Map - Folium (empty map)
    density_map = folium.Map(location=[data['lat'].mean(),
                                       data['long'].mean()],
                             default_zoom_start=15)

    # Add points on map
    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      # card function, showing features:
                      popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(
                          row['price'],
                          row['date'],
                          row['sqft_living'],
                          row['bedrooms'],
                          row['bathrooms'],
                          row['yr_built'])).add_to(marker_cluster)
    # Plot map
    with c1:
        folium_static(density_map)


# Map: Price Density ----------------------------------------------------
    c2.header('Price Density')

    # Average price by zipcode
    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    # Rename columns
    df.columns = ['ZIP', 'PRICE']

    # Filter only dataset regions on geofile file
    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    # Creates base map
    region_price_map = folium.Map(location=[data['lat'].mean(),
                                            data['long'].mean()],
                                  default_zoom_start=15)

    # Plots density by color
    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',  # join com meus dados
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.3,  # 0.2
                                legend_name='AVERAGE PRICE ($)')
    # Plot map
    with c2:
        folium_static(region_price_map)

    return None


# ========================================================================
# Create session: "Commercial Attributes"
# ========================================================================
def commercial ( data ):

    st.title('Commercial Attributes')

# Line Graph: Average Price per Year Built ------------------------------

    # 6. Checar a variação anual de preço.
    # Objetivo: Observar variações anuais de preço.
    # Ação do Usuário: Filtra os dados pelo ano.
    # A visualização: Um gráfico de linha com os anos em x e preços médios em y.


# Filters
    st.sidebar.title('----------------- # ------------------')
    st.sidebar.title('Commercial Attributes')

    # Extract date
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # Filter - Average Price per Year Built
    min_year_built = int(data['yr_built'].min())
    max_year_built = int(data['yr_built'].max())

    st.sidebar.subheader('Average Price per Year Built')
    f_year_built = st.sidebar.slider('Min Year Built', min_year_built,
                                     max_year_built,
                                     min_year_built)  # default

    # Use filter data
    df = data.loc[data['yr_built'] >= f_year_built]

 # Graph
    st.header('Average Price per Year Built')

    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # Plot
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)


# Line Graph: Average Price per Day -----------------------------------

    # 7. Checar a variação diária de preço.
    # Objetivo: Observar variações diárias de preço.
    # Ação do Usuário: Filtra os dados pelo dia.
    # A visualização: Um gráfico de linha com os dias em x e preços médios em y.

# Filter
    st.sidebar.subheader('Average Price per Day')

    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Min Date', min_date, max_date, min_date)
    # st.write(type(data['date'][0]))

    data['date'] = pd.to_datetime(data['date'])

    # Use filter data
    df = data.loc[data['date'] >= f_date]

# Graph
    st.header('Average Price per Day')

    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # Plot
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    return None



# ========================================================================
# create session "House Attributes"
# ========================================================================
def attributes_distribuition ( data ):

    # 8. Conferir a distribuição dos imóveis (histograma) por:
    # - Preço;
    # - Número de quartos;
    # - Número de banheiros;
    # - Número de andares;
    # - Vista para a água ou não.
    # Objetivo: Observar a concentração dos imóveis por preço, quarto, banheiros, andares e vista para água..
    # Ação do Usuário: Filtro de preço, quarto, banheiro, andar e vista para água.
    # A visualização: Um histograma com cada atributo definido.

    st.title('House Attributes')

# Bar Graph: Price Distribuition -----------------------------------

# Filter
    st.sidebar.title('----------------- # ------------------')
    st.sidebar.title('House Attributes')
    st.sidebar.subheader('Price Distribution')

    # Range values
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())

    f_price = st.sidebar.slider('Max Price', min_price, max_price, max_price)

    # Data filtering
    df = data.loc[data['price'] <= f_price]

# Graph
    st.header('Price Distribution')

    # Plot
    fig = px.histogram(df, x='price', nbins=50)  # nbins = número de barras
    st.plotly_chart(fig, use_container_width=True)


# Bar Graph: Houses per Bedroom -------------------------------------
# Filter
    st.sidebar.subheader('Houses per Bedroom')

    # Get nd array unique bedrooms list
    unique_bedrooms = data['bedrooms'].unique()

    #Converts nd array to dict, and then to list to pass to index of selectbox:
    unique_bedrooms_list = list(dict(enumerate(unique_bedrooms.flatten(), 0)))

    # index sorted by the last key of dictionary (grater number)
    f_bedrooms = st.sidebar.selectbox('Max Number of Bedrooms', sorted(set(data['bedrooms'].unique())), index=list(unique_bedrooms_list).index( unique_bedrooms_list[-1] ) )

    #Graph
    c1, c2 = st.columns(2)

    c1.header('Houses per Bedroom')

    df = data[data['bedrooms'] <= f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

# Bar Graph: Houses per Bathroom ------------------------------------
#Filter
    st.sidebar.subheader('Houses per Bathroom')

    # Get nd array unique bathrooms list
    unique_bathrooms = data['bathrooms'].unique()

    # Converts nd array to dict, and then to list to pass to index of selectbox:
    unique_bathrooms_list = list(dict(enumerate(unique_bathrooms.flatten(), 0)))

    # index sorted by the last key of dictionary (grater number)
    f_bathrooms = st.sidebar.selectbox('Max Number of Bathrooms', sorted(set(data['bathrooms'].unique())), index=list(unique_bathrooms_list).index(unique_bathrooms_list[-1]) )

# Graph
    c2.header('Houses per Bathroom')

    df = data[data['bathrooms'] <= f_bathrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

# Bar Graph: Houses per Floor ---------------------------------------
# Filter
    st.sidebar.subheader('Houses per Floor')

    # Get nd array unique bathrooms list
    unique_floors = data['floors'].unique()

    # Converts nd array to dict, and then to list to pass to index of selectbox:
    unique_floors_list = list(dict(enumerate(unique_floors.flatten(), 0)))

    # index sorted by the last key of dictionary (grater number)
    f_floors = st.sidebar.selectbox('Max Number of Floors', sorted(set(data['floors'].unique())),index=list(unique_floors_list).index(unique_floors_list[-1]) )

# Graph
    c1, c2 = st.columns(2)

    c1.header('Houses per Floor')
    df = data[data['floors'] <= f_floors]

    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

# Bar Graph: Waterview ----------------------------------------------
# Filter
    st.sidebar.subheader('Waterview')
    f_waterview = st.sidebar.checkbox('Only Houses with Waterview')

    if f_waterview:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()

# Graph
    c2.header('Waterview')
    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)

    return None


# ========================================================================
# Create session "Business Recommendations" and "Buy Repport"
# ========================================================================

def buy_repport(data):

    st.title('Business Recommendations')

    st.header('Purchasing Recommendation Report')

# Problema de negócio 1: Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?

#Relatório
    # Confirmar que condição 5 é a melhor, validando a subida de preços por condição
    data[['condition', 'price']].groupby('condition').mean().reset_index()

    # Agrupar os imóveis por região ( zipcode )
    dfzip = data[['price', 'zipcode']].groupby('zipcode').median().reset_index()

    # Sugerir os imóveis que estão abaixo do preço mediano da região, que estejam em boas condições e tenham vista para água
    # Unir o dataframe dfzip com o data, pelo zipcode
    df2 = pd.merge(data, dfzip, on='zipcode', how='inner')

    # Renomear colunas do novo ds
    df2.rename(columns={'price_x': 'buy_price', 'price_y': 'median_price'}, inplace=True)  # to keep in the same df

    # Percorre valores e atribui para variável 'recommendation' a recomomendação: 'compra' ou 'não compra'
    df2['recommendation'] = 'NA'

    for i in range(len(df2)):
        if ( df2.loc[i, 'buy_price'] < df2.loc[i, 'median_price'] ) & ( df2.loc[i, 'condition'] >= 4 ) & ( df2.loc[i, 'waterfront'] == 1 ):
            df2.loc[i, 'recommendation'] = 'compra'
        else:
            df2.loc[i, 'recommendation'] = 'não compra'

    # Cria DS só com imóveis recomendados para compra:
    recom_buy = df2.loc[df2['recommendation'] == 'compra'].copy()

    # Cria coluna 'condition_status' para traduzir o que é cada uma 'condition'
    recom_buy['condition_status'] = "NA"
    recom_buy['condition_status'] = recom_buy['condition'].apply( lambda x: 'excelente' if x == 5 else "muito bom" if x == 4 else None )

    # Cria um relatório só com as informações relevantes
    rep_buy = recom_buy[['id', 'zipcode', 'buy_price', 'median_price', 'condition_status', 'recommendation', 'lat', 'long']]

    # Ressetar índices para estética no relatório
    rep_buy = rep_buy.reset_index(drop=True)

    # Exibe o relatório
    st.dataframe(rep_buy)

    st.header('Location of Recommended Properties:')

#Mapa
   # Cria e exibe um mapa com os imóveis recomendados para compra:
    houses = rep_buy[['id', 'lat', 'long', 'buy_price']]

    fig = px.scatter_mapbox(houses,
                            lat='lat',
                            lon='long',
                            size='buy_price',
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=15,
                            zoom=10)

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    # fig.show()
    st.plotly_chart(fig)

    return rep_buy

# ========================================================================
# Create sell "repport"
# ========================================================================

def sell_repport(data, recom_buy_ds):

    recom_buy = recom_buy_ds

    st.header('Sales Recommendation Report')

     # Problema de negócio 2: Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço ?

#Relatório

    # Criar coluna seasonality, definindo summer e winter:
    data['date_month'] = pd.to_datetime(data['date']).dt.month  # month (int)

    data['seasonality'] = "NA"
    data['seasonality'] = data['date_month'].apply(lambda x: 'winter' if (x == 12 or x <= 2) else 'summer' if (6 <= x <= 8) else "NA")

    # Keep just data on winter and summer
    data = data.loc[data['seasonality'] != 'NA']

    # Agora, confirmar se existe diferença de preço por sazonalidade.
    # Como só sugeri compra no zipcode 98070, vamos obter a mediana apenas naquele zipcode por sazonalidade:

    bouhgt = data.loc[data['zipcode'] == 98070] #hardcoded - only recommended to buy

    group_zips = (bouhgt[['price', 'seasonality']].groupby(['seasonality']).mean().reset_index())

    # Calcula a variação (mediana) de preço entre inverno x verão
    res_price_diff = perc_diff(group_zips['price'][1], group_zips['price'][0])
    # print(res_price_diff) #8.22 mais caro no inverno com relação ao verão

    # Atribui pra depois jogar no relatório
    winter_median_price = 537730.7692

    # Condições de venda:
    # 1 Se o preço da compra do imóvel for maior que a mediana da região + sazonalidade mais cara. O preço da venda será igual ao preço da compra + 10%
    # 2 Se meu preço da compra for menor que a mediana da região + sazonalidade mais cara. O preço da venda será igual ao preço da compra + 30%

    # Criar novo dataset unindo o ds de recomendação de compra e do de venda, pra poder calcular o lucro e ter o relatório final.
    # Temos no ds 'recom_buy' para o relatório: id, zipcode, median_price, buy_price(compra)
    # Obter:
    # -1 seasonality,
    # -2 preço da mediana da região
    # -3 preço venda,
    # -4 lucro

    # -1 seasonality,
    # Criar um novo ds de recomendação de venda:
    recom_sell = recom_buy.copy()
    # Recomendar vender no inverno, logo setar seasonality como 'winter'
    recom_sell['seasonality'] = 'winter'  # ok

    # -2 preço da mediana da região
    # O preço de venda na localização recomendada de compra no inverno, e setar no relatório como 'winter_median_price'
    recom_sell['winter_median_price'] = winter_median_price

    # Resetar índices para 0, 1, 2.. para percorrer laços na sequência.
    recom_sell = recom_sell.reset_index(drop=True)
    # print( recom_sell )

    # -3 preço venda
    # Analisar se podemos pedir 30% acima para ficar próximo à mediana como inicialmente pensado:
    #recom_sell[['buy_price', 'winter_median_price']]

    # Conferindo os percentuais de diferença entre o valor pago pelas casas e a mediana para o inverno no zipcode
    #for i in range(len(recom_sell)):
        # print( recom_sell.loc[i, 'winter_median_price'], recom_sell.loc[i, 'buy_price'] )
        #conf_diff = perc_diff(recom_sell.loc[i, 'winter_median_price'], recom_sell.loc[i, 'buy_price'])
        # print (conf_diff)

    # Vamos com base nestes percentuais: setar os 30% planejados sobre o valor pago como valor de venda:
    recom_sell['sale_price'] = 'NA'
    for i in range(len(recom_sell)):
        recom_sell.loc[i, 'sale_price'] = ((recom_sell.loc[i, 'buy_price'] * 30 / 100) + recom_sell.loc[i, 'buy_price'])

    # Confere o relatório agora com preço de venda
    # print( recom_sell)

    # -4 lucro
    recom_sell['profit'] = 'NA'
    for i in range(len(recom_sell)):
        recom_sell.loc[i, 'profit'] = (recom_sell.loc[i, 'sale_price'] - recom_sell.loc[i, 'buy_price'])

    # Cria relatório de vendas final:
    rel_sell = recom_sell[['id', 'zipcode', 'seasonality', 'winter_median_price', 'buy_price', 'sale_price', 'profit']]

    # Exibe o relatório
    st.dataframe(rel_sell)

    #Rodapé
    st.write(" \n\n"
                "Made by **Nórton Mattiello Vanz**"
                 " \n\n"
                "Details on my: "
                        "[GitHub](https://github.com/nortonvanz/House-Rocket-Real-State-EDA)"
                " \n\n"
                "Social media: [LinkedIn](https://www.linkedin.com/in/norton-vanz/)")

# ============================================================================================================================================

if __name__ == '__main__': #ETL:
# ============================================================================================================================================
    # DATA EXTRACTION
# ============================================================================================================================================
    # Extract data
    path = 'kc_house_data.csv'
    data = get_data(path)

    # Extract geofile
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    geofile = get_geofile( url )

# ============================================================================================================================================
    # DATA TRANSFORMATION
# ============================================================================================================================================
    # Create price per square meters ('price_m2')
    data = set_feature( data )

    # Create session: "Data Overview"
    overview_data( data )

    # Create session: "Region Overview"
    portifolio_density ( data, geofile )

    # Create session: "Commercial Attributes"
    commercial ( data )

    # Create session "House Attributes"
    attributes_distribuition ( data )

    # Create session "Business Recommendations" and "Buy Repport"
    recom_buy_ds = buy_repport(data)

    # Create sell "repport"
    sell_repport(data, recom_buy_ds)

# ============================================================================================================================================
    # DATA LOAD
# ============================================================================================================================================
    # No external loads



