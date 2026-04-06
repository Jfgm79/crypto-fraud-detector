"""Configuración de reglas y scoring del detector."""

# Regla 1: dispersión desde una wallet origen a múltiples destinos.
MIN_DESTINOS_SOSPECHOSOS = 3
SCORE_DISPERSION = 3

# Regla 2: wallet destino que agrega fondos desde múltiples orígenes.
MIN_ORIGENES_SOSPECHOSOS = 3
SCORE_RECEPTORA_AGREGADORA = 3

# Ventana temporal (en minutos) compartida por las reglas.
VENTANA_MINUTOS = 15


def clasificar_riesgo(score):
    if score >= 3:
        return "Riesgo alto"
    if score >= 2:
        return "Riesgo medio"
    return "Riesgo bajo"
