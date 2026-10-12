from taximeter import Taximeter

STOPPED_RATE = 0.02
MOVING_RATE = 0.05

def show_instructions() -> None:

    print("=" * 40)
    print("   🚕 ¡Bienvenido a tu taxímetro! 🚕")
    print("=" * 40)
    print("Sigue estas instrucciones para usarlo:\n")
    print("  e  →  Empezar una carrera")
    print("  p  →  Taxi parado")
    print("  m  →  Taxi en movimiento")
    print("  q  →  Salir del programa")

    print("\nEscribe la letra y pulsa Enter.")
    print("=" * 40)

def main() -> None:
    taximeter = Taximeter(STOPPED_RATE, MOVING_RATE)
    show_instructions()

    while True:

        command = input("\nComando: ").strip().lower()

        match command:

            case "e":
                taximeter.start()
                print("Carrera iniciada")
            case "p":
                taximeter.set_moving(False)
                print("Taxi parado.")
            case "m":
                taximeter.set_moving(True)
                print("Taxi en movimiento.")
            case "q":
                print("Hasta luego!")
                break
            case _:
                print("Comando no válido.")

if __name__ == "__main__":
    main()

