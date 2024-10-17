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

var_calc = dict()

# Definindo os valores fixos para o cálculo
request_sku_oms = 17200000*4
var_calc['var_request_sku_oms'] = request_sku_oms

request_sales_oms = 8300000*4
var_calc["var_request_sales_oms"] = request_sales_oms

total_produtos = 570519
var_calc['var_total_produtos'] = total_produtos

total_pedidos = 55445
var_calc['var_total_pedidos'] = total_pedidos

requisicoes_por_produto = round(request_sku_oms / total_produtos, 7)
var_calc['var_requisicoes_por_produto'] = requisicoes_por_produto
requisicoes_por_pedido = round(request_sales_oms / total_pedidos, 7)
var_calc['var_requisicoes_por_pedido'] = requisicoes_por_pedido
custo_total_aws_oms = 29000
var_calc['var_custo_total_aws_oms'] = custo_total_aws_oms
custo_por_requisicao = round(custo_total_aws_oms / (request_sku_oms + request_sales_oms), 4)
var_calc['var_custo_por_requisicao'] = custo_por_requisicao
custo_por_produto = round(custo_por_requisicao * requisicoes_por_produto, 4)  # D8 * D5
var_calc['var_custo_por_produto'] = custo_por_produto
custo_por_pedido = round(custo_por_requisicao * requisicoes_por_pedido, 4)  # D8 * D6
var_calc['var_custo_por_pedido'] = custo_por_pedido
custo_armazenamento_organizacao = 0.0012
var_calc['var_custo_armazenamento_organizacao'] = custo_armazenamento_organizacao
vetor_integracoes = 0.2
var_calc['var_vetor_integracoes'] = vetor_integracoes
margem_meta = 0.2
var_calc['var_margem_meta'] = margem_meta
custo_pdv = 150
var_calc['var_custo_pdv'] = custo_pdv

custo_medio_dev_165_lojas  = 522.43  # ='Cópia de Custo por Loja'!M9 - FIXO
var_calc['var_custo_medio_dev_165_lojas'] = custo_medio_dev_165_lojas
custo_medio_dev_400_lojas  = 129.03  # ='Custo por Loja simulação +250 lojas'!M9 - FIXO
var_calc['var_custo_medio_dev_400_lojas'] = custo_medio_dev_400_lojas
custo_medio_suporte_165_lojas  = 143.52  # ='Cópia de Custo por Loja'!N91/165 - FIXO
var_calc['var_custo_medio_suporte_165_lojas'] = custo_medio_suporte_165_lojas

custo_medio_suporte_400_lojas = 71.04  # ='Cópia de Custo por Loja'!N91/400*1,2
var_calc['var_custo_medio_suporte_400_lojas'] = custo_medio_suporte_400_lojas
custo_medio_cs_165_lojas = 195.12  # ='Cópia de Custo por Loja'!O9
var_calc['var_custo_medio_cs_165_lojas'] = custo_medio_cs_165_lojas
custo_medio_cs_400_lojas = 48.19  # ='Custo por Loja simulação +250 lojas'!O9
var_calc['var_custo_medio_cs_400_lojas'] = custo_medio_cs_400_lojas

# Condicional para determinar o valor de 'cond1'
if num_lojas <= 165:
    cond1 = (custo_medio_dev_165_lojas  + custo_medio_suporte_165_lojas  + custo_medio_cs_165_lojas) * num_lojas
else:
    cond1 = (custo_medio_dev_400_lojas  + custo_medio_suporte_400_lojas + custo_medio_cs_400_lojas) * num_lojas

var_calc['condicion'] = cond1


# Cálculo do valor total
total_valor = (num_lojas * custo_pdv + (custo_por_pedido * quant_vendas_mensais + custo_por_produto * quant_skus)\
                        + (custo_por_pedido*quant_vendas_mensais+custo_por_produto*quant_skus) \
                        * num_canais_venda * vetor_integracoes + custo_armazenamento_organizacao\
                        * (quant_vendas_mensais+quant_skus) + cond1) *(1+margem_meta)

trecho_1 = num_lojas * custo_pdv + (custo_por_pedido * quant_vendas_mensais + custo_por_produto * quant_skus)
# print(f"Trecho Calc 1: {trecho_1}")

trecho_2 = (custo_por_pedido*quant_vendas_mensais+custo_por_produto*quant_skus)  * num_canais_venda * vetor_integracoes + custo_armazenamento_organizacao * (quant_vendas_mensais+quant_skus)
# print(f"Trecho Calc 2: {trecho_2}")

# print(f"Trecho Calc 3: {(1+margem_meta)}")

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
