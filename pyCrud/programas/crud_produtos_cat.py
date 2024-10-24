import oracledb as orcl
import pandas as pd

def main():
    # abrir a conexão com o BD Oracle
    conexao,inst_SQL,str_autentic = conectar_BD()
    opc_principal = 0
    while (opc_principal != 5 and conexao==True):
        # menu principal
        print("1-Cadastro de Categorias")
        print("2-Cadastro de Produtos")
        print("3-Relatório de produtos por categoria")
        print("4-Relatório de produtos cujo preço de venda esteja entre 100.00 e 300.00")
        print("5-Sair")
        opc_principal = int(input("Digite a opção desejada (1 a 4): "))

        if (opc_principal == 1):
            opc_categoria = 0
            # submenu de categorias
            while (opc_categoria != 5):
                print("1-Inserção de categoria")
                print("2-Alteração de categoria")
                print("3-Exclusão de categoria")
                print("4-Relatório de todas as categorias")
                print("5-Voltar para o menu principal")
                opc_categoria = int(input("Digite a opção desejada para as categorias (1 a 5): "))

                # cadastro (crud) de categorias
                if (opc_categoria == 1):
                    descr_cat = input("Digite a descrição da categoria: ")
                    cat_qtde_estoque = 0

                    str_insert = f"""INSERT INTO categorias (CATEGORIA_DESCR,CATEGORIA_QTDE_ESTOQUE) VALUES ('{descr_cat}',{cat_qtde_estoque})"""

                    insert_tabela(inst_SQL,str_autentic,str_insert)
                elif (opc_categoria == 2):
                    lista_dados = []

                    id_categoria = int(input("Digite o id da categoria a ser alterada: "))

                    consulta = f"""SELECT * FROM categorias WHERE CATEGORIA_ID = {id_categoria}"""

                    inst_SQL.execute(consulta)

                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("ID da categoria não encontrado")
                    else:
                        try:
                            categoria_descr = input("Digite a nova descrição da categoria: ")
                            categoria_qtde_estoque = int(input("Digite a nova quantidade em estoque de produtos da categoria: "))
                        except ValueError:
                            print("Digite dados numéricos")
                        else:
                            str_update = f"""UPDATE categorias SET CATEGORIA_DESCR='{categoria_descr}',CATEGORIA_QTDE_ESTOQUE={categoria_qtde_estoque} WHERE CATEGORIA_ID={id_categoria}"""

                            update_tabela(inst_SQL,str_autentic,str_update)
                elif (opc_categoria == 3):
                    lista_dados = []

                    id_categoria = int(input("Digite o id da categoria a ser excluída: "))

                    consulta = f"""SELECT * FROM categorias WHERE CATEGORIA_ID = {id_categoria}"""

                    inst_SQL.execute(consulta)

                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("ID da categoria não encontrado")
                    else:
                        str_delete = f"""DELETE FROM categorias WHERE CATEGORIA_ID={id_categoria}"""
                        delete_tabela(inst_SQL,str_autentic,str_delete)
                elif (opc_categoria == 4):
                    # Exibir todas categorias
                    str_colunas = "SELECT column_name FROM all_tab_cols WHERE table_name = 'CATEGORIAS' AND OWNER = 'PF1633' "
                    str_consulta = "SELECT * FROM CATEGORIAS"

                    inst_SQL.execute(str_colunas)

                    dados = inst_SQL.fetchall()

                    colunas = []

                    for i in range(len(dados)):
                        colunas.append(dados[i][0].split("_")[1])
                    colunas = ['ID','DESCRICAO','QTDE ESTOQUE']
                    consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas)
        # cadastro (crud) dos produtos
        elif (opc_principal == 2):
            opc_produto = 0
            while (opc_produto != 5):
                print("1-Inserção de produto")
                print("2-Alteração de produto")
                print("3-Exclusão de produto")
                print("4-Relatório de todas os produtos")
                print("5-Voltar para o menu principal")
                opc_produto = int(input("Digite a opção desejada para os produtos (1 a 5): "))

                # cadastro (crud) de produto
                if (opc_produto == 1):
                    try:
                        produto_descr = input("Digite a descrição do produto: ")
                        produto_qtde_estoque = int(input("Digite a quantidade em estoque do produto: "))
                        produto_valor_compra = float(input("Digite o valor de compra do produto: "))
                        produto_valor_venda = float(input("Digite o valor de venda do produto: "))

                        # Exibir todas categorias para o usuario escolher uma a ser relacionada aoa produto
                        str_colunas = "SELECT column_name FROM all_tab_cols WHERE table_name = 'CATEGORIAS' AND OWNER = 'PF1633' "
                        str_consulta = "SELECT * FROM CATEGORIAS"

                        inst_SQL.execute(str_colunas)

                        dados = inst_SQL.fetchall()

                        colunas = []

                        for i in range(len(dados)):
                            colunas.append(dados[i][0].split("_")[1])

                        colunas = ['ID','DESCRICAO','QTDE ESTOQUE']
                        consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas)

                        lista_dados = []

                        id_categoria = int(input("Digite o id da categoria a ser vinculado ao produto: "))

                        consulta = f"""SELECT * FROM categorias WHERE CATEGORIA_ID={id_categoria}"""

                        inst_SQL.execute(consulta)

                        dados = inst_SQL.fetchall()

                        for dado in dados:
                            lista_dados.append(dado)

                        if (len(lista_dados) == 0):
                            print("O ID da categoria que está querendo vincular não existe")
                    except ValueError:
                        print("Digite dados numéricos")
                    else:
                        str_insert = f"""INSERT INTO PRODUTOS (PRODUTO_DESCR,PRODUTO_QTDE_ESTOQUE,PRODUTO_PRECO_COMPRA,PRODUTO_PRECO_VENDA,PRODUTO_CATID) VALUES ('{produto_descr}',{produto_qtde_estoque},{produto_valor_compra},{produto_valor_venda},{id_categoria})"""
                        insert_tabela(inst_SQL,str_autentic,str_insert)
                # update do produto
                elif (opc_produto == 2):
                    lista_dados = []

                    id_produto = int(input("Digite o id do produto a sere alterado: "))

                    consulta = f"""SELECT * FROM PRODUTOS WHERE PRODUTO_ID={id_produto}"""

                    inst_SQL.execute(consulta)

                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("O ID do produto a ser alterado não existe")
                    else:
                        try:
                            produto_descr = input("Digite a nova descrição do produto: ")
                            produto_qtde_estoque = int(input("Digite a nova quantidade em estoque do produto: "))
                            produto_valor_compra = float(input("Digite o novo valor de compra do produto: "))
                            produto_valor_venda = float(input("Digite o novo valor de venda do produto: "))

                            # Exibir todas categorias para o usuario escolher uma a ser relacionada aoa produto
                            str_colunas = "SELECT column_name FROM all_tab_cols WHERE table_name = 'CATEGORIAS' AND OWNER = 'PF1633' "
                            str_consulta = "SELECT * FROM CATEGORIAS"

                            inst_SQL.execute(str_colunas)

                            dados = inst_SQL.fetchall()

                            colunas = []

                            for i in range(len(dados)):
                                colunas.append(dados[i][0].split("_")[1])

                            colunas = ['ID','DESCRICAO','QTDE ESTOQUE']
                            consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas)

                            lista_dados = []

                            id_categoria = int(input("Digite o id da categoria a ser vinculado ao produto: "))

                            consulta = f"""SELECT * FROM categorias WHERE CATEGORIA_ID={id_categoria}"""

                            inst_SQL.execute(consulta)

                            dados = inst_SQL.fetchall()

                            for dado in dados:
                                lista_dados.append(dado)

                            if (len(lista_dados) == 0):
                                print("O ID da categoria que está querendo vincular não existe")
                        except ValueError:
                            print("Digite dados numéricos")
                        else:
                            str_update = f"""UPDATE PRODUTOS SET PRODUTO_DESCR='{produto_descr}',PRODUTO_QTDE_ESTOQUE={produto_qtde_estoque},PRODUTO_PRECO_COMPRA={produto_valor_compra},PRODUTO_PRECO_VENDA={produto_valor_venda},PRODUTO_CATID={id_categoria} WHERE PRODUTO_ID={id_produto}"""
                            update_tabela(inst_SQL,str_autentic,str_update)
                # exclusão do produto
                elif (opc_produto == 3):
                    lista_dados = []

                    id_produto = int(input("Digite o id do produto a ser excluído: "))

                    consulta = f"""SELECT * FROM PRODUTOS WHERE PRODUTO_ID={id_produto}"""

                    inst_SQL.execute(consulta)

                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("O ID do produto a ser alterado não existe")
                    else:
                        str_delete = f"""DELETE FROM PRODUTOS WHERE PRODUTO_ID={id_produto}"""
                        delete_tabela(inst_SQL,str_autentic,str_delete)
                # relatório de todos os produtos
                elif (opc_produto == 4):
                    str_consulta = "SELECT P.PRODUTO_ID,P.PRODUTO_DESCR,P.PRODUTO_QTDE_ESTOQUE,P.PRODUTO_PRECO_COMPRA,P.PRODUTO_PRECO_VENDA,C.CATEGORIA_DESCR FROM PRODUTOS P,CATEGORIAS C WHERE P.PRODUTO_CATID = C.CATEGORIA_ID"

                    colunas = ['ID','DESCRIÇÃO','QUANTIDADE ESTOQUE','PREÇO COMPRA','PREÇO VENDA','CATEGORIA']

                    consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas)
        # relatório de produtos por categoria
        elif (opc_principal == 3):
            # exibir as categorias
            str_colunas = "SELECT column_name FROM all_tab_cols WHERE table_name = 'CATEGORIAS' AND OWNER = 'PF1633' "
            str_consulta = "SELECT * FROM CATEGORIAS"

            inst_SQL.execute(str_colunas)

            dados = inst_SQL.fetchall()

            colunas = []

            for i in range(len(dados)):
                colunas.append(dados[i][0].split("_")[1])
            colunas = ['ID','DESCRICAO','QTDE ESTOQUE']
            consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas)

            # usuário vai escolher a categoria desejada
            id_categoria = int(input("Digite o id da categoria que deseja para gerar o relatório: "))

            # verficar se o id da categoria existe
            consulta = f"""SELECT * FROM categorias WHERE CATEGORIA_ID = {id_categoria}"""

            inst_SQL.execute(consulta)

            dados = inst_SQL.fetchall()

            for dado in dados:
                lista_dados.append(dado)

            if (len(lista_dados) == 0):
                print("ID da categoria não encontrado")
            else:
                # gerar o relatório dos produtos por categoria
                str_consulta = f"""SELECT P.PRODUTO_ID,P.PRODUTO_DESCR,P.PRODUTO_QTDE_ESTOQUE,P.PRODUTO_PRECO_COMPRA,P.PRODUTO_PRECO_VENDA,C.CATEGORIA_DESCR FROM PRODUTOS P,CATEGORIAS C WHERE P.PRODUTO_CATID = C.CATEGORIA_ID AND C.CATEGORIA_ID={id_categoria}"""

                colunas = ['ID','DESCRIÇÃO','QUANTIDADE ESTOQUE','PREÇO COMPRA','PREÇO VENDA','CATEGORIA']

                consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas)
        elif (opc_principal == 4):
                # gerar o relatório dos produtos cujo preço de venda esteja entre 100.00 e 300.00
                str_consulta = "SELECT P.PRODUTO_ID,P.PRODUTO_DESCR,P.PRODUTO_QTDE_ESTOQUE,P.PRODUTO_PRECO_COMPRA,P.PRODUTO_PRECO_VENDA,C.CATEGORIA_DESCR FROM PRODUTOS P,CATEGORIAS C WHERE P.PRODUTO_CATID = C.CATEGORIA_ID AND P.PRODUTO_PRECO_VENDA BETWEEN 100 AND 300"

                colunas = ['ID','DESCRIÇÃO','QUANTIDADE ESTOQUE','PREÇO COMPRA','PREÇO VENDA','CATEGORIA']

                consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas)


# Função para a conexão com BD oracle
def conectar_BD():

    # Abrir uma conexão com BD
    try:# tentativa de conexão com o BD
        str_dados_serv = orcl.makedsn("oracle.fiap.com.br","1521","ORCL")
        str_autentic = orcl.connect(user="PF1633",password="fiap23",dsn=str_dados_serv)

        inst_SQL = str_autentic.cursor()
    except Exception as e: # executa o except quando há falha de conexão
        print("Erro: ", e)
        conexao = False
        inst_SQL = ""
        str_autentic = ""
    else: 
        conexao = True

    return(conexao,inst_SQL,str_autentic)

# Função para inserir dados na tabela (insert)
def insert_tabela(inst_SQL,str_autentic,str_insert):
    try:
        inst_SQL.execute(str_insert)
        str_autentic.commit()
    except Exception as e: # executa o except quando há falha de conexão
        print("Erro: ", e)
    else:
        print("Dados inseridos com sucesso")
    

# Função para alterar dados na tabela (update)
def update_tabela(inst_SQL,str_autentic,str_update):
    try:
        inst_SQL.execute(str_update)
        str_autentic.commit()
    except Exception as e: # executa o except quando há falha de conexão
        print("Erro: ", e)
    else:
        print("Dados alterados com sucesso")


# Função para excluir dados da tabela (delete)
def delete_tabela(inst_SQL,str_autentic,str_delete):
    try:
        inst_SQL.execute(str_delete)
        str_autentic.commit()
    except Exception as e: # executa o except quando há falha de conexão
        print("Erro: ", e)
    else:
        print("Dados excluídos com sucesso")

# Função para gerar os relatórios
def consulta_tabela(inst_SQL,str_autentic,str_consulta,colunas):
    lista_dados = []

    inst_SQL.execute(str_consulta)

    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    dados_df = pd.DataFrame.from_records(lista_dados,columns=colunas,index='ID')

    if (dados_df.empty):
        print("Não há registros na tabela")
    else:
        print(dados_df)
        print("\n")


if (__name__ == "__main__"):
    main()
