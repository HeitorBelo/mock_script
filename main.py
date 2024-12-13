from random import randint
from os import getenv, system, name
from ast import literal_eval
from dotenv import load_dotenv
from time import sleep
from colorama import init, Fore
from data_generator import DataGenerator
from save_mongo import SaveOnMongo

data_generator = DataGenerator()
save_mongo = SaveOnMongo()

init(autoreset=True)

load_dotenv()

sellers_ids = literal_eval(getenv("SELLERS_IDS", "[]"))
number_of_sellers = literal_eval(getenv("NUMBER_OF_SELLERS", "0"))
mcc_numbers = literal_eval(getenv("MCC_NUMBERS", "[5499]"))


if len(sellers_ids) == 0:
    sellers_ids = [data_generator.generate_random_string(7) for _ in range(number_of_sellers)]

def clear_screen():
    
    system('cls' if name == 'nt' else 'clear')

def cls_message(message, delay=2):
    clear_screen()
    print(Fore.GREEN + message)
    sleep(delay)
    clear_screen()

def print_main_menu():
    clear_screen()
    print(Fore.GREEN + "===============================")
    print(Fore.GREEN + "       Gerador de Dados        ")
    print(Fore.GREEN + "===============================")
    print(Fore.GREEN + "[1] Gerar documentos")
    print(Fore.GREEN + "[2] Sair")
    print(Fore.GREEN + "===============================")

while True:
    clear_screen()
    print_main_menu()
    try:
        opt = input(Fore.GREEN + "\nEscolha uma opção: ")

        if opt == '1':

            clear_screen()

            data_count = int(input('\nQuantos documentos deseja gerar para cada seller? '))

            if data_count < 1:
                cls_message('Digite um número maior que zero!', 2)
                continue
            
            clear_screen()
            
            cont = 0
            for seller_id in sellers_ids:
                seller_mcc_idx = randint(0, len(mcc_numbers) - 1)
                consumers = []
                transactions = []
                
                cont += 1
                print(Fore.GREEN + f"Gerando dados para {seller_id} ({cont}/{len(sellers_ids)})...")
                
                for _ in range(data_count):
                    data = data_generator.consumer_generate(seller_id=seller_id, mcc_idx=seller_mcc_idx)
                    
                    consumers.append(data['consumer'])
                    transactions.append(data['transactions'])
                    
                save_mongo.save_consumers(consumers)
                save_mongo.save_transactions(transactions)
                    
            cls_message(f'Dados gerados com sucesso!', 3)
        else:
            exit(0)

    except ValueError as e:
        cls_message('Digite um número!', 2)