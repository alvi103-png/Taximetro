import logging

from fare_config import load_fares
from log_config import setup_logging
from taximeter import Taximeter
from trip_history import load_today_trips, save_trip

logger = logging.getLogger(__name__)


def show_instructions() -> None:

    print("=" * 40)
    print("   🚕 ¡Bienvenido a tu taxímetro! 🚕")
    print("=" * 40)
    print("Sigue estas instrucciones para usarlo:\n")
    print("  e  →  Empezar una carrera")
    print("  p  →  Taxi parado")
    print("  m  →  Taxi en movimiento")
    print("  f  →  Finalizar carrera")
    print("  h  →  Ver carreras de hoy")
    print("  q  →  Salir del programa")

    print("\nEscribe la letra y pulsa Enter.")
    print("=" * 40)

def main() -> None:
    setup_logging()
    logger.info("Application started")

    try:
        stopped_rate, moving_rate = load_fares()
    except (OSError, ValueError, KeyError):
        logger.exception("Could not load fares from config file")
        print("Error: no se pudieron cargar las tarifas. Revisa config/fares.json.")
        return
    
    taximeter = Taximeter(stopped_rate, moving_rate)
    show_instructions()

    while True:

        command = input("\nComando: ").strip().lower()

        match command:

            case "e" if taximeter.in_progress:
                print("La carrera ya ha sido iniciada, si quieres finalizar presiona 'f'.")
                logger.warning("Start rejected: trip already in progress")

            case "e":
                taximeter.start()
                print("Carrera iniciada")
                logger.info("Trip started")

            case "p" | "m" | "f" if not taximeter.in_progress:
                print("Primero empieza carrera con 'e'.")
                logger.warning("Command '%s' rejected: no trip in progress", command)

            case "p":
                taximeter.set_moving(False)
                print("Taxi parado.")
                logger.info("Taxi stopped")

            case "m":
                taximeter.set_moving(True)
                print("Taxi en movimiento.")
                logger.info("Taxi moving")

            case "f":
                total = taximeter.finish()
                save_trip(taximeter.duration, total)
                total_text = f"{total:.2f}".replace(".", ",")
                print(f"Carrera finalizada. Total a cobrar: {total_text} €")
                logger.info("Trip finished, total: %.2f EUR", total)

            case "h":
                trips = load_today_trips()
                if not trips:
                    print("Hoy todavía no hay carreras.")
                else:
                    print("\nCarreras de hoy:")
                    day_total = 0.0
                    for trip in trips:
                        hour = trip["date"][11:16]
                        seconds = float(trip["duration_seconds"])
                        total = float(trip["total_eur"])
                        day_total += total
                        total_text = f"{total:.2f}".replace(".", ",")
                        print(f"  {hour}  |  {seconds:.0f} s  |  {total_text} €")
                    day_text = f"{day_total:.2f}".replace(".", ",")
                    print(f"Total del día: {day_text} € ({len(trips)} carreras)")
                logger.info("History requested: %d trips today", len(trips))

            case "q":
                print("Hasta luego!")
                logger.info("Application closed")
                break
            case _:
                print("Comando no válido.")
                logger.warning("Invalid command: %s", command)

if __name__ == "__main__":
    main()

