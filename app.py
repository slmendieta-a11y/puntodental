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
                    if st.button(num_dia_str, key=f"btn_dia_{clinica_actual}_{str_dia}", use_container_width=True):
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
                    <b>🕒 {t['hora']}</b> - {t['paciente']}<br>
                    <b>Motivo:</b> {t['motivo']}<br>
                    <b>Teléfono:</b> {t['telefono']}
                </div>
            """, unsafe_allow_html=True)
            
            tel_limpio = t['telefono'].replace(" ", "").replace("+", "").replace("-", "")
            msg_wpp = f"Hola {t['paciente']}, te escribimos desde la clínica {clinica_actual} de {TITULO_ENCABEZADO_APP} para recordarte tu turno el día {t['fecha']} a las {t['hora']}."
            
            url_wpp = f"https://web.whatsapp.com/send?phone={tel_limpio}&text={msg_wpp.replace(' ', '%20')}"
            
            st.markdown(f'<a href="{url_wpp}" target="_blank" style="text-decoration:none;"><div style="background-color: #25d366; color: white; padding: 8px 12px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px; font-size: 14px;">💬 Enviar WhatsApp a {t["paciente"]}</div></a>', unsafe_allow_html=True)
        
        st.markdown("#### ⚙️ Gestionar Turnos de este Día")
        opciones_gestion = [f"{t['hora']} - {t['paciente']}" for t in turnos_filtrados]
        turno_seleccionado_str = st.selectbox("Seleccione turno a modificar, cambiar de clínica o eliminar", opciones_gestion, key=f"gestion_{clinica_actual}_{st.session_state.fecha_activa}")
        
        idx_en_filtrados = opciones_gestion.index(turno_seleccionado_str)
        t_seleccionado = turnos_filtrados[idx_en_filtrados]
        
        indice_real = turnos_clinica.index(t_seleccionado)
        
        col_del, col_mov = st.columns(2)
        with col_del:
            if st.button("🗑️ Eliminar Turno", key=f"btn_del_{clinica_actual}_{indice_real}", use_container_width=True):
                turnos_clinica.pop(indice_real)
                db_general[clinica_actual] = turnos_clinica
                guardar_turnos_disco(db_general)
                st.success("¡Turno eliminado correctamente!")
                st.rerun()
                
        with col_mov:
            modo_mover = st.checkbox("🔄 Cambiar de Clínica", key=f"chk_mov_{clinica_actual}_{indice_real}")

        if modo_mover:
            st.markdown("##### Mover Turno a Otra Clínica")
            otras_clinicas = [s for s in clinicas_disponibles if s != clinica_actual]
            nueva_clinica_destino = st.selectbox("Seleccionar nueva clínica", otras_clinicas, key=f"sel_nueva_clinica_{clinica_actual}_{indice_real}")
            
            if st.button("🚀 Confirmar Cambio de Clínica", key=f"btn_conf_mov_{clinica_actual}_{indice_real}", use_container_width=True):
                turnos_destino = db_general.get(nueva_clinica_destino, [])
                conflicto_destino = any(t["fecha"] == t_seleccionado["fecha"] and t["hora"] == t_seleccionado["hora"] for t in turnos_destino)
                
                if conflicto_destino:
                    st.error(f"⚠️ El horario {t_seleccionado['hora']} del día {t_seleccionado['fecha']} ya está ocupado en la clínica {nueva_clinica_destino}.")
                else:
                    turnos_clinica.pop(indice_real)
                    db_general[clinica_actual] = turnos_clinica
                    
                    if nueva_clinica_destino not in db_general:
                        db_general[nueva_clinica_destino] = []
                    db_general[nueva_clinica_destino].append(t_seleccionado)
                    
                    guardar_turnos_disco(db_general)
                    st.success(f"¡Turno movido con éxito a la clínica {nueva_clinica_destino}!")
                    st.rerun()
            
        modo_edicion = st.checkbox("✏️ Editar datos / hora", key=f"chk_edit_{clinica_actual}_{indice_real}")
            
        if modo_edicion:
            st.markdown("##### Modificar Datos del Turno")
            nuevo_nombre = st.text_input("Nuevo Nombre", value=t_seleccionado['paciente'], key=f"edit_nom_{clinica_actual}_{indice_real}")
            nuevo_motivo = st.text_input("Nuevo Motivo", value=t_seleccionado['motivo'], key=f"edit_mot_{clinica_actual}_{indice_real}")
            nuevo_tel = st.text_input("Nuevo Teléfono", value=t_seleccionado['telefono'], key=f"edit_tel_{clinica_actual}_{indice_real}")
            
            col_eh, col_em = st.columns(2)
            with col_eh:
                horas_disp = [f"{h:02d}" for h in range(0, 24)]
                h_actual = t_seleccionado['hora'].split(":")[0]
                idx_h = horas_disp.index(h_actual) if h_actual in horas_disp else 9
                e_hora = st.selectbox("Nueva Hora", horas_disp, index=idx_h, key=f"edit_h_{clinica_actual}_{indice_real}")
            with col_em:
                min_disp = [f"{m:02d}" for m in range(0, 60, 5)]
                m_actual = t_seleccionado['hora'].split(":")[1].replace(" hs", "")
                idx_m = min_disp.index(m_actual) if m_actual in min_disp else 0
                e_min = st.selectbox("Nuevos Minutos", min_disp, index=idx_m, key=f"edit_m_{clinica_actual}_{indice_real}")
                
            nueva_hora_completa = f"{e_hora}:{e_min} hs"
            
            if st.button("💾 Guardar Cambios", key=f"btn_save_edit_{clinica_actual}_{indice_real}", use_container_width=True):
                conflicto = any(
                    i != indice_real and t["fecha"] == st.session_state.fecha_activa and t["hora"] == nueva_hora_completa 
                    for i, t in enumerate(turnos_clinica)
                )
                if conflicto:
                    st.error(f"⚠️ El horario {nueva_hora_completa} ya está ocupado en esta clínica.")
                else:
                    turnos_clinica[indice_real] = {
                        "fecha": st.session_state.fecha_activa,
                        "hora": nueva_hora_completa,
                        "paciente": nuevo_nombre.strip(),
                        "motivo": nuevo_motivo.strip(),
                        "telefono": nuevo_tel.strip()
                    }
                    db_general[clinica_actual] = turnos_clinica
                    guardar_turnos_disco(db_general)
                    st.success("¡Turno actualizado con éxito!")
                    st.rerun()
    else:
        st.info("No hay consultas agendadas para esta fecha en esta clínica.")

with col_der:
    st.markdown("### ⏰ Nueva Reserva")
    st.markdown(f"Clínica: **{clinica_actual}** | Fecha: **{st.session_state.fecha_activa}**")
    
    nombre_paciente = st.text_input("Nombre del Paciente", key=f"input_nombre_{clinica_actual}")
    motivo_consulta = st.text_input("Motivo de la Consulta", key=f"input_motivo_{clinica_actual}")
    telefono_paciente = st.text_input("Teléfono (WhatsApp)", key=f"input_tel_{clinica_actual}", value="+598")
    
    st.markdown("#### Seleccionar Horario del Turno:")
    col_h, col_m_min = st.columns(2)
    with col_h:
        horas_disponibles = [f"{h:02d}" for h in range(0, 24)]
        hora_sel = st.selectbox("Hora", horas_disponibles, index=9, key=f"sel_h_{clinica_actual}")
    with col_m_min:
        minutos_disponibles = [f"{m:02d}" for m in range(0, 60, 5)]
        minuto_sel = st.selectbox("Minutos", minutos_disponibles, index=0, key=f"sel_m_{clinica_actual}")
        
    hora_seleccionada = f"{hora_sel}:{minuto_sel} hs"
    
    ocupado = any(t["fecha"] == st.session_state.fecha_activa and t["hora"] == hora_seleccionada for t in turnos_clinica)
    
    st.markdown(f"**Horario elegido:** <span style='color: #60a5fa;'>{hora_seleccionada}</span>", unsafe_allow_html=True)
    
    if ocupado:
        st.button(f"🔴 Ocupado - {hora_seleccionada}", key=f"btn_ocupado_{clinica_actual}", disabled=True, use_container_width=True)
        st.warning(f"⚠️ El horario seleccionado ({hora_seleccionada}) ya se encuentra ocupado en {clinica_actual}.")
    else:
        if st.button(f"🟢 Confirmar Reserva ({hora_seleccionada})", key=f"btn_libre_{clinica_actual}", use_container_width=True):
            ocupado_check = any(t["fecha"] == st.session_state.fecha_activa and t["hora"] == hora_seleccionada for t in turnos_clinica)
            if ocupado_check:
                st.error(f"⚠️ Error: El horario {hora_seleccionada} ya fue ocupado.")
            elif nombre_paciente.strip():
                nuevo_t = {
                    "fecha": st.session_
                    }
