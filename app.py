"""
Aplicación básica para explicar st.session_state en Streamlit.

El código se encuentra escrito de manera lineal.
No se utilizan funciones auxiliares dentro de app.py.
"""

# Importamos Streamlit.
import streamlit as st

# Importamos el archivo de funciones con el alias ff.
import funciones_financieras as ff


# Configuramos la aplicación.
st.set_page_config(
    page_title="Finanzas con Session State",
    page_icon="💰",
    layout="centered",
)


# Título principal.
st.title("💰 Aplicación financiera")

# Explicación inicial.
st.write(
    "La aplicación permite cambiar de módulo sin perder los datos, "
    "gracias a `st.session_state`."
)


# ============================================================
# 1. VARIABLES INICIALES DE SESSION STATE
# ============================================================

# st.session_state funciona como una memoria temporal.
#
# Cada vez que Streamlit ejecuta nuevamente el código,
# primero revisamos si la variable ya existe.
#
# Si la variable no existe, la creamos.
# Si ya existe, no hacemos nada y conservamos su valor.


# Datos del módulo de interés simple.

if "simple_capital" not in st.session_state:
    st.session_state["simple_capital"] = 1000.0

if "simple_tasa" not in st.session_state:
    st.session_state["simple_tasa"] = 5.0

if "simple_meses" not in st.session_state:
    st.session_state["simple_meses"] = 12

if "simple_resultado" not in st.session_state:
    st.session_state["simple_resultado"] = None


# Datos del módulo de interés compuesto.

if "compuesto_capital" not in st.session_state:
    st.session_state["compuesto_capital"] = 1000.0

if "compuesto_tasa" not in st.session_state:
    st.session_state["compuesto_tasa"] = 5.0

if "compuesto_anios" not in st.session_state:
    st.session_state["compuesto_anios"] = 5

if "compuesto_resultado" not in st.session_state:
    st.session_state["compuesto_resultado"] = None


# Datos del módulo de pago mensual.

if "pago_monto" not in st.session_state:
    st.session_state["pago_monto"] = 10000.0

if "pago_tasa" not in st.session_state:
    st.session_state["pago_tasa"] = 10.0

if "pago_anios" not in st.session_state:
    st.session_state["pago_anios"] = 3

if "pago_resultado" not in st.session_state:
    st.session_state["pago_resultado"] = None


# ============================================================
# 2. NAVEGACIÓN ENTRE LOS MÓDULOS
# ============================================================

# Creamos un selectbox en la barra lateral.
modulo = st.sidebar.selectbox(
    "Seleccione un módulo",
    [
        "Interés simple",
        "Interés compuesto",
        "Pago mensual",
    ],
)


# ============================================================
# 3. MÓDULO DE INTERÉS SIMPLE
# ============================================================

if modulo == "Interés simple":

    st.header("Interés simple")

    st.info(
        "Cambie los valores, visite otro módulo y luego regrese."
    )

    # El widget toma como valor inicial lo almacenado en session_state.
    capital_simple = st.number_input(
        "Capital inicial ($)",
        min_value=0.0,
        step=100.0,
        value=st.session_state["simple_capital"],
        key="widget_simple_capital",
    )

    # Guardamos el valor ingresado en session_state.
    #
    # Esta línea conserva el dato aunque el widget deje de mostrarse.
    st.session_state["simple_capital"] = capital_simple


    # Campo para la tasa anual.
    tasa_simple = st.number_input(
        "Tasa anual (%)",
        min_value=0.0,
        step=0.5,
        value=st.session_state["simple_tasa"],
        key="widget_simple_tasa",
    )

    # Guardamos la tasa.
    st.session_state["simple_tasa"] = tasa_simple


    # Campo para el tiempo en meses.
    meses_simple = st.number_input(
        "Tiempo en meses",
        min_value=1,
        step=1,
        value=st.session_state["simple_meses"],
        key="widget_simple_meses",
    )

    # Guardamos el tiempo.
    st.session_state["simple_meses"] = meses_simple


    # Botón para realizar el cálculo.
    if st.button("Calcular interés simple"):

        # Utilizamos la función mediante el alias ff.
        interes, monto_final = ff.interes_simple(
            capital_simple,
            tasa_simple,
            meses_simple,
        )

        # Guardamos el resultado en session_state.
        st.session_state["simple_resultado"] = {
            "interes": interes,
            "monto_final": monto_final,
        }


    # Mostramos el resultado solamente si ya fue calculado.
    if st.session_state["simple_resultado"] is not None:

        resultado_simple = st.session_state["simple_resultado"]

        st.success(
            f"Interés generado: "
            f"${resultado_simple['interes']:,.2f}"
        )

        st.success(
            f"Monto final: "
            f"${resultado_simple['monto_final']:,.2f}"
        )


# ============================================================
# 4. MÓDULO DE INTERÉS COMPUESTO
# ============================================================

elif modulo == "Interés compuesto":

    st.header("Interés compuesto")

    # Campo para el capital.
    capital_compuesto = st.number_input(
        "Capital inicial ($)",
        min_value=0.0,
        step=100.0,
        value=st.session_state["compuesto_capital"],
        key="widget_compuesto_capital",
    )

    # Guardamos el capital.
    st.session_state["compuesto_capital"] = capital_compuesto


    # Campo para la tasa anual.
    tasa_compuesta = st.number_input(
        "Tasa anual (%)",
        min_value=0.0,
        step=0.5,
        value=st.session_state["compuesto_tasa"],
        key="widget_compuesto_tasa",
    )

    # Guardamos la tasa.
    st.session_state["compuesto_tasa"] = tasa_compuesta


    # Campo para el tiempo en años.
    anios_compuesto = st.number_input(
        "Tiempo en años",
        min_value=1,
        step=1,
        value=st.session_state["compuesto_anios"],
        key="widget_compuesto_anios",
    )

    # Guardamos el tiempo.
    st.session_state["compuesto_anios"] = anios_compuesto


    # Botón para realizar el cálculo.
    if st.button("Calcular interés compuesto"):

        interes, monto_final = ff.interes_compuesto(
            capital_compuesto,
            tasa_compuesta,
            anios_compuesto,
        )

        # Guardamos el resultado.
        st.session_state["compuesto_resultado"] = {
            "interes": interes,
            "monto_final": monto_final,
        }


    # Mostramos el resultado guardado.
    if st.session_state["compuesto_resultado"] is not None:

        resultado_compuesto = st.session_state["compuesto_resultado"]

        st.success(
            f"Interés generado: "
            f"${resultado_compuesto['interes']:,.2f}"
        )

        st.success(
            f"Monto final: "
            f"${resultado_compuesto['monto_final']:,.2f}"
        )


# ============================================================
# 5. MÓDULO DE PAGO MENSUAL
# ============================================================

else:

    st.header("Pago mensual")

    # Campo para el monto del préstamo.
    monto_prestamo = st.number_input(
        "Monto del préstamo ($)",
        min_value=0.01,
        step=500.0,
        value=st.session_state["pago_monto"],
        key="widget_pago_monto",
    )

    # Guardamos el monto.
    st.session_state["pago_monto"] = monto_prestamo


    # Campo para la tasa anual.
    tasa_prestamo = st.number_input(
        "Tasa anual (%)",
        min_value=0.0,
        step=0.5,
        value=st.session_state["pago_tasa"],
        key="widget_pago_tasa",
    )

    # Guardamos la tasa.
    st.session_state["pago_tasa"] = tasa_prestamo


    # Campo para el plazo.
    plazo_prestamo = st.number_input(
        "Plazo en años",
        min_value=1,
        step=1,
        value=st.session_state["pago_anios"],
        key="widget_pago_anios",
    )

    # Guardamos el plazo.
    st.session_state["pago_anios"] = plazo_prestamo


    # Botón para realizar el cálculo.
    if st.button("Calcular pago mensual"):

        cuota, total_pagado, total_intereses = ff.pago_mensual(
            monto_prestamo,
            tasa_prestamo,
            plazo_prestamo,
        )

        # Guardamos los resultados.
        st.session_state["pago_resultado"] = {
            "cuota": cuota,
            "total_pagado": total_pagado,
            "total_intereses": total_intereses,
        }


    # Mostramos el resultado guardado.
    if st.session_state["pago_resultado"] is not None:

        resultado_pago = st.session_state["pago_resultado"]

        st.success(
            f"Cuota mensual: "
            f"${resultado_pago['cuota']:,.2f}"
        )

        st.success(
            f"Total pagado: "
            f"${resultado_pago['total_pagado']:,.2f}"
        )

        st.success(
            f"Total de intereses: "
            f"${resultado_pago['total_intereses']:,.2f}"
        )


# ============================================================
# 6. OBSERVAR LOS DATOS GUARDADOS
# ============================================================

# Esta sección permite ver los valores permanentes.
with st.expander("Ver datos guardados en session_state"):

    st.write("### Interés simple")

    st.write(
        "Capital:",
        st.session_state["simple_capital"],
    )

    st.write(
        "Tasa:",
        st.session_state["simple_tasa"],
    )

    st.write(
        "Meses:",
        st.session_state["simple_meses"],
    )


    st.write("### Interés compuesto")

    st.write(
        "Capital:",
        st.session_state["compuesto_capital"],
    )

    st.write(
        "Tasa:",
        st.session_state["compuesto_tasa"],
    )

    st.write(
        "Años:",
        st.session_state["compuesto_anios"],
    )


    st.write("### Pago mensual")

    st.write(
        "Monto:",
        st.session_state["pago_monto"],
    )

    st.write(
        "Tasa:",
        st.session_state["pago_tasa"],
    )

    st.write(
        "Años:",
        st.session_state["pago_anios"],
    )
