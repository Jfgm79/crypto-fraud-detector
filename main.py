from utils import cargar_transacciones
from detector import (
    detectar_dispersion_wallets,
    detectar_wallets_receptoras_agregadoras,
)
from config import clasificar_riesgo


def main():
    ruta_csv = "data/transactions.csv"

    transacciones = cargar_transacciones(ruta_csv)
    alertas_dispersion = detectar_dispersion_wallets(transacciones)
    alertas_receptoras = detectar_wallets_receptoras_agregadoras(transacciones)
    alertas = alertas_dispersion + alertas_receptoras

    print("=" * 60)
    print("CRYPTO FRAUD DETECTOR")
    print("=" * 60)
    print()

    print(f"Transacciones analizadas: {len(transacciones)}")
    print(f"Alertas detectadas: {len(alertas)}")
    print()

    if not alertas:
        print("No se detectaron patrones sospechosos.")
        return

    for alerta in alertas:
        print("-" * 60)
        print(f"Tipo de alerta: {alerta['tipo_alerta']}")
        if "wallet_origen" in alerta:
            print(f"Wallet origen: {alerta['wallet_origen']}")
            print(f"Destinos distintos: {alerta['destinos_distintos']}")
        else:
            print(f"Wallet destino: {alerta['wallet_destino']}")
            print(f"Orígenes distintos: {alerta['origenes_distintos']}")

        print(f"Score de riesgo: {alerta['score']}")

        nivel = clasificar_riesgo(alerta["score"])
        print(f"Nivel de riesgo: {nivel}")

        print("Transacciones relacionadas:")

        for tx in alerta["transacciones"]:
            print(
                f"  ID {tx['id']} | "
                f"{tx['fecha'].strftime('%Y-%m-%d %H:%M')} | "
                f"{tx['wallet_origen']} -> {tx['wallet_destino']} | "
                f"{tx['importe']} ETH"
            )

        print()


if __name__ == "__main__":
    main()