import pyregister
import sys
import os

                
def main():
    if len(sys.argv) < 3:
        print("Use: python register_product.py arquivo.csv")
        sys.exit(1)

    print("Iniciando...")
    # Obtêm o caminho
    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, sys.argv[1])

    margin = sys.argv[2]
    wait_time = float(sys.argv[3])
    max_iterations = int(sys.argv[4]) if len(sys.argv) > 3 else None

    product_registrar = pyregister.Registrar(full_path, margin, wait_time, max_iterations)
    product_registrar.run()


if __name__ == "__main__":
    main()