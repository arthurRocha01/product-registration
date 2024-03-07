import pyregister
import sys
import os

def get_download_directory(filename):
    user_home = os.path.expanduser("~")
    if os.name == "nt" or os.name == "posix":
        return os.path.join(user_home, "Downloads", filename)
    else:
        return os.path.join(os.getcwd(), filename)

                
def main():
    if len(sys.argv) < 3:
        print("Use: python register_product.py arquivo.csv")
        sys.exit(1)

    print("Iniciando...")
    # Obtêm o caminho
    full_path = get_download_directory(sys.argv[1])
    margin = sys.argv[2]
    wait_time = float(sys.argv[3])
    max_iterations = None
    logger = pyregister.Logger()
    if len(sys.argv) == 5:
        max_iterations = int(sys.argv[4])

    product_registrar = pyregister.Registrar(full_path, margin, wait_time, max_iterations, logger)
    product_registrar.run()


if __name__ == "__main__":
    main()