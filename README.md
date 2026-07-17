# Finanzas con Streamlit y Session State

Proyecto básico para explicar `st.session_state` a estudiantes que están
comenzando con Streamlit.

## Módulos

1. Interés simple.
2. Interés compuesto.
3. Pago mensual.

## Estructura

```text
streamlit_finanzas_session_state_simple/
├── app.py
├── funciones_financieras.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Importación de las funciones

```python
import funciones_financieras as ff
```

Las funciones se utilizan así:

```python
ff.interes_simple(...)
ff.interes_compuesto(...)
ff.pago_mensual(...)
```

## ¿Qué hace session_state?

`st.session_state` guarda valores mientras la sesión del usuario continúe.

Primero se crea la variable:

```python
if "simple_capital" not in st.session_state:
    st.session_state["simple_capital"] = 1000.0
```

Después, el widget recupera ese valor:

```python
capital_simple = st.number_input(
    "Capital inicial",
    value=st.session_state["simple_capital"],
    key="widget_simple_capital",
)
```

Finalmente, el valor ingresado se vuelve a guardar:

```python
st.session_state["simple_capital"] = capital_simple
```

La clave `widget_simple_capital` pertenece al widget.

La clave `simple_capital` conserva el dato aunque el usuario cambie de módulo.

## Instalación

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
streamlit run app.py
```

## Ejercicio para la clase

1. Cambiar los valores del interés simple.
2. Realizar el cálculo.
3. Ir al módulo de interés compuesto.
4. Regresar al interés simple.
5. Comprobar que los valores continúan guardados.
6. Abrir la sección `Ver datos guardados en session_state`.
