import streamlit as st
import matplotlib.pyplot as plt

def criar_grafico_barras(total_by_coluna):
    variaveis = ['Empenhado', 'Liquidado', 'Pago', 'RP_Pago', 'Despesa_Executada']

    fig, ax = plt.subplots()

    ax.bar(variaveis, total_by_coluna)

    ax.set_ylabel('Valores')

    st.pyplot(fig)
