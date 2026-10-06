import json
import os
from datetime import datetime, timedelta
import streamlit as st

DB_FILE = "turnos_sucursales_db.json"

def cargar_turnos_disco():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    # Estructura por defecto inicial por sucursal
    return {
        "Centro": [{"fecha": "15/10/2026", "hora": "10:00 hs", "paciente": "Juan Pérez", "motivo": "Control anual", "telefono": "+59899123456"}],
        "Gori": [],
        "Colón": []
    }

def guardar_turnos_disco(turnos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(turnos, f, ensure_ascii=False, indent=4)

st.set_page_config(
    page_title="Consola Médica Multi-Sucursal", page_icon="🩺", layout="wide"
)

# Estilos CSS generales
st.markdown("""
    <style>
    .stApp {
        background-color: #2b3b4e !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1f2a37 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3, h4, h5, h6, span, label, .stMarkdown, p {
        color: #ffffff !important;
    }

    /* Botones de días y horarios: Fondo blanco y texto oscuro garantizado */
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

    /* Tarjetas de consultas */
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

# Cargar base de datos general de sucursales
db_general = cargar_turnos_disco()

# --- BARRA LATERAL: SELECCIÓN DE SUCURSAL ---
with st.sidebar:
    st.markdown("### 🏥 Panel de Control")
    sucursales_disponibles = ["Centro", "Gori", "Colón"]
    sucursal_activa = st.selectbox("Seleccione Sucursal", sucursales_disponibles)
    st.markdown("---")
    st.markdown(f"**Sucursal Activa:** <span style='color: #60a5fa;'>{sucursal_activa}</span>", unsafe_allow_html=True)
    st.markdown("Las agendas y turnos se guardan de forma independiente para cada sede.")

# Vinculamos los turnos de la sesión a la sucursal seleccionada
if sucursal_activa not in db_general:
    db_general[sucursal_activa] = []

turnos_sucursal = db_general[sucursal_activa]

if "fecha_activa" not in st.session_state:
    st.session_state.fecha_activa = "15/10/2026"

st.title(f"🩺 Consola Médica - Sucursal {sucursal_activa}")
st.markdown("---")

col_izq, col_der = st.columns([1.3, 1], gap="large")

with col_izq:
    st.markdown("### 📅 Selector de Mes y Año")
    
    col_m, col_a = st.columns(2)
    with col_m:
        meses_nombres = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, 
            "May\u200Bo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, 
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
        
    fechas_con_turnos = [t["fecha"] for t in turnos_sucursal]
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
                    if st.button(num_dia_str, key=f"btn_dia_{sucursal_activa}_{str_dia}", use_container_width=True):
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
    st.markdown(f"### 📋 Consultas agendadas en **{sucursal_activa}** para el: {st.session_state.fecha_activa}")
    
    turnos_filtrados = [t for t in turnos_sucursal if t["fecha"] == st.session_state.fecha_activa]
    
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
            msg_wpp = f"Hola {t['paciente']}, te escribimos desde la sucursal {sucursal_activa} del consultorio médico para recordarte tu turno el día {t['fecha']} a las {t['hora']}."
            
            # Enlace directo optimizado para WhatsApp Web
            url_wpp = f"https://web.whatsapp.com/send?phone={tel_limpio}&text={msg_wpp.replace(' ', '%20')}"
            
            st.markdown(f'<a href="{url_wpp}" target="_blank" style="text-decoration:none;"><div style="background-color: #25d366; color: white; padding: 8px 12px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px; font-size: 14px;">💬 Enviar WhatsApp a {t["paciente"]}</div></a>', unsafe_allow_html=True)
        
        # --- SECCIÓN DE GESTIÓN (MODIFICAR / ELIMINAR) ---
        st.markdown("#### ⚙️ Gestionar Turnos de este Día")
        opciones_gestion = [f"{t['hora']} - {t['paciente']}" for t in turnos_filtrados]
        turno_seleccionado_str = st.selectbox("Seleccione turno a modificar o eliminar", opciones_gestion, key=f"gestion_{sucursal_activa}_{st.session_state.fecha_activa}")
        
        idx_en_filtrados = opciones_gestion.index(turno_seleccionado_str)
        t_seleccionado = turnos_filtrados[idx_en_filtrados]
        
        indice_real = turnos_sucursal.index(t_seleccionado)
        
        col_mod, col_del = st.columns(2)
        with col_del:
            if st.button("🗑️ Eliminar Turno", key=f"btn_del_{sucursal_activa}_{indice_real}", use_container_width=True):
                turnos_sucursal.pop(indice_real)
                db_general[sucursal_activa] = turnos_sucursal
                guardar_turnos_disco(db_general)
                st.success("¡Turno eliminado correctamente!")
                st.rerun()
                
        with col_mod:
            modo_edicion = st.checkbox("✏️ Editar datos / hora", key=f"chk_edit_{sucursal_activa}_{indice_real}")
            
        if modo_edicion:
            st.markdown("##### Modificar Datos del Turno")
            nuevo_nombre = st.text_input("Nuevo Nombre", value=t_seleccionado['paciente'], key=f"edit_nom_{sucursal_activa}_{indice_real}")
            nuevo_motivo = st.text_input("Nuevo Motivo", value=t_seleccionado['motivo'], key=f"edit_mot_{sucursal_activa}_{indice_real}")
            nuevo_tel = st.text_input("Nuevo Teléfono", value=t_seleccionado['telefono'], key=f"edit_tel_{sucursal_activa}_{indice_real}")
            
            col_eh, col_em = st.columns(2)
            with col_eh:
                horas_disp = [f"{h:02d}" for h in range(8, 20)]
                h_actual = t_seleccionado['hora'].split(":")[0]
                idx_h = horas_disp.index(h_actual) if h_actual in horas_disp else 2
                e_hora = st.selectbox("Nueva Hora", horas_disp, index=idx_h, key=f"edit_h_{sucursal_activa}_{indice_real}")
            with col_em:
                min_disp = ["00", "10", "20", "30", "40", "50"]
                m_actual = t_seleccionado['hora'].split(":")[1].replace(" hs", "")
                idx_m = min_disp.index(m_actual) if m_actual in min_disp else 0
                e_min = st.selectbox("Nuevos Minutos", min_disp, index=idx_m, key=f"edit_m_{sucursal_activa}_{indice_real}")
                
            nueva_hora_completa = f"{e_hora}:{e_min} hs"
            
            if st.button("💾 Guardar Cambios", key=f"btn_save_edit_{sucursal_activa}_{indice_real}", use_container_width=True):
                conflicto = any(
                    i != indice_real and t["fecha"] == st.session_state.fecha_activa and t["hora"] == nueva_hora_completa 
                    for i, t in enumerate(turnos_sucursal)
                )
                if conflicto:
                    st.error(f"⚠️ El horario {nueva_hora_completa} ya está ocupado en esta sucursal.")
                else:
                    turnos_sucursal[indice_real] = {
                        "fecha": st.session_state.fecha_activa,
                        "hora": nueva_hora_completa,
                        "paciente": nuevo_nombre.strip(),
                        "motivo": nuevo_motivo.strip(),
                        "telefono": nuevo_tel.strip()
                    }
                    db_general[sucursal_activa] = turnos_sucursal
                    guardar_turnos_disco(db_general)
                    st.success("¡Turno actualizado con éxito!")
                    st.rerun()
    else:
        st.info("No hay consultas agendadas para esta fecha en esta sucursal.")

with col_der:
    st.markdown("### ⏰ Nueva Reserva")
    st.markdown(f"Sucursal: **{sucursal_activa}** | Fecha: **{st.session_state.fecha_activa}**")
    
    nombre_paciente = st.text_input("Nombre del Paciente", key=f"input_nombre_{sucursal_activa}")
    motivo_consulta = st.text_input("Motivo de la Consulta", key=f"input_motivo_{sucursal_activa}")
    telefono_paciente = st.text_input("Teléfono (WhatsApp)", key=f"input_tel_{sucursal_activa}", value="+598")
    
    st.markdown("#### Seleccionar Horario del Turno:")
    col_h, col_m_min = st.columns(2)
    with col_h:
        horas_disponibles = [f"{h:02d}" for h in range(8, 20)]
        hora_sel = st.selectbox("Hora", horas_disponibles, index=2, key=f"sel_h_{sucursal_activa}")
    with col_m_min:
        minutos_disponibles = ["00", "10", "20", "30", "40", "50"]
        minuto_sel = st.selectbox("Minutos", minutos_disponibles, index=0, key=f"sel_m_{sucursal_activa}")
        
    hora_seleccionada = f"{hora_sel}:{minuto_sel} hs"
    
    ocupado = any(t["fecha"] == st.session_state.fecha_activa and t["hora"] == hora_seleccionada for t in turnos_sucursal)
    
    st.markdown(f"**Horario elegido:** <span style='color: #60a5fa;'>{hora_seleccionada}</span>", unsafe_allow_html=True)
    
    if ocupado:
        st.button(f"🔴 Ocupado - {hora_seleccionada}", key=f"btn_ocupado_{sucursal_activa}", disabled=True, use_container_width=True)
        st.warning(f"⚠️ El horario seleccionado ({hora_seleccionada}) ya se encuentra ocupado en {sucursal_activa}.")
    else:
        if st.button(f"🟢 Confirmar Reserva ({hora_seleccionada})", key=f"btn_libre_{sucursal_activa}", use_container_width=True):
            ocupado_check = any(t["fecha"] == st.session_state.fecha_activa and t["hora"] == hora_seleccionada for t in turnos_sucursal)
            if ocupado_check:
                st.error(f"⚠️ Error: El horario {hora_seleccionada} ya fue ocupado.")
            elif nombre_paciente.strip():
                nuevo_t = {
                    "fecha": st.session_state.fecha_activa,
                    "hora": hora_seleccionada,
                    "paciente": nombre_paciente.strip(),
                    "motivo": motivo_consulta.strip() if motivo_consulta.strip() else "Consulta General",
                    "telefono": telefono_paciente.strip() if telefono_paciente.strip() else "+59800000000"
                }
                turnos_sucursal.append(nuevo_t)
                db_general[sucursal_activa] = turnos_sucursal
                guardar_turnos_disco(db_general)
                st.success(f"¡Turno confirmado para {nombre_paciente} a las {hora_seleccionada} en {sucursal_activa}!")
                st.rerun()
            else:
                st.warning("Ingrese el nombre del paciente antes de reservar.")