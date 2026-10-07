import json
import os
from datetime import datetime, timedelta
import streamlit as st

DB_FILE = "turnos_sucursales_db.json"
ARCHIVO_LOGO = "logo.png"

# ==========================================
# CONFIGURACIÓN DE TÍTULOS Y LOGO PRINCIPAL
# ==========================================
TEXTO_TITULO_PESTAÑA = "Punto Dental - Sistema de Gestión"
ICONO_PESTAÑA = "🦷"  
TITULO_ENCABEZADO_APP = "Punto Dental"  
# ==========================================

st.set_page_config(
    page_title=TEXTO_TITULO_PESTAÑA, page_icon=ICONO_PESTAÑA, layout="wide"
)

# Estilos CSS generales
st.markdown("""
    <style>
    .stApp {
        background-color: #2b3b4e !important;
        color: #ffffff !important;
    }
    header[data-testid="stHeader"] {
        background-color: #2b3b4e !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1f2a37 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3, h4, h5, h6, span, label, .stMarkdown, p {
        color: #ffffff !important;
    }
    div.stButton > button {
        background-color: #ffffff !important;
        color: #1f2a37 !important;
        border: 1px solid #d1d5db !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        width: 100% !important;
    }
    div.stButton > button *, div.stButton > button p, div.stButton > button span {
        color: #1f2a37 !important;
    }
    div.stButton > button:hover {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
    }
    div.stButton > button:hover *, div.stButton > button:hover p, div.stButton > button:hover span {
        color: #ffffff !important;
    }
    .consulta-card {
        background: #ffffff !important;
        color: #1f2a37 !important;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #3b82f6;
    }
    .consulta-card *, .consulta-card b, .consulta-card span {
        color: #1f2a37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SISTEMA DE SEGURIDAD (CONTRASEÑA FIJA)
# ==========================================
def verificar_password():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if st.session_state.autenticado:
        return True

    with st.sidebar:
        if os.path.exists(ARCHIVO_LOGO):
            st.image(ARCHIVO_LOGO, use_container_width=True)
        st.markdown(f"### {ICONO_PESTAÑA} {TITULO_ENCABEZADO_APP}")
        st.warning("🔒 Sistema Privado de la Clínica")
        
        input_pass = st.text_input("Ingrese la Contraseña", type="password")
        
        if st.button("Ingresar", use_container_width=True):
            if input_pass == "1234":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        
        st.markdown("---")
        st.markdown("<small style='color: #9ca3af;'>Acceso restringido únicamente al personal autorizado de la clínica.</small>", unsafe_allow_html=True)
    
    return False

if not verificar_password():
    st.stop()

# ==========================================
# LÓGICA DE DATOS Y FUNCIONES PRINCIPALES
# ==========================================
def cargar_turnos_disco():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "Centro": [{"fecha": "15/10/2026", "hora": "10:00 hs", "paciente": "Juan Pérez", "motivo": "Control anual", "telefono": "+59899123456"}],
        "Gori": [],
        "Colón": []
    }

def guardar_turnos_disco(turnos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(turnos, f, ensure_ascii=False, indent=4)

db_general = cargar_turnos_disco()

# --- BARRA LATERAL ---
with st.sidebar:
    if os.path.exists(ARCHIVO_LOGO):
        st.image(ARCHIVO_LOGO, use_container_width=True)
    
    st.markdown(f"### {ICONO_PESTAÑA} {TITULO_ENCABEZADO_APP}")
    clinicas_disponibles = ["Centro", "Gori", "Colón"]
    
    if "clinica_activa" not in st.session_state:
        st.session_state.clinica_activa = "Centro"

    clinica_activa = st.selectbox(
        "Seleccione Clínica", 
        clinicas_disponibles, 
        index=clinicas_disponibles.index(st.session_state.clinica_activa) if st.session_state.clinica_activa in clinicas_disponibles else 0,
        key="selectbox_clinica_activa"
    )
    
    if clinica_activa != st.session_state.clinica_activa:
        st.session_state.clinica_activa = clinica_activa
        st.rerun()

    st.markdown("---")
    st.markdown(f"**Clínica Activa:** <span style='color: #60a5fa;'>{st.session_state.clinica_activa}</span>", unsafe_allow_html=True)
    st.markdown("Las agendas y turnos se guardan de forma independiente para cada sede.")
    
    if st.button("🔒 Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

clinica_actual = st.session_state.clinica_activa

if clinica_actual not in db_general:
    db_general[clinica_actual] = []

turnos_clinica = db_general[clinica_actual]

if "fecha_activa" not in st.session_state:
    st.session_state.fecha_activa = "15/10/2026"

col_tit_1, col_tit_2 = st.columns([0.1, 0.9])
with col_tit_1:
    if os.path.exists(ARCHIVO_LOGO):
        st.image(ARCHIVO_LOGO, width=60)
with col_tit_2:
    st.title(f"{TITULO_ENCABEZADO_APP} - Clínica {clinica_actual}")

st.markdown("---")

col_izq, col_der = st.columns([1.3, 1], gap="large")

with col_izq:
    st.markdown("### 📅 Selector de Mes y Año")
    
    col_m, col_a = st.columns(2)
    with col_m:
        meses_nombres = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, 
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, 
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        mes_seleccionado_nombre = st.selectbox("Mes", list(meses_nombres.keys()), index=9, key="sel_mes")
        mes_num = meses_nombres[mes_seleccionado_nombre]
        
    with col_a:
        anos_disponibles = [2026, 2027, 2028]
        anio_num = st.selectbox("Año", anos_disponibles, index=0, key="sel_anio")

    st.markdown(f"**Fecha Activa Seleccionada:** <span translate='no' style='color: #60a5fa; font-size: 1.1em; font-weight: bold;'>{st.session_state.fecha_activa}</span>", unsafe_allow_html=True)
    
    st.markdown("#### 🗓️ Calendario Mensual Interactivo")
    st.markdown("<small style='color: #cbd5e1 !important;'>Hacé clic en cualquier día para seleccionarlo y ver sus horarios:</small>", unsafe_allow_html=True)
    
    inicio_mes = datetime(anio_num, mes_num, 1)
    if mes_num == 12:
        fin_mes = datetime(anio_num + 1, 1, 1) - timedelta(days=1)
    else:
        fin_mes = datetime(anio_num, mes_num + 1, 1) - timedelta(days=1)
        
    fechas_con_turnos = [t["fecha"] for t in turnos_clinica]
    hoy_str = datetime.now().strftime("%d/%m/%Y")
    
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    cols_encabezado = st.columns(7)
    for i, col in enumerate(cols_encabezado):
        col.markdown(f"<p translate='no' style='text-align:center; font-weight:bold; font-size:13px; color:#93c5fd;'>{dias_semana[i]}</p>", unsafe_allow_html=True)
        
    dia_actual_iter = inicio_mes
    
    while dia_actual_iter <= fin_mes:
        cols_semana = st.columns(7)
        for dia_idx in range(7):
            if dia_actual_iter <= fin_mes and dia_actual_iter.weekday() == dia_idx:
                str_dia = dia_actual_iter.strftime("%d/%m/%Y")
                num_dia_str = dia_actual_iter.strftime('%d')
                
                with cols_semana[dia_idx]:
                    dia_seleccionado = (str_dia == st.session_state.fecha_activa)
                    label_boton = f"✅ {num_dia_str}" if dia_seleccionado else num_dia_str
                    
                    if st.button(label_boton, key=f"btn_dia_{clinica_actual}_{str_dia}"):
                        st.session_state.fecha_activa = str_dia
                        st.rerun()
                        
                    if str_dia == hoy_str:
                        st.markdown('<div style="width: 22px; height: 3px; background-color: #f97316; margin: -4px auto 6px auto; border-radius: 2px;"></div>', unsafe_allow_html=True)
                    elif str_dia in fechas_con_turnos:
                        st.markdown('<div style="width: 22px; height: 3px; background-color: #3b82f6; margin: -4px auto 6px auto; border-radius: 2px;"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="width: 22px; height: 3px; background-color: transparent; margin: -4px auto 6px auto;"></div>', unsafe_allow_html=True)
                        
                dia_actual_iter += timedelta(days=1)
            else:
                with cols_semana[dia_idx]:
                    st.write("")

    st.markdown("---")
    st.markdown(f"### 📋 Consultas agendadas en **{clinica_actual}** para el: {st.session_state.fecha_activa}")
    
    turnos_filtrados = [t for t in turnos_clinica if t["fecha"] == st.session_state.fecha_activa]
    
    if turnos_filtrados:
        for idx, t in enumerate(turnos_filtrados):
            st.markdown(f"""
                <div class="consulta-card">
                    <b>🕒 {t['hora']}
