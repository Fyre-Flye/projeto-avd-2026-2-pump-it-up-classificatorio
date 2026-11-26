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
- **Identidade visual (cor de marca, fonte, logo):** definida na seção 2.1 abaixo (26/11/2026). Não aplique a identidade do CESAR (manual de marca da escola) nem logo nenhum sem o Gustavo pedir.

### 2.1 Identidade visual do projeto (decidida em 26/11/2026)
Segue o design system do RecifeView, que o Gustavo já usa na disciplina Projeto 5, com um ajuste: **as cores de situação do ponto d'água (seção 2) vêm antes de qualquer cor de marca.** Vale para o relatório, os slides, o dashboard e as figuras. É uma regra de **apresentação**: não decide o que concluir.

**Cores de marca (interface e texto, nunca no lugar da cor de situação)**

| Token | Hex | Uso |
| --- | --- | --- |
| azul-principal | `#0F62FE` | Títulos de destaque, botões, links, a série em foco em gráfico que **não** mostra a situação do ponto d'água |
| azul-claro | `#EAF2FF` | Fundo de cartão de apoio, barra lateral, faixa de filtros, linha selecionada |
| azul-marinho | `#062A5F` | Cabeçalho da capa, do slide de título e do dashboard |
| azul-escuro | `#0043CE` | Hover, foco e link visitado |
| preto | `#000000` | Texto principal |
| branco | `#FFFFFF` | Fundo da página; texto sobre azul |

**Neutros:** texto secundário `#525252`; rótulo de eixo e nota de fonte `#6F6F6F`; borda de campo `#8D8D8D`; série de contexto (fora de foco) `#C6C6C6`; linha de grade e borda de cartão `#E0E0E0`; fundo de tabela zebrada `#F4F4F4`.

**Aviso, sucesso e erro** (só para estado da interface, nunca como decoração): aviso texto `#8E6A00` sobre fundo `#FCF4D6`; erro `#DA1E28` sobre `#FFF1F1`; sucesso `#198038` sobre `#DEFBE6`.

**Como convivem marca e situação**
- Gráfico que mostra `status_group`: use **só** as três cores fixas da seção 2. O azul de marca não aparece nele, porque o azul de `functional` (`#0072B2`) e o azul de marca ficariam parecidos.
- Gráfico que mostra outra coisa (por exemplo, uma única série, ranking de regiões, importância das variáveis): série em foco em azul-principal e o resto em `#C6C6C6`.
- Mapa ou heatmap de uma só medida: escala sequencial de azuis `#EAF2FF`, `#A6C8FF`, `#4589FF`, `#0F62FE`, `#062A5F`, com "sem dado" em `#C6C6C6`. Se a medida for taxa de `non functional`, vale a escala laranja da situação já usada na EDA. Figuras já geradas e aprovadas não precisam ser refeitas só por causa da paleta.
- A cor laranja de seleção do RecifeView (`#FF832B`) **não** é usada aqui, porque se confunde com `functional needs repair` (`#E69F00`).

**Tipografia:** Montserrat (Google Fonts, pesos 400, 500, 600 e 700). Se não estiver disponível (matplotlib, Colab, Streamlit sem a fonte), use sans-serif genérica, sem mudar o resto do padrão. Nada em caixa alta corrida, exceto siglas. Números de tabela e de eixo alinhados à direita, com algarismos tabulares quando o meio permitir.

| Papel | Tamanho (dashboard) | Peso |
| --- | --- | --- |
| Título da página | 28 px | 700 |
| Título de seção | 20 px | 700 |
| Título de gráfico | 16 px | 600 |
| Corpo | 14 px | 400 |
| Subtítulo e descrição | 13 px | 400 |
| Legenda, eixo e nota de fonte | 12 px | 500 |
| Número de KPI | 32 px | 700 |

No PDF e nos slides, mantenha a mesma proporção entre os papéis (título maior que seção, seção maior que corpo), com o corpo do relatório entre 10 e 11 pt e o texto dos slides a partir de 18 pt.

**Forma e espaço**
- Espaçamento em múltiplos de 4 (4, 8, 12, 16, 24, 32, 48).
- Raio de 4 px em botão e campo, 8 px em cartão. Profundidade com borda de 1 px `#E0E0E0`, não com sombra. Sombra só em tooltip ou menu aberto, e discreta.
- Sem gradiente (inclusive em barra), vidro, neon, fundo escuro, ícone decorativo e ilustração genérica. Ícone só quando identifica uma ação ou um destino de navegação.

**Layout do dashboard (Streamlit)**
- Fundo branco; barra lateral em azul-claro; texto preto. No `.streamlit/config.toml`: `primaryColor = "#0F62FE"`, `backgroundColor = "#FFFFFF"`, `secondaryBackgroundColor = "#EAF2FF"`, `textColor = "#000000"`. Confira na documentação do Streamlit instalado como carregar a Montserrat; se não der, deixe `font = "sans serif"`.
- Filtros fixos no topo ou na barra lateral, sempre no mesmo lugar. No máximo 4 KPIs por tela. Telas com assuntos diferentes viram abas em vez de crescer para baixo.
- Cada gráfico traz o título, o texto `> Como ler` (pode ficar num expander) e, sempre visível, a nota de fonte, período e n. A **nota analítica** e a mensagem do gráfico explanatório continuam sendo autorais.
- Desenhe primeiro para tela de computador (1280 px ou mais) e garanta leitura em tablet. No celular basta que KPIs e tabelas sejam legíveis.

**Contraste:** azul-principal sobre branco é 5,0:1 (serve para texto de qualquer tamanho); sobre azul-claro cai para 4,4:1, então use azul-escuro nesse caso; branco sobre azul-principal é 5,0:1. Texto pequeno em `#B28600` ou em amarelo não passa: use preto ao lado de uma marca de cor.

**Logo:** o projeto não usa logo. Não insira o logo do RecifeView nem o do CESAR.

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
