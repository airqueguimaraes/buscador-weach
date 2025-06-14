import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# --- ESTRUTURA DE SITES ATUALIZADA PARA INCLUIR LOCALIZAÇÕES (v1.5) ---
SITES = {
    "G1": {
        "domain": "g1.globo.com",
        "locations": {
            "Nacional": "",
            "AC": "/ac/", "AL": "/al/", "AP": "/ap/", "AM": "/am/", "BA": "/ba/", 
            "CE": "/ce/", "DF": "/df-distrito-federal/", "ES": "/es/", "GO": "/go/", 
            "MA": "/ma/", "MT": "/mt/", "MS": "/ms/", "MG": "/mg/", "PA": "/pa/", 
            "PB": "/pb/", "PR": "/pr/", "PE": "/pe/", "PI": "/pi/", "RJ": "/rj/", 
            "RN": "/rn/", "RS": "/rs/", "RO": "/ro/", "RR": "/rr/", "SC": "/sc/", 
            "SP": "/sp/", "SE": "/se/", "TO": "/to/"
        }
    },
    "O Globo": {
        "domain": "oglobo.globo.com",
        "locations": { "Nacional": "" }
    },
    "UOL": {
        "domain": "uol.com.br",
        "locations": { "Nacional": "" }
    },
    "Estadão": {
        "domain": "estadao.com.br",
        "locations": { "Nacional": "" }
    },
    "TecMundo": {
        "domain": "tecmundo.com.br",
        "locations": { "Nacional": "" }
    },
    # Adicione outros sites aqui no mesmo formato
}

TEMAS = [
    "Qualquer Tema", "Alimento", "Bem-estar", "Carreira", "Carro", "Casa & Decoração",
    "Ciência", "Cultura", "Dinheiro", "Educação", "Empreendedorismo", "Esportes",
    "Família", "Imóveis", "Meio Ambiente", "Moda", "Negócios", "Pets", "Saúde",
    "Sustentabilidade", "Tecnologia", "Viagem"
]

# --- INTERFACE DO SITE COM STREAMLIT ---

st.set_page_config(page_title="Buscador Weach", layout="wide")
st.markdown("<h1 style='text-align: center;'>Buscador de Notícias Weach</h1>", unsafe_allow_html=True)

# Organiza os seletores em colunas
col1, col2, col3, col4 = st.columns(4, gap="large")

# --- SELETOR DE DATA (COLUNA 1) ---
with col1:
    st.markdown("<h6>Selecione a Data:</h6>", unsafe_allow_html=True)
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

# --- SELETOR DE SITE (COLUNA 2) ---
with col2:
    st.markdown("<h6>Selecione o Site:</h6>", unsafe_allow_html=True)
    lista_de_sites_ordenada = sorted(SITES.keys())
    site_selecionado = st.selectbox("Site", options=lista_de_sites_ordenada, label_visibility="collapsed")

# --- NOVO SELETOR DE LOCALIZAÇÃO (COLUNA 3) ---
with col3:
    st.markdown("<h6>Selecione a Localização:</h6>", unsafe_allow_html=True)
    # Pega as localizações disponíveis para o site selecionado
    opcoes_localizacao = SITES[site_selecionado].get("locations", {})
    
    # Desabilita o menu se não houver opções de localização (além de "Nacional")
    desabilitar_localizacao = len(opcoes_localizacao) <= 1
    
    localizacao_selecionada = st.selectbox(
        "Localização", 
        options=opcoes_localizacao.keys(), 
        label_visibility="collapsed",
        disabled=desabilitar_localizacao
    )

# --- SELETOR DE TEMA (COLUNA 4) ---
with col4:
    st.markdown("<h6>Selecione o Tema:</h6>", unsafe_allow_html=True)
    tema_selecionado = st.selectbox("Tema", options=TEMAS, label_visibility="collapsed")

st.write("") 

# --- LÓGICA DO BOTÃO ATUALIZADA ---
if st.button("Achar Minha Notícia no Google", type="primary", use_container_width=True):
    base_domain = SITES[site_selecionado]["domain"]
    
    # Adiciona o caminho da localização ao domínio, se aplicável
    location_path = SITES[site_selecionado].get("locations", {}).get(localizacao_selecionada, "")
    dominio_completo = base_domain + location_path
    
    data_selecionada = datetime(int(ano_selecionado), int(mes_selecionado), int(dia_selecionado))
    data_anterior = data_selecionada - timedelta(days=1)
    data_posterior = data_selecionada + timedelta(days=1)
    after_str = data_anterior.strftime('%Y-%m-%d')
    before_str = data_posterior.strftime('%Y-%m-%d')
    
    partes_da_busca = [f"site:{dominio_completo}", f"after:{after_str}", f"before:{before_str}"]
    if tema_selecionado != "Qualquer Tema":
        partes_da_busca.append(f'"{tema_selecionado}"')
        
    query_final = " ".join(partes_da_busca)
    url_google = f"https://www.google.com/search?q={urllib.parse.quote_plus(query_final)}"
    
    link_markdown = f"<a href='{url_google}' target='_blank' style='display: inline-block; padding: 11px 20px; background-color: #fbbc07; color: #000000; text-align: center; text-decoration: none; font-weight: bold; border-radius: 5px;'>✔️ Clique aqui para ver os resultados da busca</a>"
    st.markdown(link_markdown, unsafe_allow_html=True)
