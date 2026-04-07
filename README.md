# Estágio RFQ-Sirius Janeiro-Fevereiro 2026
## Objetivo:
O objetivo do estágio aqui relatado foi simular cavidades de radiofrequência para síncrotrons. Foi dado foco especial em uma cavidade TM-020 que atua com absorvedores de High-Order Modes [1], impedindo interferências indesejadas no feixe de elétrons.
## Estrutura do projeto:
### RFC_Maker:
O objetivo inicial deste repositório era guardar o RFC_maker, um gerador de arquivos de entrada para o Automesh criado para facilitar o processo de gerar geometrias diferentes para as simulações eletromagnéticas. O arquivo Maker.py contém a biblioteca responsável por essa função, podendo ser utilizada em scripts python utilizando o comando import Maker.
### Pillbox:
Neste diretório estão guardados os arquivos referentes aos testes realizados com pillbox, tais como cálculo analítico, e simulação de beampipe para os modos TM-010 e TM-020. Estão guardados também os testes que utilizam o parâmetro E0T como valor de campo elétrico. 
Há dois scripts principais que aparecem nos diretórios dessa seção: testes.py, que gera os arquivos de entrada do Autofish e calcula_tensao.py que calcula as figuras de mérito da simulação e as exibe em gráfico, estando nos subdiretórios Resultados.
### Simulação do Artigo:
Este diretório contém diferentes exemplos de arquivos de entrada e saída do Superfish para as diferentes geometrias testadas. 
### Cálculo de impedância
Neste diretório estão os testes associados ao cálculo da impedância das cavidades do artigo simuladas com ferrite e sem ferrite. 
