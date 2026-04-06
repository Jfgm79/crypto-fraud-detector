from collections import defaultdict
from config import (
    MIN_DESTINOS_SOSPECHOSOS,
    MIN_ORIGENES_SOSPECHOSOS,
    VENTANA_MINUTOS,
    SCORE_DISPERSION,
    SCORE_RECEPTORA_AGREGADORA,
)


def detectar_dispersion_wallets(transacciones):
    """
    Detecta wallets que envían fondos a múltiples destinos distintos
    en una ventana corta de tiempo.
    """
    agrupadas_por_origen = defaultdict(list)

    for tx in transacciones:
        agrupadas_por_origen[tx["wallet_origen"]].append(tx)

    alertas = []

    for wallet_origen, movimientos in agrupadas_por_origen.items():
        movimientos_ordenados = sorted(movimientos, key=lambda x: x["fecha"])

        for i in range(len(movimientos_ordenados)):
            base = movimientos_ordenados[i]
            destinos = {base["wallet_destino"]}
            grupo = [base]

            for j in range(i + 1, len(movimientos_ordenados)):
                candidata = movimientos_ordenados[j]
                diferencia = candidata["fecha"] - base["fecha"]
                minutos = diferencia.total_seconds() / 60

                if minutos <= VENTANA_MINUTOS:
                    destinos.add(candidata["wallet_destino"])
                    grupo.append(candidata)
                else:
                    break

            if len(destinos) >= MIN_DESTINOS_SOSPECHOSOS:
                alerta = {
                    "wallet_origen": wallet_origen,
                    "destinos_distintos": len(destinos),
                    "transacciones": grupo,
                    "score": SCORE_DISPERSION,
                    "tipo_alerta": "Posible dispersión de fondos a múltiples wallets",
                }
                alertas.append(alerta)
                break

    return alertas


def detectar_wallets_receptoras_agregadoras(transacciones):
    """
    Detecta wallets destino que reciben fondos desde múltiples orígenes
    distintos en una ventana corta de tiempo.
    """
    agrupadas_por_destino = defaultdict(list)

    for tx in transacciones:
        agrupadas_por_destino[tx["wallet_destino"]].append(tx)

    alertas = []

    for wallet_destino, movimientos in agrupadas_por_destino.items():
        movimientos_ordenados = sorted(movimientos, key=lambda x: x["fecha"])

        for i in range(len(movimientos_ordenados)):
            base = movimientos_ordenados[i]
            origenes = {base["wallet_origen"]}
            grupo = [base]

            for j in range(i + 1, len(movimientos_ordenados)):
                candidata = movimientos_ordenados[j]
                diferencia = candidata["fecha"] - base["fecha"]
                minutos = diferencia.total_seconds() / 60

                if minutos <= VENTANA_MINUTOS:
                    origenes.add(candidata["wallet_origen"])
                    grupo.append(candidata)
                else:
                    break

            if len(origenes) >= MIN_ORIGENES_SOSPECHOSOS:
                alerta = {
                    "wallet_destino": wallet_destino,
                    "origenes_distintos": len(origenes),
                    "transacciones": grupo,
                    "score": SCORE_RECEPTORA_AGREGADORA,
                    "tipo_alerta": "Posible wallet receptora agregadora",
                }
                alertas.append(alerta)
                break

    return alertas