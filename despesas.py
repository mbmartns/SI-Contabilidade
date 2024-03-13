import streamlit as st
import pandas as pd
import re

def formatar_numero(numero):
    """
    Função responsável por colocar sufixo nos números baseados na escala númerica.
    """
    sufixos_singular = ['', ' mil', ' milhão', ' bilhão', ' trilhão']
    sufixos_plural = ['', ' mil', ' milhões', ' bilhões', ' trilhões']

    escala = 0
    
    while numero >= 1000 and escala < len(sufixos_singular) - 1:
        escala += 1
        numero /= 1000.0
    
    numero_formatado = f'{numero:.2f}'
    
    numero_formatado = numero_formatado.rstrip('0').rstrip('.')
    
    comparacao = numero_formatado.split('.')
    if comparacao[0] == '1':
        numero_formatado += sufixos_singular[escala]
    else:
        numero_formatado += sufixos_plural[escala]
    
    return numero_formatado



def get_despesas(data):
    columns = ['Empenhado', 'Liquidado', 'Pago', 'RP Pago', 'Despesa Executada']
    # result = {}
    # for column in columns:
    #     total_sum = 0
    #     for value in data[column]:
    #         try:
    #             num = pd.to_numeric(value.strip().replace('.', '').replace(',', '.').replace(' ', ''), errors='raise')
    #             total_sum += num
    #         except (ValueError, TypeError) as e:
    #             # print(f'Erro ao converter {value} para float')
    #             # print(e)
    #             continue
    #     # formatted_sum = '{:,.2f}'.format(total_sum).replace(',', '.')
    #     # split_value = formatted_sum.split('.')
    #     # formatted_value = '.'.join(split_value[:-1]) + ',' + split_value[-1]
    #     result[column] = total_sum

    Empenhado, Liquidado, Pago, RP_Pago, Despesa_Executada = data.loc[:, columns].sum()
    
    return Empenhado, Liquidado, Pago, RP_Pago, Despesa_Executada


def mostrar_despesas(Empenhado, Liquidado, Pago, RP_Pago, Despesa_Executada):
    """
    Função responsável por colocar visualmente as despesas no Streamlit.
    Os dados colocados são: Despesas Empenhadas, Despesas Liquidadas, Despesas Pagas, Execução de Despesa.
    """
    col5, col6, col7 = st.columns(3) 
    col5.metric("Empenhado", formatar_numero(Empenhado))
    col6.metric("Liquidado", formatar_numero(Liquidado))    
    col7.metric("Pago", formatar_numero(Pago))
    col8, col9 = st.columns(2) 
    col8.metric("RP Pago", formatar_numero(RP_Pago))
    col9.metric("Executado", formatar_numero(Despesa_Executada))
