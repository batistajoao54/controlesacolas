import pandas as pd
import streamlit as st
import plotly.express as px
import openpyxl

st.set_page_config(layout = 'wide')

dados = st.sidebar.file_uploader("")

pagina = st.sidebar.checkbox('dados carregados')

if pagina == True:
    df = pd.read_excel(dados)
    df['QUANTIDADE'] = pd.to_numeric(df["QUANTIDADE"])
    
    lista_marca = df.MARCA.unique()
    
    #SELECIONANDO AS MARCAS
    cx_marca = st.sidebar.selectbox("Escolha uma MARCA!",lista_marca)
    
    df_marca = df[df['MARCA'] == cx_marca]
    
    lista_Os = df_marca.OS.unique()
    

    #SELECIONADO A OS
    cx_os = st.sidebar.selectbox("Selecione uma OS", lista_Os)
    df_os = df[df["OS"] == cx_os]

    df_total = df_os[df_os['STATUS'] == "TOTAL OS"]
            
    #SELECIONANDO O TOTAL DE SACOLAS ENVIADAS e recebidas POR OS
    df_base = df[df['OS'] == cx_os]
    df_base['QUANTIDADE'] = pd.to_numeric(df_base['QUANTIDADE'])
    df_recebido = df_base[df_base["STATUS"] == 'RECEBIDO']
    df_enviado = df_base[df_base['STATUS'] == 'ENVIADO']
    
    soma_enviado = df_enviado.copy()
    
    soma_recebido = df_recebido.copy()
    

    juncao = soma_enviado.groupby(["OS", "TAMANHO", "STATUS",]).sum().reset_index()
    juncao2 = soma_recebido.groupby(["OS", "TAMANHO", "STATUS",]).sum().reset_index()

    df_total_final = pd.concat([df_total,juncao,juncao2])
   
    c1,c,c2 = st.columns([1,0.2,1])

    with c1:
        fig_inicial = px.bar(df_total_final, x="OS", y="QUANTIDADE", color='STATUS',
                             barmode='group', height=400, width=400,
                             text_auto=True,
                             title=f"SACOLAS {df_total.iloc[0,4]} {df_total.iloc[0,5]} {df_total.iloc[0,6]}")

        st.plotly_chart(fig_inicial)


    with c2:
        df_dropidez = df_os[df_os['STATUS'] != "TOTAL OS"].copy()
        df_dropidez['QUANTIDADE'] = pd.to_numeric(df_dropidez['QUANTIDADE'])
        coladores = df_dropidez.groupby(["COLADOR", "MARCA", "TAMANHO", "COR", "OS", "STATUS",]).sum().reset_index()
        coladores_enviado = coladores[coladores["STATUS"] == "ENVIADO"]
        coladores_recebido = coladores[coladores["STATUS"] == "RECEBIDO"]
        
        novo_coladores = pd.concat([coladores_enviado, coladores_recebido])

        fig2 = st.checkbox("VER COLADORES")
        
        if fig2 == True:
            
            fig_final = px.bar(novo_coladores, x="COLADOR", y="QUANTIDADE",
                               color="STATUS", text_auto=True,
                               barmode="group", height=400, width=500,
                               title="COLADORES")

            st.plotly_chart(fig_final)

            #transformando os número em data
            df_data = df_dropidez.copy()
            df_data["DATA"] = f"{df_data.iloc[0,0]:.0f}-{df_data.iloc[0,1]:.0f}-{df_data.iloc[0,2]:.0f}"
            df_data_atual = df_data[df_data['COLADOR'] != "IDEZ"]
            lista_data = list(df_data_atual['COLADOR'].unique())
        
            registros = st.checkbox("Verificar tabelas")
        
            if registros == True:
                pesquisa = st.selectbox("Colador", lista_data)

                df_tabela = df_data_atual[['DATA',"COLADOR",'QUANTIDADE','STATUS','PAGO']]
            
                df_tabela_final = df_tabela[df_tabela['COLADOR'] == pesquisa]
                df_apresentacao = df_tabela_final[['DATA','QUANTIDADE','STATUS','PAGO']]
                st.table(df_apresentacao)
        
        
    st.header("Dados gerais de todas as OS ativas")
