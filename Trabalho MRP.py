import sqlite3
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

conn = sqlite3.connect('reservatorio.db')
cursor = conn.cursor()

# TABELA PRINCIPAL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservatorio (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        categoria TEXT,
        preco REAL,
        quantidade INTEGER,
        estoqueminimo INTEGER
    )
''')

# TABELA HISTÓRICO DE ESTOQUE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS historico_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produto INTEGER,
        periodo TEXT,
        quantidade INTEGER,
        FOREIGN KEY (id_produto) REFERENCES reservatorio(id_produto)
    )
''')
conn.commit()

def cadastro_produto():
    def validar_nome():
        while True:
            nome = input("Produto: ").strip().title()
            if nome:
                return nome
            else:
                print("Não pode deixar esse espaço em branco!")
    def validar_categoria():
        while True:
            tipo = input("Categoria: ").strip().title()
            if tipo:
                return tipo
            else:
                print("Não pode deixar esse espaço em branco!")
    def validar_preco():
        while True:
            try:
                valor = float(input("Preço Unitário: "))
                if valor <= 0:
                    print("O preço tem que ser um número real positivo!")
                else:
                    return valor
            except ValueError:
                print("O preço tem que ser um número real positivo!")
    def validar_quantidade():
        while True:
            try:
                qtd = int(input("Quantidade: "))
                if qtd < 0:
                    print("A quantidade não pode ser negativa!")
                else:
                    return qtd
            except ValueError:
                print("A quantidade tem que ser um número inteiro válido!")
    def validar_minimo():
        while True:
            try:
                estomin = int(input("Estoque Mínimo: "))
                if estomin < 0:
                    print("O estoque mínimo não pode ser negativo!")
                else:
                    return estomin
            except ValueError:
                print("O estoque mínimo tem que ser um número inteiro válido!")
    print("\n", "-"*10, "CADASTRO DE PRODUTO", "-"*10)
    nome = validar_nome()
    tipo = validar_categoria()
    valor = validar_preco()
    qtd = validar_quantidade()
    min = validar_minimo()

    cursor.execute('''
                   INSERT INTO reservatorio (nome,categoria,preco,quantidade,estoqueminimo)
                   VALUES (?,?,?,?,?)
                   ''', (nome, tipo, valor, qtd, min))
    conn.commit()
    id_produto = cursor.lastrowid
    print(f"Produto cadastrado com sucesso! ID: {id_produto}")

def excluir_produto():
    print("\n", "-"*10, "EXCLUIR PRODUTO", "-"*10)
    try:
        id_produto = int(input("Digite o ID do produto a ser excluído: "))
    except ValueError:
        print("Digite um ID válido!")
        return
    cursor.execute('SELECT nome FROM reservatorio WHERE id_produto = ?', (id_produto,))
    item = cursor.fetchone()
    if item:
        nome = item[0]
        confirmacao = input(f"Deseja realmente remover '{nome}' (ID: {id_produto})? (S/N): ").strip().upper()
        if confirmacao == 'S':
            cursor.execute('DELETE FROM reservatorio WHERE id_produto = ?', (id_produto,))
            cursor.execute('DELETE FROM historico_estoque WHERE id_produto = ?', (id_produto,))
            conn.commit()
            print("✓ Produto removido com sucesso!")
        elif confirmacao == 'N':
            print("Operação cancelada!")
        else:
            print("Digite uma operação válida.")
    else:
        print("Produto não encontrado!")

def relatorios():
    def listar_estoque():
        print("\n", "-"*10, "LISTAR ESTOQUE", "-"*10, "\n")

        cursor.execute('SELECT COUNT(*) FROM reservatorio')
        qtd_total = cursor.fetchone()[0]
        print(f"Quantidade de Produtos no Estoque: {qtd_total}\n")

        cursor.execute('SELECT * FROM reservatorio ORDER BY id_produto')
        produtos = cursor.fetchall()

        if not produtos:
            print("Não há produtos no estoque!")
            return

        print(f"{'ID':<5}{'NOME':<20}{'CATEGORIA':<15}{'PREÇO':<10}{'QTD':<8}{'MÍNIMO':<8}{'TOTAL':<12}{'STATUS':<5}")
        print("-"*70)

        for item in produtos:
            id_produto, nome, categoria, preco, quantidade, estoqueminimo = item
            total = quantidade * preco
            alerta = "⚠" if quantidade <= estoqueminimo else "✓"
            print(f"{id_produto:<5}{nome:<20}{categoria:<15}{preco:<10.2f}{quantidade:<8}{estoqueminimo:<8}{total:<12.2f}{alerta:<5}")

        print("-"*70)
    def atualizar_estoque():
        print("\n", "-"*10, "ATUALIZAR QUANTIDADE", "-"*10, "\n")
        try:
            id = int(input("Digite o ID do produto a ser atualizado: "))
        except ValueError:
            print("Digite um ID válido!")
            return

        cursor.execute('SELECT nome,quantidade FROM reservatorio WHERE id_produto = ?', (id,))
        produto = cursor.fetchone()

        if not produto:
            print(f"Produto com ID '{id}' não foi encontrado.")
            return

        nome, qtd_atual = produto
        print(f"\nProduto: {nome}")
        print(f"Quantidade Atual: {qtd_atual} unidades\n")

        try:
            print("\n", "-"*5, "Escolha uma Opção", "-"*5)
            print("1 - Adicionar Quantidade (Entrada)\n2 - Subtrair Quantidade (Saída)")
            opcao = int(input("Escolha uma opção: ").strip())
        except ValueError:
            print("Digite um número válido para a opção!")
            return

        try:
            match opcao:
                case 1:
                    qtd_somada = int(input("\nDigite a quantidade a ser adicionada: "))
                    if qtd_somada <= 0:
                        print("Quantidade a ser adicionada tem que ser positiva!")
                        return
                    nova_qtd = qtd_atual + qtd_somada
                    cursor.execute('UPDATE reservatorio SET quantidade = ? WHERE id_produto = ?', (nova_qtd, id))
                    conn.commit()
                    print(f"\n✓ {qtd_somada} unidades adicionadas!\nNova quantidade: {nova_qtd} unidades\n")
                case 2:
                    qtd_subtraida = int(input("\nDigite a quantidade a ser subtraída: "))
                    if qtd_subtraida <= 0:
                        print("Quantidade a ser subtraida tem que ser positiva!")
                        return
                    if qtd_subtraida > qtd_atual:
                        print(f"Não há estoque suficiente para retirar {qtd_subtraida} unidades.")
                        return
                    nova_qtd = qtd_atual - qtd_subtraida
                    cursor.execute('UPDATE reservatorio SET quantidade = ? WHERE id_produto = ?', (nova_qtd, id))
                    conn.commit()
                    print(f"\n✓ {qtd_subtraida} unidades removidas!\nNova quantidade: {nova_qtd} unidades\n")
                case _:
                    print("Digite uma opção válida!")
        except ValueError:
            print("Digite um número válido para a quantidade!")
    def estoque_baixo():
        print("\n", "-"*10, "PRODUTOS EM ESTOQUE BAIXO", "-"*10, "\n")
        cursor.execute('''
            SELECT id_produto, nome, categoria, preco, quantidade, estoqueminimo
            FROM reservatorio
            WHERE quantidade <= estoqueminimo
            ORDER BY id_produto
        ''')
        produtos_baixo = cursor.fetchall()

        if not produtos_baixo:
            print("Não há produtos abaixo do limite no estoque!")
            return

        print(f"{'ID':<5}{'NOME':<20}{'CATEGORIA':<15}{'PREÇO':<10}{'QTD':<8}{'MÍNIMO':<8}{'TOTAL':<12}")
        print("-"*80)

        for item in produtos_baixo:
            id_produto, nome, categoria, preco, quantidade, estoqueminimo = item
            total = preco * quantidade
            print(f"{id_produto:<5}{nome:<20}{categoria:<15}{preco:<10.2f}{quantidade:<8}{estoqueminimo:<8}{total:<12.2f}")
        print("-"*80)
        print("⚠ Atenção: Produtos com Estoque Baixo! ⚠")
    def contas():
        def giro_estoque():
            print("\n", "-"*10, "GIRO DE ESTOQUE", "-"*10, "\n")
            cursor.execute('SELECT id_produto, nome, quantidade FROM reservatorio ORDER BY id_produto')
            produtos = cursor.fetchall()

            if not produtos:
                print("Não há produtos cadastrados no estoque.")
                return

            vendas = {}
            for produto in produtos:
                id_produto, nome, _ = produto
                while True:
                    try:
                        qtd_vendida = int(input(f"Digite a quantidade vendida no período para '{nome}' (ID {id_produto}): "))
                        if qtd_vendida < 0:
                            print("Quantidade vendida não pode ser negativa. Tente novamente.")
                        else:
                            vendas[id_produto] = qtd_vendida
                            break
                    except ValueError:
                        print("Digite um número inteiro válido.")

            print("\nResultado do giro de estoque:\n")
            print(f"{'ID':<5}{'NOME':<20}{'QTD ESTOQUE':<15}{'QTD VENDIDA':<15}{'GIRO':<10}")
            print("-"*65)

            for produto in produtos:
                id_produto, nome, quantidade_estoque = produto
                qtd_vendida = vendas.get(id_produto, 0)
                giro = 0 if quantidade_estoque == 0 else qtd_vendida / quantidade_estoque
                print(f"{id_produto:<5}{nome:<20}{quantidade_estoque:<15}{qtd_vendida:<15}{giro:<10.2f}")
        def custo_manutencao():
            print("\n", "-"*10, "CUSTO DE MANUTENÇÃO DE ESTOQUE", "-"*10, "\n")
            while True:
                try:
                    taxa = float(input("Digite a taxa percentual do custo de manutenção (exemplo: 2 para 2%): "))
                    if taxa < 0:
                        print("Taxa não pode ser negativa. Tente novamente.")
                    else:
                        break
                except ValueError:
                    print("Digite um número válido para a taxa.")

            cursor.execute('SELECT id_produto, nome, preco, quantidade FROM reservatorio ORDER BY id_produto')
            produtos = cursor.fetchall()

            if not produtos:
                print("Não há produtos cadastrados no estoque.")
                return

            print("\nResultado do custo de manutenção:\n")
            print(f"{'ID':<5}{'NOME':<20}{'QTD':<10}{'PREÇO UNIT':<12}{'CUSTO MANUT':<15}")
            print("-"*50)

            for item in produtos:
                id_produto, nome, preco, quantidade = item
                custo_manut = preco * quantidade * (taxa / 100)
                print(f"{id_produto:<5}{nome:<20}{quantidade:<10}{preco:<12.2f}{custo_manut:<15.2f}")

            print("-"*50)
        def tempo_reposicao():
            print("\n", "-"*10, "TEMPO DE REPOSIÇÃO", "-"*10, "\n")
            cursor.execute('SELECT id_produto, nome FROM reservatorio ORDER BY id_produto')
            produtos = cursor.fetchall()

            if not produtos:
                print("Não há produtos cadastrados no estoque.")
                return

            tempos = {}
            for produto in produtos:
                id_produto, nome = produto
                while True:
                    try:
                        data_saida_str = input(f"Digite a data de saída do pedido para '{nome}' (ID {id_produto}) [dd/mm/aaaa]: ")
                        data_entrada_str = input(f"Digite a data de entrada no estoque para '{nome}' (ID {id_produto}) [dd/mm/aaaa]: ")
                        data_saida = datetime.strptime(data_saida_str, "%d/%m/%Y")
                        data_entrada = datetime.strptime(data_entrada_str, "%d/%m/%Y")
                        if data_entrada < data_saida:
                            print("Data de entrada não pode ser anterior à data de saída. Tente novamente.")
                        else:
                            tempo = (data_entrada - data_saida).days
                            tempos[id_produto] = tempo
                            break
                    except ValueError:
                        print("Formato de data inválido. Use dd/mm/aaaa.")

            print("\nResultado do tempo de reposição (dias):\n")
            print(f"{'ID':<5}{'NOME':<20}{'TEMPO DE REPOSIÇÃO (dias)':<25}")
            print("-"*50)

            for produto in produtos:
                id_produto, nome = produto
                tempo = tempos.get(id_produto, 0)
                print(f"{id_produto:<5}{nome:<20}{tempo:<25}")
        while True:
            print("\n", "-"*30, "SELECIONE UM RELATÓRIO GERENCIAL", "-"*30, "\n")
            print("1 - Giro de Estoque\n2 - Custo de Manutenção\n3 - Tempo de Reposição\n0 - Voltar")
            try:
                acao = int(input("Digite o relatório que deseja ver: "))
                match acao:
                    case 1:
                        giro_estoque()
                    case 2:
                        custo_manutencao()
                    case 3:
                        tempo_reposicao()
                    case 0:
                        return
                    case _:
                        print("Opção inválida! Digite uma ação válida.")
            except ValueError:
                print("Caractere inválido! Tente novamente.")

    def graficos():
        def grafico_evolucao():
            cursor.execute('''
                SELECT reservatorio.nome, historico_estoque.periodo, historico_estoque.quantidade
                FROM historico_estoque
                JOIN reservatorio ON historico_estoque.id_produto = reservatorio.id_produto
                ORDER BY reservatorio.nome, historico_estoque.periodo
            ''')
            dados = cursor.fetchall()

            if not dados:
                print("Não há dados históricos de estoque.")
                return

            dados_por_produto = defaultdict(list)
            for nome, periodo, qtd in dados:
                dados_por_produto[nome].append((periodo, qtd))

            plt.figure(figsize=(10, 6))
            for nome, valores in dados_por_produto.items():
                valores.sort(key=lambda x: x[0])
                periodos = [v[0] for v in valores]
                quantidades = [v[1] for v in valores]
                plt.plot(periodos, quantidades, marker='o', label=nome)

            plt.title('Evolução do Estoque ao Longo do Tempo')
            plt.xlabel('Período')
            plt.ylabel('Quantidade em Estoque')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        def grafico_comparativo():
            cursor.execute('SELECT categoria, SUM(quantidade) FROM reservatorio GROUP BY categoria')
            resultados = cursor.fetchall()

            if not resultados:
                print("Não há dados de categorias no estoque.")
                return

            categorias = [r[0] for r in resultados]
            quantidades = [r[1] for r in resultados]

            plt.figure(figsize=(8, 6))
            plt.bar(categorias, quantidades, color='skyblue')
            plt.xlabel('Categorias')
            plt.ylabel('Quantidade Total em Estoque')
            plt.title('Comparação de Estoque por Categoria')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        def curva_abc():
            cursor.execute('SELECT nome, preco, quantidade FROM reservatorio')
            produtos = cursor.fetchall()

            if not produtos:
                print("Estoque vazio.")
                return

            dados = [(nome, preco * qtd) for nome, preco, qtd in produtos]
            dados.sort(key=lambda x: x[1], reverse=True)

            total = sum([d[1] for d in dados])
            acumulado = []
            soma_cumulada = 0

            for nome, custo in dados:
                soma_cumulada += custo
                acumulado.append(soma_cumulada / total * 100)

            plt.figure(figsize=(10, 6))
            plt.plot(range(1, len(acumulado) + 1), acumulado, marker='o', linewidth=2)
            plt.axhline(y=80, color='r', linestyle='--', label='80% (Classe A)')
            plt.axhline(y=95, color='orange', linestyle='--', label='95% (Classe B)')
            plt.title('Curva ABC de Custos de Estoque')
            plt.xlabel('Itens ordenados por custo')
            plt.ylabel('Percentual acumulado do custo (%)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        while True:
            print("\n", "-"*30, "SELECIONE UM GRÁFICO", "-"*30, "\n")
            print("1 - Evolução de Estoque\n2 - Comparação de Categorias\n3 - Curva ABC de Custos\n0 - Voltar")
            try:
                acao = int(input("Digite o gráfico que deseja ver: "))
                match acao:
                    case 1:
                        grafico_evolucao()
                    case 2:
                        grafico_comparativo()
                    case 3:
                        curva_abc()
                    case 0:
                        return
                    case _:
                        print("Opção inválida! Digite uma ação válida.")
            except ValueError:
                print("Caractere inválido! Tente novamente.")

    while True:
        print("\n", "-"*40, "SELECIONE UMA AÇÃO", "-"*40, "\n")
        print("1 - Listar Estoque\n2 - Atualizar Estoque\n3 - Ver Estoque Baixo\n4 - Relatórios Gerenciais\n"
              "5 - Gráficos\n0 - Voltar ao Menu Principal")
        try:
            acao = int(input("Escolha uma ação: "))
            match acao:
                case 1:
                    listar_estoque()
                case 2:
                    atualizar_estoque()
                case 3:
                    estoque_baixo()
                case 4:
                    contas()
                case 5:
                    graficos()
                case 0:
                    print("-"*55, "VOLTANDO", "-"*55)
                    return
                case _:
                    print("Opção inválida! Digite uma ação válida.")
        except ValueError:
            print("Caractere inválido! Tente novamente.")

def menu():
    while True:
        print("\n", "="*30, "SISTEMA DE CONTROLE DE ESTOQUE", "="*30, "\n")
        print("1 - Cadastrar Produto\n2 - Excluir Produto\n3 - Relatórios de Produtos Cadastrados\n0 - Sair do Sistema")
        try:
            acao = int(input("Escolha uma ação: "))
            match acao:
                case 1:
                    cadastro_produto()
                case 2:
                    excluir_produto()
                case 3:
                    relatorios()
                case 0:
                    print("-"*30, "ENCERRANDO SISTEMA", "-"*30)
                    conn.close()
                    break
                case _:
                    print("Opção inválida! Digite uma ação válida.")
        except ValueError:
            print("Caractere inválido! Tente novamente.")

if __name__ == "__main__":
    menu()
