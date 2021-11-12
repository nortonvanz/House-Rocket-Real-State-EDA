# House-Rocket-Real-State-EDA

<img src="https://github.com/nortonvanz/House-Rocket-Real-State-EDA/blob/main/src/house_rocket_img.jpg" width=70% height=70%/>

Projeto de Insights de uma empresa fictícia do ramo imobiliário.

Contextualização:
A House Rocket é uma plataforma digital, que tem como modelo de negócio a compra e a venda de imóveis através da internet.

## 1. Problema de negócios
### 1.1 Problema
Recentemente, as áreas de prespecção e de vendas da House Rocket receberam novas metas de desempenho. 
Ambas as áreas estão com dificuldades em cumpri-las, utilizando suas ferramentas tradicionais de trabalho.

### 1.2 Objetivo
Este projeto de insights tem por objetivo fornecer subsídios para a tomada de decisão aos dois times de negócios.  
Estima-se que após a entrega do projeto, a House Rocket possa obter aumento de 20 a 30% no seu lucro líquido.

### 1.3 Demandas de negócio

Produto de dados solicitado pelo time de prospecção: 
* Dashboard interativo do portfólio disponível, com todas informações de negócio mais relevantes disponíveis atualmente, para que possam realizar análises e melhorar sua prospecção.
   
Produto de dados solicitado pelo time de vendas: 
* Respostas para duas questões:
  - 1 - Quais são os imóveis que deveríamos comprar?
  - 2 - Uma vez o imóvel comprado, qual o melhor momento para vendê-lo, e por qual preço?

## 2. Premissas de negócio
- Será utilizado o critério de sazonalidade considerando inverno e verão na análise exploratório de dados. 
- Todos os produtos de dados entregues devem ser acessíveis via internet e também através de dispositivos móvies.
- O planejamento da solução será validado com os times de negócio, visando garantir que as soluções desenvolvidas são efetivas úteis na sua tomada de decisão.

As variáveis do dataset original são:

Variável | Definição
------------ | -------------
|id | Identificador de cada propriedade.|
|date | Data em que a propriedade ficou disponível.|
|price | O preço de cada imóvel, considerado como preço de compra.|
|bedrooms | Número de quartos.|
|bathrooms | O número de banheiros, o valor 0,5 indica um quarto com banheiro, mas sem chuveiro. O valor 0,75 ou 3/4 banheiro representa um banheiro que contém uma pia, um vaso sanitário e um chuveiro ou banheira.|
|sqft_living | Pés quadrados do interior das casas.|
|sqft_lot | Pés quadrados do terreno das casas.|
|floors | Número de andares.|
|waterfront | Uma variável fictícia para saber se a casa tinha vista para a orla ou não, '1' se a propriedade tem uma orla, '0' se não.|
|view | Vista, Um índice de 0 a 4 de quão boa era a visualização da propriedade.|
|condition | Um índice de 1 a 5 sobre o estado das moradias, 1 indica propriedade degradada e 5 excelente.|
|grade | Uma nota geral é dada à unidade habitacional com base no sistema de classificação de King County. O índice de 1 a 13, onde 1-3 fica aquém da construção e design do edifício, 7 tem um nível médio de construção e design e 11-13 tem um nível de construção e design de alta qualidade.|
|sqft_above | Os pés quadrados do espaço habitacional interior acima do nível do solo.|
|sqft_basement | Os pés quadrados do espaço habitacional interior abaixo do nível do solo.|
|yr_built | Ano de construção da propriedade.|
|yr_renovated | Representa o ano em que o imóvel foi reformado. Considera o número ‘0’ para descrever as propriedades nunca renovadas.|
|zipcode | Um código de cinco dígitos para indicar a área onde se encontra a propriedade.|
|lat | Latitude.|
|long | Longitude.|
|sqft_living15 | O tamanho médio em pés quadrados do espaço interno de habitação para as 15 casas mais próximas.|
|sqft_lot15 | Tamanho médio dos terrenos em metros quadrados para as 15 casas mais próximas.|

## 3. Planejamento da solução
### 3.1. Produto final 
O que será entregue efetivamente?
- Um grande dashboard interativo acessível via navegador, contendo os produtos de dados solicitados pelos times de negócio.
  
### 3.2. Ferramentas 
Quais ferramentas serão usadas no processo?
- Python 3.8.0;
- IDE PyCharm;
- Google Colab.   
  
### 3.3 Processo 
#### 3.3.1 Estratégia de solução
Minha estratégia para resolver esse desafio é:
1. Compreender o modelo de negócios;
2. Compreender o problema de negócios;
3. Coletar os dados;
4. Realizar a análise exploratória de dados;
5. Validar hipóteses e gerar insights;
6. Implantar o dashboard em produção.

#### 3.3.2 Detalhamento da solução
Produto de dados ao time de Prospecção: 
* Seções no dashboard interativo, contendo:
  * Lista contendo os imóveis do portfólio, e todas as suas características disponíveis. Deve conter filtro de variáveis desejadas para comparação.
  * Lista contendo média de preços e número de imóveis disponível em cada região (código postal). Deve conter filtro para uma ou várias regiões.
  * Lista contendo métricas descritivas (valor mínimo, máximo, médio, mediano, e desvio padrão) de cada variável disponível no portfólio.
  * Mapa de densidade do portfótio, exibindo o número de imóveis da região conforme o zoom aplicado no mapa.
  * Mapa de densidade de preços, exibindo o valor médio dos imóveis de cada região.
  * Gráfico interativo de preço médio por ano de construção, com filtro de ano de construção mínimo.
  * Gráfico interativo de preço médio por dia, para imóveis com registros de atualização de preços, com filtro de data mínima disponível.
  * Gráfico de distribuição de preços dos imóveis, com filtro de preços máximos.
  * Gráficos de distribuição do número de quartos, banheiros, andares e vista para a água, com a possibilidade de filtrar todos os valores existentes.
  
Produtos de dados ao time de Vendas:
* Seções no dashboard interativo, contendo:
  * Relatório de imóveis recomendados para compra, que se enquadrem nas seguintes condições:
    * 1 - Abaixo do preço mediano da sua região;
    * 2 - Em boas condições (Escala 1 à 5, somente classificações 4 e 5);
    * 3 - Apenas se tiverem vista para o mar.
  * Mapa exibindo a localização dos imóveis indicados para compra.
  * Relatório contendo a melhor sazonalidade para venda dos respectivos imóveis sugeridos para compra, e valor de venda recomendado. Estratégia:
    * 1 - Para cada região com imóveis sugeridos para compra, identificar a variação de preço médio por sazonalidade, para sugerir a venda na sazonalidade onde os valores são mais elevados.
    * 2 - Definição do preço de venda: Se o preço da compra do imóvel for maior que o preço médio da região + sazonalidade de maior preço, o preço da venda sugerido será igual ao preço da compra + 10%. 
                                        Se o preço da compra do imóvel for menor que o preço médio da região + sazonalidade de maior preço, o preço da venda sugerido será igual ao preço da compra + 30%.
   
## 4. Os 3 principais insights dos dados

#### 1 Imóveis com vista para o mar são, em média, 212.64% mais caros que os sem vista.
* Insight de negócio: Prospectar para compra imóveis com vista para o mar, quando estiverem com valor até 150% maior que imóveis sem vista na mesma região. Aliar outros critérios relevantes como o seu estado de conservação, para a tomada de decisão.

#### 2 Imóveis com data de construção menor que 1955, são em média apenas 0.79 % mais baratos que os após 1955.
* Insight de negócio: Prospectar imóveis com data de construção menor de 1955, que tenham passado por reformas, e que estejam com preço no mínimo 10% abaixo da média dos imóveis com ano de construção maior que 1955 na mesma região.

#### 3 Imóveis reformados na mesma região, tem preços em média 17.49 % maiores que imóveis não reformados.
* Insight de negócio: Prospectar imóvies reformados, onde o preço do imóvel seja até 5% maior que a média dos imóveis não reformados da região, nas mesmas condições.

## 5. Resultados financeiros para o negócio
De acordo com os critérios definidos, 5 imóvies foram sugeridos para a compra. 

Destes, todos apresentam condições de venda com 30% de margem na sazonalidade indicada. 

Mesmo com a margem citada, apenas um imóvel ultrapassa o preço da mediana de preços da região. Logo, é possível aumentar ainda mais a margem, conforme as demais características do imóvel. 

Considerando apenas os 30% de lucro por imóvel, o lucro total estimado caso as sugestões de compra e venda sejam seguidas é de aproximadamente $544 mil dólares.

## 6. Conclusão
O objetivo do projeto foi alcançado, dado que os produtos de dados propostos foram gerados com sucesso, e apresentados aos times de prospecção e de vendas. Os times já o utilizam agora para a tomada de decisão e o atingimento de metas na House Rocket.

O dashboard com os produtos de dados em produção pode ser acessado via navegador pelo [Heroku](https://house-rocket-eda.herokuapp.com/) 

## 7. Próximos passos
Melhorias nos dashboars podem ser incrementadas no futuro, avaliando algumas situações:
* Foram adotados altos critérios para sugestão dos imóveis para a compra (apenas notas 4 e 5, numa escala de 1 a 5). Uma grande quantidade de oportunidades pode existir nos imóveis com avaliações menores.
* Pode ser analisada se a distância do mar impacta proporcionalmente no preço dos imóveis, e se há oportunidades a partir desta análise.
* Pode ser estudado em que região há maior valorização de imóveis reformados, a fim de recomendar compra para reforma quando viável, considerando demais métricas de negócio como o estado do imóvel.

## 8 Referências
* Este Projeto de Insights é parte do curso "Python do Zero ao DS", da [Comunidade DS](https://www.comunidadedatascience.com/comunidade-ds/)
* O Dataset foi obtido no [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Os significados das variáveis foi obtido no [Geocenter](https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/)
* A imagem utilizada é de uso livre e foi obtida no [Pexels](https://www.pexels.com/)
