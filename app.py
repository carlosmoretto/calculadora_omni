import streamlit as st

st.set_page_config(page_title="Nexaas - Calculadora Omni", page_icon="faviconV2.png")

# Aplicar CSS customizado
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .css-18e3th9 {
        background-color: #030f31;
    }
    .css-1d391kg { 
        background-color: #0b1946;
    }
    .css-10trblm {
        color: #ffffff;
    }
    .css-2trqyj {
        color: #da3063;
    }
    .stSidebar {
        background-color: #030f31;
        color: #ffffff;
    }
    .stSidebar .sidebar-content h1, .stSidebar .sidebar-content h2, .stSidebar .sidebar-content h3, .stSidebar .sidebar-content h4, .stSidebar .sidebar-content h5, .stSidebar .sidebar-content h6 {
        color: #ffffff;
    }
    .stSidebar .sidebar-content .stHeader {
        color: #ffffff;
    }
    .stMainBlockContainer{
        width: 100%;
        padding: 2rem 1rem 10rem;
        max-width: 46rem;
    </style>
    """, unsafe_allow_html=True)


# Título da calculadora
st.title('Calculadora Nexaas')

# Inserir logo no topo esquerdo da sidebar
st.sidebar.image('https://cdn.prod.website-files.com/64668a3aea99d8467b17deab/65b797a57a29dbaf17c77aee_NEXAAS_LOGO_HORIZONTAL_BRANCO_1%201.png', width=106)

# Seção para entrada de dados
st.header('Suas Vendas')

num_lojas = st.number_input('Quantas lojas você possui?', min_value=1, step=1, value=20, key='op1')
quant_vendas_mensais = st.number_input('Em média, qual a quantidade de vendas mensais?', min_value=1, step=1, value=2, key='op2')
quant_skus = st.number_input("Quantos SKU's em média você possui total?", min_value=1, step=1, value=300, key='op3')
num_canais_venda = st.number_input('Quantos canais de venda diferentes?', min_value=1, step=1, value=5, key='op4')

# Definindo os valores fixos para o cálculo
request_sku_oms = 17200000*4
request_sales_oms = 8300000*4

custo_por_produto_pedidoD03 = 570519
custo_por_produto_pedidoD04 = 55445

custo_por_produto_pedidoD05 = round(request_sku_oms / custo_por_produto_pedidoD03, 7)
custo_por_produto_pedidoD06 = round(request_sales_oms / custo_por_produto_pedidoD04, 7)
custo_por_produto_pedidoD07 = 29000
custo_por_produto_pedidoD08 = round(custo_por_produto_pedidoD07 / (request_sku_oms + request_sales_oms), 4)
custo_por_produto_pedidoD09 = round(custo_por_produto_pedidoD08 * custo_por_produto_pedidoD05, 4)  # D8 * D5
custo_por_produto_pedidoD10 = round(custo_por_produto_pedidoD08 * custo_por_produto_pedidoD06, 4)  # D8 * D6
custo_por_produto_pedidoD11 = 30
custo_por_produto_pedidoD12 = 1.5
custo_por_produto_pedidoD14 = 200

custo_por_produto_pedidoD15 = 522.43  # ='Cópia de Custo por Loja'!M9 - FIXO
custo_por_produto_pedidoD16 = 129.03  # ='Custo por Loja simulação +250 lojas'!M9 - FIXO
custo_por_produto_pedidoD17 = 143.52  # ='Cópia de Custo por Loja'!N91/165 - FIXO

custo_por_produto_pedidoD18 = 71.04  # ='Cópia de Custo por Loja'!N91/400*1,2
custo_por_produto_pedidoD19 = 195.12  # ='Cópia de Custo por Loja'!O9
custo_por_produto_pedidoD20 = 48.19  # ='Custo por Loja simulação +250 lojas'!O9

# Condicional para determinar o valor de 'cond1'
if num_lojas <= 165:
    cond1 = (custo_por_produto_pedidoD15 + custo_por_produto_pedidoD17 + custo_por_produto_pedidoD19) * num_lojas
else:
    cond1 = (custo_por_produto_pedidoD16 + custo_por_produto_pedidoD18 + custo_por_produto_pedidoD20) * num_lojas

# Cálculo do valor total
total_valor = num_lojas * custo_por_produto_pedidoD14 + (custo_por_produto_pedidoD10 * quant_vendas_mensais + custo_por_produto_pedidoD09 * quant_skus)\
                        * num_canais_venda * custo_por_produto_pedidoD12 + custo_por_produto_pedidoD11 + cond1

total_setup = round(total_valor * 5, 2)

valor_por_loja = total_valor / num_lojas

# Função para formatar valores monetários
def formatar_valor(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')

@st.dialog("Resumo dos Totalizadores")
def calc (total_valor, valor_por_loja, total_setup):
    # st.write('\n**Totalizadores**')
    st.write(f'Nexaas Omni por apenas: **{formatar_valor(round(total_valor, 2))}**')
    st.write(f'Valor por loja: **{formatar_valor(round(valor_por_loja, 2))}**')
    st.write(f'Valor do Setup: **{formatar_valor(round(total_setup, 2))}**')

if st.button("Calcular"):
    calc(total_valor, valor_por_loja, total_setup)


# # Exibição dos totalizadores
# st.sidebar.write('\n**Totalizadores**')
# st.sidebar.write(f'Nexaas Omni por apenas: **{formatar_valor(round(total_valor, 2))}**')
# st.sidebar.write(f'Valor por loja: **{formatar_valor(round(valor_por_loja, 2))}**')
# st.sidebar.write(f'Valor do Setup: **{formatar_valor(round(total_setup, 2))}**')
