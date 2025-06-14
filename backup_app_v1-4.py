import streamlit as st
import webbrowser
from datetime import datetime, timedelta
import urllib.parse

# --- CONFIGURAÇÕES ---
SITES = {
    "AutoEsporte": "autoesporte.globo.com", "Campo Grande News": "campograndenews.com.br",
    "Caras": "caras.com.br", "CNN Brasil": "cnnbrasil.com.br",
    "Época Negócios": "epocanegocios.globo.com", "Estadão": "estadao.com.br",
    "Exame": "exame.com", "G1": "g1.globo.com", "Gazeta de S. Paulo": "gazetasp.com.br",
    "Globo Rural": "globorural.globo.com", "Globo.com": "globo.com", "IGN Brasil": "ign.com",
    "IstoÉ": "istoe.com.br", "IstoÉ Dinheiro": "istoedinheiro.com.br", "MSN": "msn.com",
    "Notícias Automotivas": "noticiasautomotivas.com.br", "O Globo": "oglobo.globo.com",
    "Olhar Digital": "olhardigital.com.br", "Quatro Rodas": "quatrorodas.abril.com.br",
    "Radios.com.br": "radios.com.br", "Só Notícia Boa": "sonoticiaboa.com.br",
    "TecMundo": "tecmundo.com.br", "Tempo.com": "tempo.com", "UOL": "uol.com.br",
    "Valor Econômico": "valor.globo.com"
}

TEMAS = [
    "Qualquer Tema", "Alimento", "Bem-estar", "Carreira", "Carro", "Casa & Decoração",
    "Ciência", "Cultura", "Dinheiro", "Educação", "Empreendedorismo", "Esportes",
    "Família", "Imóveis", "Meio Ambiente", "Moda", "Negócios", "Pets", "Saúde",
    "Sustentabilidade", "Tecnologia", "Viagem"
]

# --- INTERFACE DO SITE COM STREAMLIT ---

# Título da Página
st.set_page_config(page_title="Buscador Weach", layout="wide")

# Título centralizado usando Markdown e HTML
st.markdown("<h1 style='text-align: center;'>Buscador de Notícias Weach</h1>", unsafe_allow_html=True)

# Organiza os seletores em colunas
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("<h6>Selecione a Data:</h6>", unsafe_allow_html=True)
    # --- LÓGICA DOS 3 MENUS DE DATA ---
    dias = [str(d).zfill(2) for d in range(1, 32)]
    meses = [str(m).zfill(2) for m in range(1, 13)]
    anos = [str(y) for y in range(datetime.now().year, datetime.now().year - 10, -1)]
    
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    with sub_col1:
        dia_selecionado = st.selectbox("Dia", options=dias, index=datetime.now().day - 1, label_visibility="collapsed")
    with sub_col2:
        mes_selecionado = st.selectbox("Mês", options=meses, index=datetime.now().month - 1, label_visibility="collapsed")
    with sub_col3:
        ano_selecionado = st.selectbox("Ano", options=anos, label_visibility="collapsed")

with col2:
    st.markdown("<h6>Selecione o Site:</h6>", unsafe_allow_html=True)
    lista_de_sites_ordenada = sorted(SITES.keys())
    site_selecionado = st.selectbox("Site", options=lista_de_sites_ordenada, label_visibility="collapsed")

with col3:
    st.markdown("<h6>Selecione o Tema:</h6>", unsafe_allow_html=True)
    tema_selecionado = st.selectbox("Tema", options=TEMAS, label_visibility="collapsed")

st.write("") # Adiciona um espaço vertical

# Botão de Busca
if st.button("Achar Minha Notícia no Google", type="primary", use_container_width=True):
    dominio_site = SITES[site_selecionado]
    data_selecionada = datetime(int(ano_selecionado), int(mes_selecionado), int(dia_selecionado))
    
    data_anterior = data_selecionada - timedelta(days=1)
    data_posterior = data_selecionada + timedelta(days=1)
    after_str = data_anterior.strftime('%Y-%m-%d')
    before_str = data_posterior.strftime('%Y-%m-%d')
    partes_da_busca = [f"site:{dominio_site}", f"after:{after_str}", f"before:{before_str}"]
    if tema_selecionado != "Qualquer Tema":
        partes_da_busca.append(f'"{tema_selecionado}"')
    query_final = " ".join(partes_da_busca)
    url_google = f"https://www.google.com/search?q={urllib.parse.quote_plus(query_final)}"
    
    link_markdown = f"<a href='{url_google}' target='_blank' style='display: inline-block; padding: 11px 20px; background-color: #fbbc07; color: #000000; text-align: center; text-decoration: none; font-weight: bold; border-radius: 5px;'>✔️ Clique aqui para ver os resultados da busca</a>"
    st.markdown(link_markdown, unsafe_allow_html=True)
