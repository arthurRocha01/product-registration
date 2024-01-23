# Importações
import pyautogui
import pandas as pd
import tabula
import sys
import os
import csv
from time import sleep

class Registrar:
    def __init__(self, data_file, margin, wait_time):
        self.data_file = data_file
        self.output_file = "output.csv"
        self.data_frame = pd.DataFrame()
        self.margin = margin
        self.wait_time = wait_time
        self.mouse_speed = 0.5
        self.max_iterations = int(sys.argv[4]) if len(sys.argv) > 3 else None
        pyautogui.FAILSAFE = True

         # Constantes x, y
        self.DADOS_FISCAIS = [706, 307]
        self.SAVE_POSITION = [562, 209]
        self.VALUES = [
            {"axis": [483, 308], "info": "Unnamed: 0"},  # NAME_POSITION
            {"axis": [449, 509], "info": "VALOR"},      # PRICE_POSITION
            {"axis": [587, 508], "info": self.margin},   # MARGIN_POSITION
            {"axis": [806, 296], "info": "500"},         # CSN_POSITION
            {"axis": [813, 342], "info": "0,19"},        # ICMS_POSITION
            {"axis": [816, 388], "info": "Unnamed: 1"},  # NCM_POSITION
        ]

    def register_product(self, product):
        print(f'''
    ---------------------------------
            {product}
    ---------------------------------
    ''')
        
        for value in self.VALUES:
            sleep(self.wait_time)
            pyautogui.moveTo(value["axis"][0], value["axis"][1], duration=self.mouse_speed)
            sleep(self.wait_time)

            print("click 2x")
            for i in range(0, 2):
                pyautogui.click()
            sleep(self.wait_time)

            if value["info"] in product:
                pyautogui.write(product[value["info"]])
                print(product[value["info"]])
                continue

            pyautogui.write(value["info"])
            print(value["info"])

            sleep(self.wait_time)
            pyautogui.moveTo(*self.SAVE_POSITION, duration=self.mouse_speed)
            print("save")

        print("----------------------------")

    def run(self):
        # Lê pdf
        print("Lendo arquivo...")
        try:
            pdf = tabula.read_pdf(self.data_file, pages="all", multiple_tables=True)
        except Exception as error:
            print(
            f"Ocorreu um erro durante a leitura do PDF {self.data_file}: {error}"
        )

        # Trata o data frame
        for table in pdf:
            if "CÓDIGO DO" in table:
                self.data_frame = pd.concat([self.data_frame, table], ignore_index=True)

        self.data_frame = self.data_frame[self.data_frame["VALOR"] != "UNITÁRIO"]
        self.data_frame = self.data_frame.astype(object)

        # Salva o csv
        print("Salvando arquivo...")
        try:
            self.data_frame.to_csv(self.output_file, index=False)
        except Exception as error:
            print(f"Ocorreu um erro ao salvar o DataFrame em {self.data_file}: {error}")

        # -----------------------> RPA <---------------------
            
        # Lê csv
        print("Abrindo arquivo...")
        try:
            with open(self.output_file, "r", encoding="utf-8") as file:
                products = list(csv.DictReader(file))
        except Exception as error:
             print(f"Ocorreu um erro ao abrir o arquivo CSV {self.data_file} para leitura: {error}")

        # Alerta 
        pyautogui.alert("ATENÇÃO!!: Não use mouse e tecla, pode atralhar o funcionamento.\nO RPA vai ser executado.")

        # Prepara o ambiente
        pyautogui.moveTo(*self.SAVE_POSITION, duration=self.mouse_speed)
        pyautogui.click()
        sleep(self.wait_time)
        pyautogui.moveTo(*self.DADOS_FISCAIS, duration=self.mouse_speed)
        pyautogui.click()
        sleep(self.wait_time)

        count_iteration = 0
        for product in products:
            self.register_product(product)

            count_iteration += 1
            if self.max_iterations is not None and count_iteration == self.max_iterations:
                break

                
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

    product_registrar = Registrar(full_path, margin, wait_time)
    product_registrar.run()


if __name__ == "__main__":
    main()