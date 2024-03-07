# Importações
import os
import csv
from time import sleep
import logging
import pyautogui


# Limpa o terminal
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# Registra todos os logs do programa e printa no terminal
class Logger:
    def __init__(self, filename="log.txt", level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        formater = logging.Formatter("%(asctime)s / %(levelname)s: %(message)s")

        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formater)

        self.logger.addHandler(file_handler)

    def log(self, message, level=logging.INFO):
        self.logger.log(level, message)
        print(message)


# Captura as coordenadas do campo desejado
class UserInteraction:
    def __init__(self, logger):
        self.logger = logger

    def alert_user(self, message):
        self.logger.log(message)

    def get_coordinates(self, name):
        self.alert_user("Você tem 3 segundos para marcar o ponto desejado...")
        sleep(3)
        x, y = pyautogui.position()
        self.alert_user(f"{name}: Coordenadas {x}, {y} registradas.")
        return x, y

class Registrar:
    def __init__(self, input_file, margin, wait_time, max_iterations=None, logger=None):
        self.input_file = input_file
        self.margin = margin
        self.wait_time = wait_time
        self.max_iterations = max_iterations
        self.logger = logger
        self.mouse_speed = 0.5
        pyautogui.FAILSAFE = True

        # Coordenadas dos campos
        self.DADOS_FISCAIS = [706, 307]
        self.SAVE = [562, 209]
        self.CONFIRMATION = [669,443]
        COLUMNS = ["nome", "valor", "margin", "cst", "taxa", "ncm"]
        self.user_interaction = UserInteraction(logger)

        # Estrutura dos valores
        self.FIELDS = []

        # Armazena as coordenadas do campo e valores do produto na estrutura
        for col in COLUMNS:
            coordinates = self.user_interaction.get_coordinates(col)
            self.FIELDS.append({"axis": coordinates, "info": col})

    def register_product(self, product):
        for field in self.FIELDS:
            x, y = field["axis"]

            # Move o mouse para os campos escolhidos
            sleep(self.wait_time)
            pyautogui.moveTo(x, y, duration=self.mouse_speed)

            # Clica duas vezes no campo
            pyautogui.click(clicks=2)
            sleep(self.wait_time)

            # Escreve o valor
            if field["info"] == "margin":
                pyautogui.write(self.margin)
                self.logger.log(f"margin: {self.margin}")
            else:
                key = field["info"]
                pyautogui.write(product[key].replace('.', ','))
                self.logger.log(f"{field['info']}: {product[key]}")

        # Salva o produto
        self.click_and_wait(self.SAVE)

        # Confirma a salvação
        self.click_and_wait(self.CONFIRMATION, 'Produto salvo!')

        self.logger.log("*****--*****--*****-*****--*****--*****--*****--*****")
        self.logger.log("\n\n")

    def click_and_wait(self, cordinates, action=None):
        pyautogui.moveTo(*cordinates, duration=self.wait_time)
        pyautogui.click()
        sleep(self.wait_time)
        if action:
            self.logger.log(action)

    def run(self):
        # Lê csv
        self.logger.log("Abrindo arquivo...")
        try:
            with open(self.input_file, "r", encoding="utf-8") as file:
                products = list(csv.DictReader(file))
        except Exception as error:
            self.logger.log(f"Ocorreu um erro ao abrir o arquivo CSV {self.input_file} para leitura: {error}")

        # Limpa o terminal
        clear_screen()

        # Alerta
        pyautogui.alert("ATENÇÃO!!: Não use mouse e tecla, pode atrapalhar o funcionamento.\nO RPA vai ser executado.")
        self.logger.log("Iniciando...")
        self.logger.log("\n")

        # Prepara o ambiente
        self.click_and_wait(self.DADOS_FISCAIS)

        # Cadastra cada produto
        count_iteration = 0
        for product in products:
            self.register_product(product)
            count_iteration += 1
            if self.max_iterations is not None and count_iteration == self.max_iterations:
                break