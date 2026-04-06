import csv
from pathlib import Path
from datetime import datetime


def cargar_transacciones(ruta_csv: str):
    """
    Carga las transacciones desde un CSV y convierte tipos básicos.
    """
    ruta = Path(ruta_csv)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    transacciones = []

    with ruta.open("r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            transaccion = {
                "id": int(fila["id"]),
                "wallet_origen": fila["wallet_origen"],
                "wallet_destino": fila["wallet_destino"],
                "importe": float(fila["importe"]),
                "fecha": datetime.strptime(fila["fecha"], "%Y-%m-%d %H:%M"),
            }
            transacciones.append(transaccion)

    return transacciones