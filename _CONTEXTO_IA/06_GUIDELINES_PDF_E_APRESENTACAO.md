# 06 — Guidelines de PDF, figuras e apresentação

Vale para tudo que vira **relatório em PDF, slides, figuras e textos de interface** do projeto. As regras vêm do que o Gustavo usa no RecifeView (projeto da disciplina Projeto 5) e foram adaptadas ao AVD. O relatório e a apresentação são feitos pelo Claude Code, mas as **figuras e os textos que saem do notebook e do dashboard precisam seguir o mesmo padrão**, para o PDF não ficar com visuais diferentes.

> **Quem decide o conteúdo é o aluno.** Estas regras dizem *como* apresentar, nunca *o que concluir*. Título afirmativo de gráfico explanatório, mensagem do slide, nota analítica e resposta à pergunta de pesquisa são autorais. A IA formata, revisa e checa números.

## 1. Princípios
1. **O dado é o protagonista.** Fundo branco, texto preto, cor só onde se quer chamar a atenção. Se tudo tem cor, nada se destaca.
2. **Honestidade antes de impacto.** Diga o que o número é e o que ele não é. Mostre mediana quando a média engana, e avise quando houver faltante ou cobertura baixa (por exemplo, os zeros que escondem faltantes).
3. **Nenhum número inventado.** Todo número em figura, relatório ou slide vem de uma consulta reproduzível no notebook e informa **fonte, período e n**. Para este projeto: DrivenData/Taarifa, registros de 2002 a 2013, n = 59.400 (ou o n da amostra filtrada).
4. **Consistência.** A mesma classe tem a mesma cor em todo lugar, o mesmo termo tem o mesmo nome, e o mesmo número tem o mesmo formato.
5. **Quem lê tem pouco tempo.** O mais importante vem primeiro; o detalhe vem depois ou fica em apêndice.

## 2. Cores
- **Situação do ponto d'água (fixa em todas as figuras, no PDF e nos slides):** `functional` `#0072B2`, `functional needs repair` `#E69F00`, `non functional` `#D55E00`. É a paleta Okabe-Ito, legível por quem tem daltonismo.
- **Destaque por contraste:** a série ou categoria em foco em cor, e o resto em cinza (`#C6C6C6`). É o uso de atributo pré-atentivo que a rubrica cobra; a justificativa de qual atributo foi usado é do aluno.
- **A informação nunca depende só da cor:** use rótulo, posição ou padrão junto.
- **Texto sobre cor:** contraste de pelo menos 4,5:1 (3:1 em elementos gráficos).
- **Identidade visual (cor de marca, fonte, logo):** **ainda não decidida.** Não aplique a identidade do CESAR nem a do RecifeView sem o Gustavo confirmar. Enquanto isso: fundo branco, texto preto, uma família de fonte sem serifa e as cores acima.

## 3. Gráficos e tabelas
- Todo gráfico tem **título, eixos identificados, unidade e legenda** quando há mais de uma série. Abaixo dele vai a nota de fonte, período, filtros e n, em corpo pequeno e cinza.
- **Um gráfico, uma pergunta.** O título descreve o que se olha. Quando o gráfico é explanatório, o título pode afirmar a mensagem, mas **quem escreve a mensagem é o aluno**.
- Rótulo direto na barra ou na linha sempre que couber. Grade só horizontal e discreta. Eixo Y de barras começa em zero. Escala logarítmica só quando os dados pedirem, e com "escala log" escrito no eixo.
- **Não use:** pizza com mais de 3 fatias, rosca, gráfico 3D, gauge, eixo duplo e gradiente dentro de barra. Pizza e radar só com justificativa muito forte (regra do enunciado).
- Gráfico para pergunta: evolução no tempo, **linha**; ranking de categorias, **barra horizontal ordenada**; distribuição, **histograma ou boxplot** (nunca só a média); relação entre duas numéricas, **dispersão**; padrão entre duas categorias, **heatmap**; onde fica, **mapa**.
- Toda figura tem uma **alternativa em texto ou tabela**, e a figura é citada no texto do relatório ("Figura 3").
- Números em tabela alinhados à direita. Tabelas que listam colunas do dataset levam a coluna `significado` do `docs/GLOSSARIO.md`.

## 4. Texto e voz (relatório, slides e interface)
- Português do Brasil, direto, sem jargão desnecessário. Termos sempre iguais: ponto d'água, situação, região, `status_group`, classificador.
- Números no padrão pt-BR: `59.400`, `54,3%`, `19.287`. Datas `dd/mm/aaaa`; períodos `2002 a 2013`.
- **Sem travessão (—) nem meia-risca (–) em texto novo**: use vírgula, dois-pontos, parênteses ou ponto. O hífen comum continua valendo em palavras compostas, datas ISO e nomes de arquivo, e os valores do dataset (como `non functional`) ficam exatamente como são. **Exceção:** a marcação `# [IA] <ferramenta> – <finalidade>` do código segue o formato do enunciado, com a meia-risca. Texto antigo do repositório pode ter travessão; não precisa reescrever tudo.
- **Sem emoji** em relatório, slide, interface e mensagem de commit.
- **Sem frase de efeito e sem enchimento** ("insights poderosos", "transformando dados em decisões", "bem-vindo"). Sem texto genérico que serviria a qualquer dataset: cite as regiões, os tipos de bomba e as categorias reais.
- Prefira frases a listas com marcador em texto corrido. Pouco negrito.
- **Sem gradiente, glassmorphism, neon, fundo escuro "tech", sombra grande, ícone decorativo e ilustração genérica.**
- Dado fictício ou de exemplo nunca é apresentado como real. Se existir, vem marcado "dado fictício".

## 5. Relatório em PDF (`relatorio.pdf`, entregue até 26/11)
O enunciado pede "análise técnica completa de ambas as partes" e manda documentar: **decisões de tratamento dos dados, escolha de k, leitura da matriz de confusão, raciocínio do storytelling e resposta à pergunta de pesquisa**. Também exige, no mesmo pacote, `docs/DECLARACAO_IA.pdf` assinada por todos e a matriz de contribuição.
- Estrutura sugerida (o grupo pode mudar): resumo; pergunta de pesquisa e público-alvo; dados e fontes; EDA e qualidade dos dados (faltantes, mecanismo de ausência, outliers); tratamento e justificativas; storytelling e visualizações com as notas analíticas; classificador e métricas, se houver; Parte Comum (padronização, K-Means nas duas passadas, matriz, discussão crítica); limitações; referências; apêndices.
- Cada figura do relatório é um PNG de `out/` (gerado pelo notebook com `TEMA_ESCURO = False`), com legenda numerada e fonte.
- A **interpretação, a discussão crítica e as notas analíticas são do aluno**. A IA só ajuda a diagramar e a revisar ortografia e clareza.
- O relatório cita as definições do `docs/GLOSSARIO.md`, e os itens "a confirmar" precisam ser resolvidos ou ficar fora.

## 6. Apresentação (03/12)
- **Regras da arguição:** não há dataset surpresa; a professora pode escolher **duas variáveis do dataset** e pedir a interpretação da relação ao vivo; **qualquer integrante** pode ser questionado sobre **qualquer parte** (Comum ou Específica), com avaliação individual.
- Slides: uma mensagem por slide, figura grande, pouco texto, e o mesmo padrão de cores e números do relatório. Nada nos slides que não esteja no relatório.
- Preparar uma **colinha de variáveis** (o que cada coluna significa e como se relaciona com as outras), a partir do `docs/GLOSSARIO.md` e do esquema da seção 1.5 do `eda.ipynb`.
- Preparar o dashboard para demonstração ao vivo, com um plano B (capturas de tela) e o tempo de fala definido (o tempo total ainda não foi confirmado com a professora).
- Um documento de preparo com os trechos de código que podem ser questionados e as perguntas prováveis. Código que o grupo não sabe explicar na arguição **zera o projeto**.
