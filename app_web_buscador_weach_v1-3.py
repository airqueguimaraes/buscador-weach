import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# --- CONFIGURAÇÕES ---
SITES = {
    "G1": {
        "domain": "g1.globo.com",
        "locations": {
            "Nacional": "", "AC": "/ac/", "AL": "/al/", "AP": "/ap/", "AM": "/am/", 
            "BA": "/ba/", "CE": "/ce/", "DF": "/df-distrito-federal/", "ES": "/es/", 
            "GO": "/go/", "MA": "/ma/", "MT": "/mt/", "MS": "/ms/", "MG": "/mg/", 
            "PA": "/pa/", "PB": "/pb/", "PR": "/pr/", "PE": "/pe/", "PI": "/pi/", 
            "RJ": "/rj/", "RN": "/rn/", "RS": "/rs/", "RO": "/ro/", "RR": "/rr/", 
            "SC": "/sc/", "SP": "/sp/", "SE": "/se/", "TO": "/to/"
        }
    },
    "AutoEsporte": {"domain": "autoesporte.globo.com", "locations": {"Nacional": ""}},
    "Campo Grande News": {"domain": "campograndenews.com.br", "locations": {"Nacional": ""}},
    "Caras": {"domain": "caras.com.br", "locations": {"Nacional": ""}},
    "CNN Brasil": {"domain": "cnnbrasil.com.br", "locations": {"Nacional": ""}},
    "Época Negócios": {"domain": "epocanegocios.globo.com", "locations": {"Nacional": ""}},
    "Estadão": {"domain": "estadao.com.br", "locations": {"Nacional": ""}},
    "Exame": {"domain": "exame.com", "locations": {"Nacional": ""}},
    "Gazeta de S. Paulo": {"domain": "gazetasp.com.br", "locations": {"Nacional": ""}},
    "Globo Rural": {"domain": "globorural.globo.com", "locations": {"Nacional": ""}},
    "Globo.com": {"domain": "globo.com", "locations": {"Nacional": ""}},
    "IGN Brasil": {"domain": "ign.com", "locations": {"Nacional": ""}},
    "IstoÉ": {"domain": "istoe.com.br", "locations": {"Nacional": ""}},
    "IstoÉ Dinheiro": {"domain": "istoedinheiro.com.br", "locations": {"Nacional": ""}},
    "MSN": {"domain": "msn.com", "locations": {"Nacional": ""}},
    "Notícias Automotivas": {"domain": "noticiasautomotivas.com.br", "locations": {"Nacional": ""}},
    "O Globo": {"domain": "oglobo.globo.com", "locations": {"Nacional": ""}},
    "Olhar Digital": {"domain": "olhardigital.com.br", "locations": {"Nacional": ""}},
    "Quatro Rodas": {"domain": "quatrorodas.abril.com.br", "locations": {"Nacional": ""}},
    "Radios.com.br": {"domain": "radios.com.br", "locations": {"Nacional": ""}},
    "Só Notícia Boa": {"domain": "sonoticiaboa.com.br", "locations": {"Nacional": ""}},
    "TecMundo": {"domain": "tecmundo.com.br", "locations": {"Nacional": ""}},
    "Tempo.com": {"domain": "tempo.com", "locations": {"Nacional": ""}},
    "UOL": {"domain": "uol.com.br", "locations": {"Nacional": ""}},
    "Valor Econômico": {"domain": "valor.globo.com", "locations": {"Nacional": ""}}
}

TEMAS = [
    "Qualquer Tema", "Alimento", "Bem-estar", "Carreira", "Carro", "Casa & Decoração",
    "Ciência", "Cultura", "Dinheiro", "Educação", "Empreendedorismo", "Esportes",
    "Família", "Imóveis", "Meio Ambiente", "Moda", "Negócios", "Pets", "Saúde",
    "Sustentabilidade", "Tecnologia", "Viagem"
]

PALAVRAS_SENSIVEIS = [
    "morte", "morre", "morreu", "assassinato", "assassinado", "crime", "homicídio", 
    "latrocínio", "estupro", "abuso", "sequestro", "tragédia", "acidente", "fatal", 
    "vítima", "corpo", "sangue", "ferido", "polícia", "operação", "investigação", 
    "corrupção", "escândalo", "suicídio", "desastre", "condenado", "preso"
]

# --- INTERFACE DO SITE COM STREAMLIT ---

st.set_page_config(page_title="Buscador Weach", layout="wide")
st.markdown("<h1 style='text-align: center; color: #fbbc07;'>Buscador de Notícias Weach</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="large")

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

with col2:
    st.markdown("<h6>Selecione o Site:</h6>", unsafe_allow_html=True)
    lista_de_sites_ordenada = sorted(SITES.keys())
    site_selecionado = st.selectbox("Site", options=lista_de_sites_ordenada, label_visibility="collapsed")

with col3:
    st.markdown("<h6>Selecione a Localização:</h6>", unsafe_allow_html=True)
    opcoes_localizacao = SITES[site_selecionado].get("locations", {})
    desabilitar_localizacao = len(opcoes_localizacao) <= 1
    localizacao_selecionada = st.selectbox("Localização", options=opcoes_localizacao.keys(), label_visibility="collapsed", disabled=desabilitar_localizacao)

with col4:
    st.markdown("<h6>Selecione o Tema:</h6>", unsafe_allow_html=True)
    tema_selecionado = st.selectbox("Tema", options=TEMAS, label_visibility="collapsed")

st.write("---") 

evitar_sensiveis = st.checkbox("✔️ Marcar para ativar o filtro de Brand Safety (evitar notícias com palavras sensíveis)")

st.write("---")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    if st.button("Achar Minha Notícia no Google", use_container_width=True):
        base_domain = SITES[site_selecionado]["domain"]
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
        
        if evitar_sensiveis:
            termos_negativos = " ".join([f"-{palavra}" for palavra in PALAVRAS_SENSIVEIS])
            partes_da_busca.append(termos_negativos)
            
        query_final = " ".join(partes_da_busca)
        url_google = f"https://www.google.com/search?q={urllib.parse.quote_plus(query_final)}"
        
        link_markdown = f"<a href='{url_google}' target='_blank' style='display: inline-block; padding: 11px 20px; background-color: #fbbc07; color: #021850; text-align: center; text-decoration: none; font-weight: bold; border-radius: 5px;'>✔️ Clique aqui para ver os resultados da busca</a>"
        st.markdown(link_markdown, unsafe_allow_html=True)

# --- CSS CUSTOMIZADO PARA O ESTILO EXATO DO BOTÃO ---
st.markdown("""
<style>
    /* Seleciona o botão dentro do container do Streamlit */
    .stButton > button {
        border: 2px solid #021850;
        background-color: #021850;
        color: #ffffff;
        font-weight: bold;
    }
    
    /* Define o estilo QUANDO O MOUSE PASSA POR CIMA (hover) */
    .stButton > button:hover {
        border: 2px solid #fbbc07;
        background-color: #fbbc07;
        color: #021850;
    }
</style>
""", unsafe_allow_html=True)
