# trabalho-
Repositório com o trabalho MRP (Estoques)

🧾 Mini ERP de Estoque – Sistema de Cadastro de Produtos

Este projeto é um mini sistema de controle de estoque inspirado em módulos de ERP.
Ele foi desenvolvido para a atividade da disciplina, com foco em mostrar na prática conceitos de gestão de estoque e módulos de ERP.

🎯 Objetivo

Simular um módulo de estoque de um ERP, permitindo:

 - Cadastro de produtos
 - Exclusão de produtos
 - Movimentação de estoque (entrada e saída)
 - Relatórios gerenciais
 - Dashboard com gráficos de acompanhamento

Tudo isso rodando em modo texto, direto no terminal.

🧠 Conceitos de ERP e Gestão de Estoques abordados

O sistema foi pensado para refletir funcionalidades típicas de um módulo de estoque em ERP:

Cadastro de produtos

 - Nome
 - Categoria
 - Preço
 - Quantidade em estoque
 - Estoque mínimo

Movimentação de estoque

 - Entrada (aumenta a quantidade)
 - Saída (baixa estoque, com validação para não ficar negativo)

Relatórios gerenciais

 - Lista de produtos
 - Produtos com estoque baixo
 - Giro de estoque
 - Custo de manutenção de estoque
 - Tempo de reposição

Dashboards (gráficos)

 - Evolução do estoque ao longo do tempo
 - Comparação de estoque por categoria
 - Curva ABC de custos de estoque

🛠️ Tecnologias utilizadas

- Linguagem: Python

- Banco de dados: SQLite (sqlite3)

- Gráficos: Matplotlib (matplotlib.pyplot)

- Outras libs da própria linguagem:

   - datetime (datas e cálculo de tempo de reposição)

   - collections.defaultdict (organização de dados para gráficos)

📂 Estrutura básica do sistema

As principais partes do código são:

- Conexão e criação do banco (reservatorio.db)

- Tabela reservatorio: produtos cadastrados

- Tabela historico_estoque: histórico de quantidades por período (usado nos gráficos)

Função menu()

- Menu principal:

  - 1 Cadastrar produto

  - 2 Excluir produto

  - 3 Relatórios de produtos cadastrados

  - 0 Sair do sistema

Cadastro de produto

- Valida:

    - Nome

    - Categoria

    - Preço (real positivo)

    - Quantidade (inteiro ≥ 0)

    - Estoque mínimo (inteiro ≥ 0)

- Salva no banco de dados.

Exclusão de produto

  - Busca pelo ID

  - Confirma com o usuário antes de excluir

  - Remove também registros ligados no histórico de estoque.

Relatórios (relatorios())

  - Listar estoque (com total por item e alerta de estoque baixo)

  - Atualizar quantidade (entrada e saída)

  - Mostrar produtos com estoque abaixo do mínimo

  - Relatórios gerenciais:

    - Giro de estoque

    - Custo de manutenção

    - Tempo de reposição

Gráficos (graficos())

  - Evolução do estoque por produto (linha)

  - Comparação de categorias (barras)

  - Curva ABC de custos (linha com marcação de 80% e 95%)
