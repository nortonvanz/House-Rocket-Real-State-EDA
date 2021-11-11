# House-Rocket-Real-State-EDA

<img src="" width=70% height=70%/>

Projeto de Insights de uma empresa do ramo imobiliário.

Contextualização:
A House Rocket é uma plataforma digital fictícia, que tem como modelo de negócio a compra e a venda de imóveis através da internet.

## 1. Problema de negócios
Atualmente, as áreas de prespecção e de vendas da House Rocket não conseguem melhorar sua performance, visto que ainda não utilizam análise de dados de forma profissional.

Este projeto de insights tem por objetivo prover subsídios aos dois times de negócios, tendo como resultado o incremento de 10 a 30% no lucro da empresa.

Produto de dados ao time de prospecção: 
* O time de prespecção solicitou um dashboard interativo do portfólio disponível com as informações de negócio mais relevantes disponíveis atualmente, para que possam mehorar sua análise.
   
Produto de dados ao time de vendas: 
* O time de vendas solicitou respostas para duas questões:
  * 1 Quais são os imóveis que deveríamos comprar?
  * 2 Uma vez o imóvel comprado, qual o melhor momento para vendê-lo, e por qual preço?

## 2. Premissas de negócio
- Todos os imóvies do portfólio deven ser considerados, ou seja, nenhum registro será tratado como outlier.
- Será utilizado o critério de sazonalidade na análise exploratório de dados. Considera-se inverno os meses 06, 07 e 08, e verão os meses 12, 01 e 02.
- Todos os produtos de dados entregues devem ser acessíveis via internet e também através de dispositivos móvies.
- O planejamento da solução será validado com os times de negócio, visando garantir que as soluções desenvolvidas provém subsídio para tomada de decisão no dia a dia.

As variáveis do dataset original são:

Variable | Definition
------------ | -------------
|id | Identification number of each property|
|date | The date when the property was available|
|price | The price of each property considered as the purchase price |
|bedrooms | Number of bedrooms|
|bathrooms | The number of bathrooms, the value .5 indicates a room with a toilet but no shower. The value .75 or 3/4 bathroom represents a bathroom that contains one sink, one toilet, and either a shower or a bath.|
|sqft_living | Square feet of the houses interior space|
|sqft_lot | Square feet of the houses land space |
|floors | Number of floors|
|waterfront | A dummy variable for whether the house was overlooking the waterfront or not, ‘1’ if the property has a waterfront, ‘0’ if not|
|view | An index from 0 to 4 of how good the view of the property was|
|condition | An index from 1 to 5 on the condition of the houses, 1 indicates worn-out property and 5 excellent|
|grade | An overall grade is given to the housing unit based on the King County grading system. The index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 has a high-quality level of construction and design|
|sqft_above | The square feet of the interior housing space that is above ground level|
|sqft_basement | The square feet of the interior housing space that is below ground level|
|yr_built | Built year of the property |
|yr_renovated | Represents the year when the property was renovated. It considers the number ‘0’ to describe the properties never renovated.|
|zipcode | A five-digit code to indicate the area where the property is in|
|lat | Latitude|
|long | Longitude|
|sqft_living15 | The square feet average size of interior housing living space for the closest 15 houses|
|sqft_lot15 | The square feet average size of land lots for the closest 15 houses|

## 3. Planejamento da solução
3.1. Produto final (o que será entreque efetivamente?) 
Dois links para dashboars interativos na web, cada um contendo respostas aos problemas de negócio.
  
3.2. Ferramentas (quais ferramentas serão usadas no processo?) 
Python 3.8.0
IDE PyCharm
Google Colab   
  
3.3 Processo (quais os passos necessários para alcançar meu objetivo?)

Produto de dados ao time de Prospecção: 
* Dashboar interativo contendo:
  * Amostra de todas as características exitentes dos imóveis.
  * Média de preços e número de imóveis disponível em cada região (código postal). Deve conter filtro que permita selecionar apenas as regiões  disponíveis.
  * Métricas descritivas (valor mínimo, máximo, médio, mediano, e desvio padrão) de cada característica disponível no portfólio.
  * Mapa de densidade do portfótio, exibindo o número de imóveis da região conforme o zoom aplicado no mapa.
  * Mapa de densidade de preços, exibindo o valor medio dos imóveis de cada região.
  * Gráfico interativo de preço médio por ano de construção, com filtro de ano de construção.
  * Gráfico interativo de preço médio por dia, para imóveis com registros de atualização de preços, com filtro de datas disponíveis.
  * Distribuição de preços dos imóveis, com filtro de preços máximos.
  * Distribuição do número de quartos banheiros, andares e vista para a água, com seus os respectivos filtros.

Produto de dados ao time de vendas:
* Relatório contendo imóveis sugeridos para compra. 
Serão sugeridos imóveis que se enquadrem nas seguintes condições:
   * 1 - Abaixo do preço mediano da sua região;
   * 2 - Em boas condições (Escala 1 à 5, somente classificações 4 e 5);
   * 3 - Apenas se tiverem vista para o mar.

* Relatório contendo a melhor sazonalidade para venda dos respectivos imóvies sugeridos para compra, e valor de venda recomendado.
    * Isto será obtido através da identificação das diferenças de preço médio por sazonalidade (inverno e verão), para sugestão de venda na melhor sazonalidade.
   Se o preço da compra do imóvel for maior que a média da região + melhor sazonalidade, o preço da venda sugerido será igual ao preço da compra + 10%.
   Se o preço da compra do imóvel for menor que a média da região + melhor sazonalidade, o preço da venda sugerido será igual ao preço da compra + 30%.
   
## 4. Os 3 principais insights dos dados
Insight 1: 
Imóveis com vista para o mar são, em média, 212.64% mais caros que os sem vista.
Recomendação de negócio: Prospectar para compra imóveis com vista para o mar, quando estiverem com valor até 150% mais caros em relação aos sem vista na mesma região, visto que em média ainda haverá boa margem para venda. Aliar outros critérios como sua classificação (estado de conservação) para a tomada de decisão.

Insight 2: 
Imóveis com data de construção menor que 1955, são em média apenas 0.79 % mais baratos que os após 1955.
Recomendação de negócio: Prospectar imóveis com data de construção menor de 1955, que tenham passado por reformas, e que estejam com preço no mínimo 20% abaixo da média dos imóvies com ano de constução maior que 1955.

Insight 3:
Imóveis reformados no mesmo zipcode tem preço em média: 17.49 % maior que imóveis não reformados.
Recomendação de negócio: Prospectar imóvies reformados onde o preço médio da região seja igual ou menor que o do imóvel, nas mesmas condições.

## 5. Resultados financeiros para o negócio
Foram sugeridos inicialmente para a compra 5 imóvies. Destes, todos apresentam condições de venda com 30% de margem na sazonalidade indicada, e apenas um ultrapassa o preço da mediana de preços da região. Logo, é possível aumentar ainda mais esta margem conforme as demais características do imóvel como estado e metragem quadrada. 

Considerando apenas os 30% de lucro por imóvel, o lucro total estimado seria de $544.347.

## 6. Conclusão
O objetivo do projeto foi alcançado, dado que os produtos de dados proportos forma gerados com sucesso, e podem ser utilizados pelos times de prospecção e vendas para a tomada de decisões. 
Na proporção dos resultados obitdos através da tomadas de decisão baseadas em dados, o projeto contribuiu significativamente para o aumento do faturamento da empresa, e novos insights podem ser gerados através de novas análises. 

** 7. Próximos passos**
Outras análises podem ser realizadas no futuro, como por exemplo:
* Foram adotados altos critérios a respeito do estado dos imóvies para a compra (apenas nota 4 e 5, numa escala de 1 a 5). Uma grande quantidade de oportunidades pode existir nos imóveis com avaliações menores.
* Pode ser analisada se a distância do mar impacta proporcionalmente no preço dos imóveis, e se há oportunidades a partir dos resultados.
* Pode ser estudado em que região há maior valorização de imóveis reformados, e comprar para reforma caso haja viabilidade, aliado a demais métricas como estado do imóvel.

** 8 Referências
* Este Projeto de Insights é parte do curso "Python do Zero ao DS", da [Comunidade DS](https://www.comunidadedatascience.com/comunidade-ds/)
* O Dataset está disponível no [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Significados das variáveis está disponível no [Geocenter](https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/)
* A imagem utilizada é de uso livre e foi obtida no [Pexels](https://www.pexels.com/)
