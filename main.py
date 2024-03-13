import pandas as pd
import streamlit as st
from despesas import get_despesas, mostrar_despesas
from graficos import criar_grafico_barras

#PRIMEIRO FAÇA O UPLOAD DA PLANILHA https://docs.google.com/spreadsheets/d/1xw8bydqh0v4zlsuchqzB3JiSNMt1sYQjIHhN-3pbLNA/edit?usp=sharing
# EM FORMATO CSV
# renomei-e a mesma como "dados.csv"
@st.cache_data()
def load_data(file_path):

    data = pd.read_csv(file_path, skiprows=7)
    #tratamento para substituir traços por zeros
    data[['Empenhado', 'Liquidado', 'Pago', 'RP Pago', 'Despesa Executada']] = data.loc[:, ['Empenhado', 'Liquidado', 'Pago', 'RP Pago', 'Despesa Executada']].map(lambda x: x.strip().replace('.', '').replace(',','.').replace(' ', '')) \
    .replace('-', '0').astype(float, errors='ignore')
    return data

def main():



    st.set_page_config(layout="wide", page_title="Análise custos em Saúde")
    st.sidebar.image('./image.png')
        
    uploaded_file = st.file_uploader("Choose a file")

    st.text('download https://docs.google.com/spreadsheets/d/1xw8bydqh0v4zlsuchqzB3JiSNMt1sYQjIHhN-3pbLNA/edit?usp=sharing')

    st.title("Análise custos em Saúde")
    
    
    if uploaded_file is not None:
        
        data = load_data(uploaded_file)
    
        with st.sidebar:
            st.title("Filtros")

            selected_regiao = st.sidebar.selectbox('Filtrar por Região', ['Todas as Regiões'] + list(data['Região'].unique()))
            selected_uf = st.sidebar.selectbox('Filtrar por UF', ['Todas as UF'] + list(data['UF'].unique()))
            selected_ano = st.sidebar.selectbox('Filtrar por Ano', ['Todos os anos'] + list(data['Ano'].unique()))
            selected_subfunco = st.sidebar.selectbox('Filtrar por subfuncao', ['Todas as Subfuncoes'] + list(data['Subfunção'].unique()))
        
        data_visualization = data.copy()

        if selected_uf != "Todas as UF":
            data_visualization = data_visualization[(data_visualization['UF'] == selected_uf)]
        if selected_ano != "Todos os anos":
            data_visualization = data_visualization[(data_visualization['Ano'] == selected_ano)]

        if selected_regiao != 'Todas as Regiões':
            data_visualization = data_visualization[(data_visualization['Região'] == selected_regiao)]
        if selected_subfunco != 'Todas as Subfuncoes':
            data_visualization = data_visualization[(data_visualization['Subfunção'] == selected_subfunco)]

        st.subheader('Dados Filtrados')

        st.write(data_visualization)
            
        st.subheader(f'Valor Total por Estágio de Despesa')
        st.text(f"UF: {selected_uf} / Ano: {selected_ano} / Subfunção: {selected_subfunco} / Região: {selected_regiao}")
        
        Empenhado, Liquidado, Pago, RP_Pago, Despesa_Executada = get_despesas(data_visualization)
        mostrar_despesas(Empenhado, Liquidado, Pago, RP_Pago, Despesa_Executada)

        total_by_coluna = [Empenhado, Liquidado, Pago, RP_Pago, Despesa_Executada]
        #Gráfico Despesa
        with st.expander("Visualizar gráfico de despesa"):
            criar_grafico_barras(total_by_coluna)
      
if __name__ == '__main__':
    main()