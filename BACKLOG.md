# Backlog do projeto: contratos públicos de Portugal

Dados reais, empresa fictícia: somos o time de dados de uma organização de transparência.

Este é o documento com **todas as issues** do projeto. Cada secção `## USxx` vira uma issue no seu fork, durante a inicialização (`INIT.md`). Várias têm perguntas em aberto: responda no `clarify`, antes do plano.

## US00: Como engenheiro de dados, quero o ambiente pronto, para começar sem surpresas

- Labels: story, fundacao
- Depende de: nenhuma

### Contexto

Cada pessoa usa o próprio computador, fork e workspace.

### Critérios de aceite

- [ ] O verificador de ambiente informa todas as ferramentas como ok
- [ ] Login no GitHub e no Databricks funcionando
- [ ] O `gh` aponta para o meu fork
- [ ] Sei quais tabelas de sistema consigo consultar no meu workspace
- [ ] Nenhum token foi impresso, colado no chat ou salvo no repositório

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US01: Como engenheiro de dados, quero os contratos de um ano na bronze, para ter o dado bruto rastreável

- Labels: story, ingestao
- Depende de: US00

### Contexto

Fonte: contratos do Portal BASE publicados no dados.gov.pt. O endereço do arquivo vem da API do catálogo.

### Critérios de aceite

- [ ] O endereço do arquivo é obtido pela API do catálogo, sem estar fixo no código
- [ ] O arquivo original fica guardado em um Volume
- [ ] A bronze mantém todos os campos da fonte, sem alterar valores
- [ ] Cada carga registra origem, data da fonte e momento da ingestão
- [ ] A contagem da bronze é igual à do arquivo
- [ ] Rodar duas vezes não duplica dados
- [ ] Uma falha no download gera uma mensagem clara

### Perguntas em aberto (responder antes do plano)

- Uma nova publicação substitui o ano ou acrescenta?
- O arquivo descompactado é grande. Como ler sem esgotar a memória?
- Que ano carregar por padrão?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US02: Como analista, quero os códigos CPV na bronze, para classificar os contratos

- Labels: story, ingestao
- Depende de: US01

### Contexto

O dados.gov.pt publica uma lista de códigos CPV.

### Critérios de aceite

- [ ] O arquivo é obtido pela API do catálogo
- [ ] Há limite de tempo e número limitado de tentativas
- [ ] Há teste com uma resposta pequena gravada
- [ ] Rodar duas vezes não duplica dados

### Perguntas em aberto (responder antes do plano)

- Qual versão da lista usar e como saber que ela mudou?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US03: Como engenheiro de dados, quero carregar vários anos e recarregar quando a fonte mudar, para manter os dados atuais

- Labels: story, ingestao
- Depende de: US01

### Contexto

A fonte é republicada periodicamente.

### Critérios de aceite

- [ ] Os anos são um parâmetro
- [ ] Só baixa de novo se a data de modificação da fonte mudou
- [ ] A recarga de um ano não altera os outros
- [ ] Inclusões, alterações e remoções são contadas

### Perguntas em aberto (responder antes do plano)

- O identificador do contrato se mantém entre publicações? Como comprovar?
- Guardamos o histórico das versões?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US04: Como analista, quero contratos tipados e padronizados, para consultar com segurança

- Labels: story, silver
- Depende de: US01

### Contexto

A silver parte da bronze.

### Critérios de aceite

- [ ] Datas e valores têm tipos corretos
- [ ] Nomes de colunas seguem um padrão
- [ ] A chave do contrato está definida e testada
- [ ] Nenhuma linha desaparece sem explicação
- [ ] Há testes das transformações

### Perguntas em aberto (responder antes do plano)

- Qual é a chave? Como foi verificado?
- Um valor zero significa zero ou não informado?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US05: Como engenheiro de dados, quero expectations e quarentena, para saber o que está errado nos dados

- Labels: story, qualidade
- Depende de: US04

### Contexto

As regras devem vir da exploração dos dados, não de suposições.

### Critérios de aceite

- [ ] Há pelo menos uma regra que interrompe a carga, uma que separa registros e várias que apenas alertam
- [ ] Registros separados vão para uma quarentena com o motivo
- [ ] Cada regra tem teste
- [ ] A soma de silver e quarentena é explicável a partir da bronze

### Perguntas em aberto (responder antes do plano)

- Que problemas os dados realmente têm? Mostre as consultas.
- O que é erro e o que é apenas incomum?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US06: Como responsável por privacidade, quero as listas em tabelas sem expor pessoas físicas

- Labels: story, silver, privacidade
- Depende de: US04

### Contexto

Alguns campos trazem listas, como fornecedores, categorias e locais.

### Critérios de aceite

- [ ] Cada lista vira uma tabela ligada ao contrato
- [ ] As contagens conferem
- [ ] Itens que não puderam ser interpretados são contados
- [ ] Dados que possam identificar pessoa física são mascarados a partir da silver
- [ ] Um teste falha se esses dados vazarem
- [ ] As limitações do método de identificação estão documentadas

### Perguntas em aberto (responder antes do plano)

- Como reconhecer um possível dado de pessoa física? Quando a regra falha?
- Há dados pessoais em campos de texto livre?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US07: Como analista, quero a dimensão de categorias, para analisar o que se contrata

- Labels: story, silver
- Depende de: US02, US06

### Contexto

Liga os códigos dos contratos à lista CPV.

### Critérios de aceite

- [ ] Uma linha por código
- [ ] Códigos sem correspondência são contados e visíveis
- [ ] Há testes

### Perguntas em aberto (responder antes do plano)

- Agrupamos por qual nível do código?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US08: Como analista, quero o gasto mensal por entidade, para acompanhar a evolução

- Labels: story, gold
- Depende de: US06

### Contexto

Primeira tabela de negócio.

### Critérios de aceite

- [ ] O grão e a data de referência estão documentados
- [ ] A soma bate com a silver
- [ ] Contratos com várias entidades não são contados em dobro
- [ ] Há teste de conciliação

### Perguntas em aberto (responder antes do plano)

- Qual data define o mês?
- Como repartir um contrato com mais de uma entidade?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US09: Como analista, quero gastos por categoria, procedimento, fornecedor e região, para entender o que, como e onde se contrata

- Labels: story, gold
- Depende de: US07, US08

### Contexto

Tabelas que alimentam o app.

### Critérios de aceite

- [ ] A regra para várias categorias, fornecedores e locais está documentada
- [ ] Os totais conciliam
- [ ] Pessoas físicas não são expostas

### Perguntas em aberto (responder antes do plano)

- Ratear o valor ou escolher um item principal?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US10: Como engenheiro de dados, quero um job que rode tudo em ordem, para não executar passos à mão

- Labels: story, orquestracao
- Depende de: US05

### Contexto

Orquestra ingestão, pipeline e checagem.

### Critérios de aceite

- [ ] Ingestão, pipeline e checagem de qualidade em sequência
- [ ] O ano é um parâmetro
- [ ] A ingestão tem novas tentativas
- [ ] O job falha se um limite de qualidade for ultrapassado
- [ ] Em dev, a agenda fica pausada
- [ ] O job é definido no bundle

### Perguntas em aberto (responder antes do plano)

- Quais limites fazem o job falhar?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US11: Como engenheiro de dados, quero métricas operacionais em views, para monitorar sem consultar tabelas brutas

- Labels: story, observabilidade
- Depende de: US05, US10

### Contexto

Base do dashboard.

### Critérios de aceite

- [ ] Há views de qualidade, volume, ingestão e execuções
- [ ] As views são testadas ou conciliadas com uma execução conhecida
- [ ] A fonte e o atraso de cada métrica estão documentados

### Perguntas em aberto (responder antes do plano)

- Que tabelas de sistema estão disponíveis no meu workspace?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US12: Como engenheiro de dados, quero um dashboard de qualidade, para ver quais regras falham

- Labels: story, dashboard
- Depende de: US11

### Contexto

Público: engenheiros e administradores.

### Critérios de aceite

- [ ] Reprovações por regra ao longo do tempo
- [ ] Taxa de falha
- [ ] Quarentena por motivo
- [ ] Filtros por execução e tabela
- [ ] Dado ausente aparece como indisponível, não como zero

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US13: Como consumidor dos dados, quero um app com indicadores e análises, para entender a contratação pública

- Labels: story, app
- Depende de: US08, US09

### Contexto

Público: quem consome os dados.

### Critérios de aceite

- [ ] Visão geral, quem contrata, o que se contrata e como se contrata
- [ ] Cada indicador mostra definição, período, data da fonte e registros excluídos
- [ ] Nenhum valor é contado em dobro
- [ ] O app lê apenas a gold, com consultas parametrizadas
- [ ] Nenhum dado de pessoa física
- [ ] Linguagem neutra, sem sugerir irregularidade

### Perguntas em aberto (responder antes do plano)

- Quais indicadores respondem às perguntas do usuário?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US14: Como time, queremos deploy automático em dev, para publicar sem passos manuais

- Labels: story, deploy
- Depende de: US10, US12, US13

### Contexto

Pipeline, job, dashboard e app.

### Critérios de aceite

- [ ] No PR rodam lint, testes e validação do bundle
- [ ] No merge, o bundle é publicado em dev e o app é iniciado
- [ ] O fluxo confere se o app está rodando
- [ ] Nenhum segredo no repositório

### Perguntas em aberto (responder antes do plano)

- Que forma de autenticação funciona no meu workspace?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US15: Como cliente dos dados, quero ler a documentação num endereço web, para entender os dados sem instalar nada

- Labels: story, documentacao
- Depende de: US00

### Contexto

A documentação é escrita em Markdown no repositório e publicada como site.

### Critérios de aceite

- [ ] Páginas em português: início, fonte e licença, o que há nos dados, qualidade e limitações, indicadores, novidades
- [ ] Cada número tem origem e data; o que não existe aparece como planeado
- [ ] Site com menu e busca; `zensical build --clean --strict` passa
- [ ] Só `docs/cliente/` é publicado, sem material interno, endereços de workspace ou dados pessoais
- [ ] No PR o CI gera o site sem publicar
- [ ] No merge na `main` o CI publica no GitHub Pages
- [ ] O endereço abre em janela anônima, sem login nem instalação
- [ ] O README aponta para o endereço

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US16: Como engenheiro de dados, quero monitorar volume, ingestão e tempo de processamento, para perceber mudanças e lentidão

- Labels: story, dashboard
- Depende de: US11, US12

### Contexto

Complementa o dashboard de qualidade.

### Critérios de aceite

- [ ] Volume por tabela e execução
- [ ] Cada ingestão registra sucesso ou falha, tamanho, linhas e duração
- [ ] Mostra a idade do dado mais recente
- [ ] Duração do pipeline e das tarefas do job
- [ ] Os totais conferem com uma execução conhecida

### Perguntas em aberto (responder antes do plano)

- Que variação de volume merece atenção?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## US17: Como administrador, quero acompanhar o consumo de DBUs, para controlar o uso da plataforma

- Labels: story, dashboard, custo
- Depende de: US10

### Contexto

Usa as tabelas de sistema de faturação.

### Critérios de aceite

- [ ] DBUs por dia, produto e recurso do projeto
- [ ] Correções dos registros de uso entram na soma, com teste
- [ ] O custo é rotulado como estimativa a preço de lista
- [ ] A tela mostra até que momento há dados
- [ ] Sem acesso à fonte, mostra indisponível

### Perguntas em aberto (responder antes do plano)

- O que dá para atribuir a este projeto e o que é consumo partilhado?

### Definição de pronto

- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Pull request revisado

## Pedidos ainda sem história

Não viram issues na inicialização. Servem para praticar requisitos: escolha um e peça ao `requirements-analyst` para transformá-lo em história.

1. "Queremos saber se há muito ajuste direto."
2. "O diretor quer ser avisado quando os dados estiverem estranhos."
3. "Dá para ver quem são os maiores fornecedores?"
4. "Precisamos comparar este ano com o ano passado."
5. "O dashboard está bom, mas queria saber quanto estamos gastando."
