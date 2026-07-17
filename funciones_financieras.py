"""
Funciones financieras utilizadas por la aplicación.

Este archivo contiene únicamente las fórmulas.
La interfaz se encuentra en app.py.
"""


def interes_simple(capital, tasa_anual, tiempo_meses):
    """
    Calcula el interés simple y el monto final.
    """

    # Convertimos la tasa de porcentaje a decimal.
    tasa_decimal = tasa_anual / 100

    # Convertimos los meses a años.
    tiempo_anios = tiempo_meses / 12

    # Calculamos el interés simple.
    interes = capital * tasa_decimal * tiempo_anios

    # Calculamos el monto final.
    monto_final = capital + interes

    # Retornamos los dos resultados.
    return interes, monto_final


def interes_compuesto(capital, tasa_anual, tiempo_anios):
    """
    Calcula el interés compuesto con capitalización anual.
    """

    # Convertimos la tasa de porcentaje a decimal.
    tasa_decimal = tasa_anual / 100

    # Calculamos el monto final.
    monto_final = capital * (1 + tasa_decimal) ** tiempo_anios

    # Calculamos solamente el interés ganado.
    interes = monto_final - capital

    # Retornamos los dos resultados.
    return interes, monto_final


def pago_mensual(monto_prestamo, tasa_anual, plazo_anios):
    """
    Calcula la cuota mensual de un préstamo.
    """

    # Convertimos los años a meses.
    numero_pagos = plazo_anios * 12

    # Convertimos la tasa anual porcentual a una tasa mensual decimal.
    tasa_mensual = (tasa_anual / 100) / 12

    # Verificamos si la tasa es igual a cero.
    if tasa_mensual == 0:

        # Sin intereses, dividimos el préstamo para el número de meses.
        cuota_mensual = monto_prestamo / numero_pagos

    else:

        # Aplicamos la fórmula de una cuota mensual fija.
        cuota_mensual = (
            monto_prestamo
            * tasa_mensual
            * (1 + tasa_mensual) ** numero_pagos
            / ((1 + tasa_mensual) ** numero_pagos - 1)
        )

    # Calculamos el total pagado al finalizar el préstamo.
    total_pagado = cuota_mensual * numero_pagos

    # Calculamos cuánto se pagó únicamente por intereses.
    total_intereses = total_pagado - monto_prestamo

    # Retornamos los tres resultados.
    return cuota_mensual, total_pagado, total_intereses
