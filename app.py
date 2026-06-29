import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# Configuración de formato regional para números (Punto para miles, coma para decimales)
def formatear_numero(valor):
    try:
        texto = f"{valor:,.6f}".rstrip('0').rstrip('.')
        if ',' in texto or '.' in texto:
            comas_por_puntos = texto.replace(',', 'X').replace('.', ',').replace('X', '.')
            return comas_por_puntos
        return f"{valor:,}".replace(',', '.')
    except:
        return str(valor)

# --- MENÚ NAVEGADOR LATERAL ---
st.sidebar.title("Módulos")
modulo_seleccionado = st.sidebar.radio(
    "Seleccioná un módulo de trabajo:",
    ["Conversor de Unidades al SI", "Sedimentación por Gravedad", "Balance de masa para variación de concentraciones"]
)

st.markdown("---")

# ==========================================
# MÓDULO 1: CONVERSOR DE UNIDADES
# ==========================================
if modulo_seleccionado == "Conversor de Unidades al SI":
    st.title("Simulador de Operaciones Unitarias")
    st.subheader("Módulo: Megaconversor de Unidades al Sistema Internacional (SI)")
    st.write("Convertí cualquier unidad del sistema inglés o técnico a las unidades requeridas en el SI.")

    categorias = {
        "Longitud": ({"Pulgada (in)": 0.0254, "Pie (ft)": 0.3048, "Yarda (yd)": 0.9144, "Milla (mi)": 1609.344}, "m"),
        "Masa": ({"Onza (oz)": 0.028349523, "Libra (lb)": 0.45359237}, "kg"),
        "Superficie": ({"Pulgada cuadrada (in²)": 0.00064516, "Pie cuadrado (ft²)": 0.09290304, "Yarda cuadrada (yd²)": 0.83612736, "Milla cuadrada (mi²)": 2589988.11, "Acre": 4046.85642}, "m²"),
        "Volumen": ({"Pulgada cúbica (in³)": 0.000016387064, "Pie cúbico (ft³)": 0.0283168466, "Yarda cúbica (yd³)": 0.764554858, "Galón imperial (gal uk)": 0.00454609, "Cuarto imperial (qt uk)": 0.0011365225, "Pinta (pt)": 0.00056826125, "Onza líquida (fl oz)": 0.00002841306, "Barril (bbl)": 0.158987295}, "m³"),
        "Fuerza": ({"Dina (dyn)": 1e-5, "Libra fuerza (lbf)": 4.44822162}, "N"),
        "Energía / Trabajo": ({"Caloría (cal)": 4.184, "BTU": 1055.05585, "Libra fuerza pulgada (lbf·in)": 0.112984829, "Libra fuerza pie (lbf·ft)": 1.35581795}, "J"),
        "Potencia": ({"Caballo de fuerza (hp)": 745.699872, "BTU/h": 0.29307107}, "W"),
        "Presión": ({"Atmósfera (atm)": 101325.0, "Torricelli / mmHg": 133.322368, "Bar": 100000.0, "Psi (lbf/in²)": 6894.75729}, "Pa"),
        "Velocidad": ({"Pulgada por segundo (in/s)": 0.0254, "Pie por segundo (ft/s)": 0.3048, "Milla por hora (mi/h)": 0.44704, "Nudo (kt)": 0.514444444}, "m/s"),
        "Caudal Volumétrico": ({"Galón por segundo (gps)": 0.00378541178}, "m³/s"),
        "Viscosidad Dinámica": ({"Poise (P)": 0.1, "Centipoise (cP)": 0.001}, "Pa·s")
    }

    lista_opciones = list(categorias.keys()) + ["Temperatura"]
    categoria_seleccionada = st.selectbox("1. Seleccioná la variable física que querés calcular:", lista_opciones)

    st.markdown("---")

    if categoria_seleccionada != "Temperatura":
        st.subheader(f"Conversor de {categoria_seleccionada}")
        unidades_dict, unidad_si = categorias[categoria_seleccionada]
        
        col1, col2 = st.columns(2)
        with col1:
            unidad_origen = st.selectbox("Unidad de origen:", list(unidades_dict.keys()))
            valor_ingresado = st.number_input("Ingresá el valor numérico:", value=1.0, step=1.0, format="%.6f")
            
        factor = unidades_dict[unidad_origen]
        resultado_si = valor_ingresado * factor
        
        with col2:
            st.write(f"### Equivalencia en el SI ({unidad_si}):")
            st.info(f"**{formatear_numero(resultado_si)}** {unidad_si}")
    else:
        st.subheader("Conversor de Temperatura")
        col1, col2 = st.columns(2)
        with col1:
            unidad_temp = st.selectbox("Seleccioná la escala de origen:", ["Celsius (°C)", "Fahrenheit (°F)", "Rankine (°R)"])
            valor_temp = st.number_input("Ingresá la temperatura:", value=25.0, step=1.0, format="%.2f")
            
        if "Celsius" in unidad_temp:
            resultado_k = valor_temp + 273.15
        elif "Fahrenheit" in unidad_temp:
            resultado_k = (valor_temp - 32) * 5/9 + 273.15
        else:
            resultado_k = valor_temp * 5/9
            
        with col2:
            st.write("### Equivalencia en el SI (K):")
            st.info(f"**{formatear_numero(resultado_k)}** K")

# ==========================================
# MÓDULO 2: SEDIMENTACIÓN POR GRAVEDAD
# ==========================================
elif modulo_seleccionado == "Sedimentación por Gravedad":
    st.title("Módulo: Sedimentación por Gravedad")
    
    sub_bloque = st.selectbox(
        "Seleccioná el sub-bloque de cálculo:",
        ["Criterio para determinar régimen del flujo", "Cálculo de velocidad terminal y velocidad de asentamiento"]
    )
    
    st.markdown("---")
    
    st.write("### Datos generales del sistema (Unidades del SI):")
    col1, col2 = st.columns(2)
    with col1:
        Dp = st.number_input("Diámetro de la partícula, Dp (m):", min_value=0.0, value=0.0001, step=0.00001, format="%.6f", key="sed_Dp")
        g = st.number_input("Aceleración de la gravedad, g (m/s²):", min_value=0.0, value=9.80665, step=0.01, format="%.5f", key="sed_g")
        mu = st.number_input("Viscosidad del fluido, μ (Pa·s):", min_value=1e-7, value=0.001, step=0.0001, format="%.6f", key="sed_mu")
    with col2:
        rho = st.number_input("Densidad del fluido, ρ (kg/m³):", min_value=0.0, value=1000.0, step=10.0, format="%.2f", key="sed_rho")
        rho_p = st.number_input("Densidad de la partícula, ρp (kg/m³):", min_value=0.0, value=2500.0, step=10.0, format="%.2f", key="sed_rhop")

    st.markdown("---")

    # --- SUB-BLOQUE 1: CRITERIO K ---
    if sub_bloque == "Criterio para determinar régimen del flujo":
        st.subheader("Sub-bloque: Criterio para determinar régimen del flujo")
        
        if rho_p > rho:
            termino_interno = (g * rho * (rho_p - rho)) / (mu ** 2)
            K = Dp * (termino_interno ** (1/3))
            
            st.write("### Resultado del Parámetro K:")
            st.metric(label="Valor calculado de K", value=formatear_numero(K))
            
            if K < 2.6:
                st.success("📢 **Régimen de Stokes**")
            elif 2.6 <= K <= 68.9:
                st.warning("📢 **Región de transición**")
            elif 68.9 < K <= 2360:
                st.info("📢 **Régimen de Newton**")
            else:
                st.error("⚠️ **Fuera de rango:** El valor de K supera el límite superior de Newton (K > 2360).")
        else:
            st.error("La densidad de la partícula (ρp) debe ser mayor que la densidad del fluido (ρ).")
            
        st.markdown("---")
        st.caption("Bibliografía en página 185, McCabe")

    # --- SUB-BLOQUE 2: VELOCIDAD TERMINAL Y DE ASENTAMIENTO ---
    elif sub_bloque == "Cálculo de velocidad terminal y velocidad de asentamiento":
        st.subheader("Sub-bloque: Cálculo de velocidad terminal y velocidad de asentamiento")
        
        ut_calculada = 0.0
        
        if rho_p > rho:
            st.write("## 1. Cálculo de la Velocidad Terminal ($u_t$)")
            regimen_calculo = st.radio(
                "Seleccioná el régimen para realizar el cálculo de ut:",
                ["Régimen de Stokes", "Región de transición", "Régimen de Newton"],
                horizontal=True
            )
            
            # --- EVALUACIÓN DE LAS 3 OPCIONES ---
            if regimen_calculo == "Régimen de Stokes":
                ut_calculada = (g * (Dp ** 2) * (rho_p - rho)) / (18 * mu)
                Re_final = (Dp * ut_calculada * rho) / mu
                
                st.write("### Resultados Calculados (Stokes):")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.metric(label="Velocidad Terminal (ut)", value=f"{formatear_numero(ut_calculada)} m/s")
                with col_s2:
                    st.metric(label="Número de Reynolds recalculado (Re)", value=formatear_numero(Re_final))
                    
            elif regimen_calculo == "Región de transición":
                st.write("### Iteración Manual (Pasos del Alumno):")
                st.info("1️⃣ Buscá el Coeficiente de Arrastre ($C_D$) en la gráfica inferior usando tu Reynolds estimado.\n\n2️⃣ Cargá ese valor acá abajo para resolver la velocidad terminal real.")
                
                col_it1, col_it2 = st.columns(2)
                with col_it1:
                    re_propuesto = st.number_input("Número de Reynolds propuesto (Rep):", min_value=0.0, value=10.0, step=1.0, format="%.2f")
                with col_it2:
                    Cd_propuesto = st.number_input("Coeficiente de Arrastre propuesto (Cd):", min_value=1e-4, value=2.0, step=0.1, format="%.4f")
                
                if Cd_propuesto > 0:
                    ut_calculada = math.sqrt((4 * g * (rho_p - rho) * Dp) / (3 * Cd_propuesto * rho))
                    Re_recalculado = (Dp * ut_calculada * rho) / mu
                    
                    st.markdown("---")
                    st.write("### Resultados de la Iteración:")
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.metric(label="Velocidad Terminal resultante (ut)", value=f"{formatear_numero(ut_calculada)} m/s")
                    with col_r2:
                        st.metric(label="Número de Reynolds verificado (Re)", value=formatear_numero(Re_recalculado))
                        
                    st.caption(f"💡 *Compará tu 'Reynolds propuesto' ({formatear_numero(re_propuesto)}) con el 'Reynolds verificado' ({formatear_numero(Re_recalculado)}) para validar tu lectura de la gráfica.*")
                
                st.markdown("---")
                nombre_imagen = "grafica_mccabe.png"
                if os.path.exists(nombre_imagen):
                    st.image(nombre_imagen, caption="Fig. 7.7, McCabe", use_container_width=True)
                else:
                    st.warning(f"Falta el archivo visual: Guardá la imagen como '{nombre_imagen}' en la carpeta de tu proyecto.")
                
            elif regimen_calculo == "Régimen de Newton":
                ut_calculada = 1.75 * math.sqrt((g * Dp * (rho_p - rho)) / rho)
                Re_final = (Dp * ut_calculada * rho) / mu
                
                st.write("### Resultados Calculados (Newton):")
                col_n1, col_n2 = st.columns(2)
                with col_n1:
                    st.metric(label="Velocidad Terminal (ut)", value=f"{formatear_numero(ut_calculada)} m/s")
                with col_n2:
                    st.metric(label="Número de Reynolds verificado (Re)", value=formatear_numero(Re_final))

            # --- SECCIÓN: VELOCIDAD DE ASENTAMIENTO IMPEDIDO ---
            st.markdown("---")
            st.write("## 2. Cálculo de la Velocidad de Asentamiento ($u_s$)")
            st.write("Ingresá los parámetros de concentración y el exponente experimental leídos de la FIGURA 7.8:")

            col_as1, col_as2 = st.columns(2)
            with col_as1:
                ut_input = st.number_input("Velocidad terminal de partida, ut (m/s):", min_value=0.0, value=ut_calculada, step=0.001, format="%.6f")
                epsilon = st.number_input("Fracción de vacío / Porosidad (ε):", min_value=1e-4, max_value=1.0, value=0.7, step=0.05, format="%.4f")
            with col_as2:
                n_exponente = st.number_input("Exponente experimental (n):", min_value=0.0, value=3.5, step=0.1, format="%.2f")

            us_resultado = ut_input * (epsilon ** n_exponente)

            st.write("### Resultado de la Velocidad de Asentamiento:")
            st.success(f"**Velocidad de asentamiento calculada (us):** {formatear_numero(us_resultado)} m/s")

            st.markdown("---")
            nombre_imagen_78 = "grafica_mccabe_78.png"
            if os.path.exists(nombre_imagen_78):
                st.image(nombre_imagen_78, caption="FIGURA 7.8, McCabe", use_container_width=True)
            else:
                st.warning(f"Falta el archivo de la curva de porosidad: Guardá la imagen como '{nombre_imagen_78}' en tu carpeta para verla.")
                st.error("La densidad de la partícula (ρp) debe ser mayor que la densidad del fluido (ρ).")
                st.markdown("---")
                st.caption("Bibliografía: Capítulo 7, McCabe")
            
           

        # ==========================================
# ACÁ EMPIEZA EL TERCER SUB-BLOQUE
# ==========================================



# Estilo personalizado
st.markdown("""
    <style>
    .pink-box {
        background-color: #FFE4E1;
        padding: 12px;
        border-radius: 8px;
        color: #5D4037;
        margin-bottom: 15px;
        border: 1px solid #FFC0CB;
    }
    .unit-hint {
        color: #BC8F8F;
        font-size: 0.85rem;
        margin-top: -15px;
        margin-bottom: 10px;
        font-weight: 500;
    }
    .validation-hint {
        color: #8B4513;
        font-size: 0.8rem;
        margin-top: -10px;
        margin-bottom: 15px;
        font-style: italic;
    }
    /* Centrado de imagen */
    .stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .footer-container {
        width: 100%;
        display: flex;
        justify-content: center;
        padding-top: 50px;
    }
    /* Alineación vertical de inputs en el sidebar */
    [data-testid="stVerticalBlock"] > div > div > [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

def fmt(valor, decimales=2):
    try:
        if valor is None: return "0,00"
        s = f"{valor:,.{decimales}f}"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(valor)


def main():
    st.title("🧪Balance de masa para variación de concentraciones")
    
    st.markdown('<div class="pink-box">💡 <b>Supuestos:</b> Buen mezclado; no hay reacciones químicas; densidades homogéneas entre contenido inicial del recipiente y flujos de circulación.</div>', unsafe_allow_html=True)

    st.header("📥 Configuración de Variables")

    m_conv = {"kg": 1.0, "g": 0.001, "lb": 0.453592}
    v_conv = {"m3": 1.0, "L": 0.001, "gal": 0.00378541}
    t_conv = {"s": 1.0, "min": 60.0, "h": 3600.0, "d": 86400.0}

    # 1. CONTENIDO DEL RECIPIENTE
    st.subheader("1. Contenido del Recipiente")
    c_v1, c_v2 = st.columns([2, 1])
    v0_input = c_v1.number_input("Cantidad inicial", value=100.0, step=0.1, key="v0_val")
    v0_unit = c_v2.selectbox("Unidad", ["kg", "g", "L", "m3", "gal", "lb"], key="u_v0")
    
    # 2. DENSIDAD
    st.subheader("2. Densidad (ρ)")
    c_r1, c_r2 = st.columns([2, 1])
    rho_input = c_r1.number_input("Valor de ρ", value=1000.0, step=0.1, key="rho_val")
    rho_unit = c_r2.selectbox("Unidad", ["kg/m³", "g/cm³"], key="u_rho")
    rho_si = rho_input if rho_unit == "kg/m³" else rho_input * 1000.0
    st.markdown(f'<p class="unit-hint">SI: {fmt(rho_si)} kg/m³</p>', unsafe_allow_html=True)

    M0 = v0_input * m_conv[v0_unit] if v0_unit in m_conv else v0_input * v_conv[v0_unit] * rho_si
    st.markdown(f'<p class="unit-hint">SI: {fmt(M0, 3)} kg</p>', unsafe_allow_html=True)

    # 3. COMPONENTE DE INTERÉS
    st.subheader("3. Componente de Interés")
    c_d1, c_d2 = st.columns([2, 1])
    d0_input = c_d1.number_input("Cantidad inicial (compuesto)", value=10.0, step=0.1, key="d0_val")
    d0_unit = c_d2.selectbox("Unidad", ["kg", "g", "lb", "L"], key="u_d0")
    
    D0 = d0_input * v_conv["L"] * rho_si if d0_unit == "L" else d0_input * m_conv[d0_unit]
    st.markdown(f'<p class="unit-hint">SI: {fmt(D0, 3)} kg</p>', unsafe_allow_html=True)

    c0_manual = st.number_input("Concentración Inicial (opcional)", value=0.0, format="%.4f", step=0.0001)
    st.markdown('<p class="validation-hint">Concentración solicitada en proporción masa en masa. <br> En caso de no cargar concentración inicial, se requiere completar el campo precedente de Cantidad inicial del compuesto</p>', unsafe_allow_html=True)
    
    C0 = c0_manual if c0_manual > 0 else (D0 / M0 if M0 > 0 else 0.0)
    st.markdown(f'<p class="unit-hint">Concentración calculada: {fmt(C0, 4)} kg/kg</p>', unsafe_allow_html=True)

    # 4. FLUJOS
    st.subheader("4. Flujos")
    flow_units = ["kg/s", "kg/min", "kg/h", "L/s", "L/min", "L/h", "gal/min", "lb/min"]
    cf1, cf2 = st.columns([2, 1])
    fe_val = cf1.number_input("Flujo de Entrada", value=1.0, format="%.3f", step=0.001, key="fe_val")
    fe_unit = cf2.selectbox("Unidad", flow_units, key="u_fe")
    
    def to_kg_s_fixed(val, unit, dens, mc, vc, tc):
        u_b, u_t = unit.split('/')
        mass = val * mc[u_b] if u_b in mc else val * vc[u_b] * dens
        return mass / tc[u_t]

    Fe_si = to_kg_s_fixed(fe_val, fe_unit, rho_si, m_conv, v_conv, t_conv)
    st.markdown(f'<p class="unit-hint">SI: {fmt(Fe_si, 5)} kg/s</p>', unsafe_allow_html=True)

    cf3, cf4 = st.columns([2, 1])
    fs_val = cf3.number_input("Flujo de Salida", value=1.0, format="%.3f", step=0.001, key="fs_val")
    fs_unit = cf4.selectbox("Unidad", flow_units, key="u_fs")
    Fs_si = to_kg_s_fixed(fs_val, fs_unit, rho_si, m_conv, v_conv, t_conv)
    st.markdown(f'<p class="unit-hint">SI: {fmt(Fs_si, 5)} kg/s</p>', unsafe_allow_html=True)

    # 5. PARÁMETROS SIMULACIÓN
    st.subheader("5. Parámetros de Simulación")
    ce_input = st.number_input("Concentración de Entrada", value=0.1, format="%.4f", step=0.0001)
    st.markdown('<p class="validation-hint">concentración solicitada en proporción masa en masa</p>', unsafe_allow_html=True)
    
    c_t1, c_t2 = st.columns([2, 1])
    t_input = c_t1.number_input("Tiempo total", value=60.0, step=1.0, key="t_val")
    t_unit = c_t2.selectbox("Unidad", ["s", "min", "h", "d"], key="u_t")
    T_max = t_input * t_conv[t_unit]

    # --- CÁLCULO ---
    t_steps = np.linspace(0, T_max, 1000)
    dt = t_steps[1] - t_steps[0]
    M_t, C_t = [M0], [C0]

    for i in range(len(t_steps)-1):
        # Masa total del sistema (t)
        M_next = M_t[-1] + (Fe_si - Fs_si) * dt
        M_t.append(max(M_next, 1e-6))
        
        # Variación de concentración dC/dt
        dCdt = (Fe_si * (ce_input - C_t[-1])) / M_t[-1]
        C_next = C_t[-1] + dCdt * dt
        C_t.append(max(C_next, 0))

    M_t = np.array(M_t)
    C_t = np.array(C_t)
    # CORRECCIÓN SOLICITADA: Masa del compuesto = C(t) * M_sistema(t)
    D_t = C_t * M_t

    # --- RESULTADOS ---
    st.subheader("📊 Análisis de Masa")
    delta_m = M_t[-1] - M0
    if abs(Fe_si - Fs_si) < 1e-7:
        st.markdown(f'<div class="pink-box">✅ <b>Estado Estacionario:</b> Masa constante en {fmt(M0)} kg.</div>', unsafe_allow_html=True)
    else:
        txt = "aumentó" if delta_m > 0 else "disminuyó"
        st.markdown(f'<div class="pink-box">⚖️ <b>Sistema Dinámico:</b> La masa total del sistema {txt} {fmt(abs(delta_m))} kg.</div>', unsafe_allow_html=True)

    # --- GRÁFICAS ---
    st.divider()
    col_g1, col_g2 = st.columns(2)
    
    x_formatter = plt.FuncFormatter(lambda x, p: fmt(x, 1))

    with col_g1:
        fig1, ax1 = plt.subplots()
        ax1.plot(t_steps / t_conv[t_unit], C_t, color='#FFC0CB', lw=2)
        ax1.set_title("Concentración vs Tiempo")
        ax1.set_xlabel(f"Tiempo [{t_unit}]")
        ax1.set_ylabel("Concentración [kg/kg]")
        ax1.xaxis.set_major_formatter(x_formatter)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: fmt(x, 3)))
        st.pyplot(fig1)
        st.metric(label=f"Concentración final (t={fmt(t_input, 1)})", value=f"{fmt(C_t[-1], 3)} kg/kg")

    with col_g2:
        fig2, ax2 = plt.subplots()
        ax2.plot(t_steps / t_conv[t_unit], D_t, color='#B2EC5D', lw=2)
        ax2.set_title("Masa del Compuesto vs Tiempo")
        ax2.set_xlabel(f"Tiempo [{t_unit}]")
        ax2.set_ylabel("Masa [kg]")
        ax2.xaxis.set_major_formatter(x_formatter)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: fmt(x, 1)))
        st.pyplot(fig2)
        st.metric(label=f"Masa final del compuesto (t={fmt(t_input, 1)})", value=f"{fmt(D_t[-1], 3)} kg")

    # --- FOOTER ---
    if os.path.exists("footer_image.png"):
        st.markdown('<div class="footer-container">', unsafe_allow_html=True)
        st.image("footer_image.png", width=500)
        st.markdown('</div>', unsafe_allow_html=True)

if modulo_seleccionado == "Balance de masa para variación de concentraciones":
    main()