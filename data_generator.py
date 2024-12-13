import random
from string import ascii_uppercase
from datetime import datetime, timedelta
from os import getenv
from ast import literal_eval
from dotenv import load_dotenv
import locale


class DataGenerator:
    def __init__(self):
        # Configura o locale para português (ajuste conforme o sistema)
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except locale.Error:
            print("Não foi possível configurar o locale. Verifique se 'pt_BR.UTF-8' está instalado no sistema.")

        # Configurações originais
        load_dotenv()
        self.specific_seller = getenv("SPECIFIC_SELLER") == "True"
        self.sellers_ids = literal_eval(getenv("SELLERS_IDS", "[]"))
        self.number_of_sellers = literal_eval(getenv("NUMBER_OF_SELLERS", "0"))
        self.n_transactions = literal_eval(getenv("N_TRANSACTIONS", "5"))
        self.score_range = literal_eval(getenv("SCORE_RANGE", "[0, 1000]"))
        self.age_range = literal_eval(getenv("AGE_RANGE", "[18, 60]"))
        self.distance_range = literal_eval(getenv("DISTANCE_RANGE", "[100, 3000]"))
        self.value_range = literal_eval(getenv("VALUE_RANGE", "[30, 500]"))
        self.mcc_numbers = literal_eval(getenv("MCC_NUMBERS", "[5499]"))
        self.mcc_names = literal_eval(getenv("MCC_NAMES", "['LOJA DE ALIMENTOS VARIADOS']"))
        self.transaction_types = literal_eval(getenv("TRANSACTION_TYPES", "['PIX']"))

    def generate_random_date_within_90_days(self):
        today = datetime.now()
        random_days_ago = random.randint(0, 90)
        random_date = today - timedelta(days=random_days_ago)
        return random_date.replace(hour=0, minute=0, second=0, microsecond=0)

    def generate_date_now(self):
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def generate_random_string(self, length):
        return ''.join(random.choice(ascii_uppercase) for _ in range(length))

    def generate_transactions(self, seller_id, consumer_id, mcc_idx):
        portfolio_seller_id = seller_id
        if random.randint(0, 100) > 98:
            portfolio_seller_id = ''
        
        transactions = []
        for _ in range(self.n_transactions):
            transaction_id = self.generate_random_string(15)
            
            transaction_seller_id = seller_id
            if random.randint(0, 100) > 80:
                mcc_idx = random.randint(0, len(self.mcc_numbers) - 1)
                transaction_seller_id = self.generate_random_string(7)
            
            mcc_number = self.mcc_numbers[mcc_idx]
            mcc_category = self.mcc_names[mcc_idx]
            transaction_date = self.generate_random_date_within_90_days()
            transaction = {
                'transaction_id': transaction_id,
                'consumer_id': consumer_id,
                'transaction_seller_id': transaction_seller_id,
                'portfolio_seller_id': portfolio_seller_id,
                'seller_mcc': mcc_number,
                'seller_mcc_category': mcc_category,
                'value': random.randint(self.value_range[0], self.value_range[1]),
                'type': random.choice(self.transaction_types),
                'date': transaction_date,
                'day_of_week': transaction_date.strftime('%A'),
                'updated_at': self.generate_date_now(),
                'created_at': self.generate_date_now()
            }
            
            transactions.append(transaction)
        
        return transactions

    def consumer_generate(self, seller_id, mcc_idx):
        consumer_id = self.generate_random_string(7)
        
        consumer = {
            'consumer_id': consumer_id,
            'seller_id': seller_id,
            'score': random.randint(self.score_range[0], self.score_range[1]),
            'age': random.randint(self.age_range[0], self.age_range[1]),
            'exact_distance': random.randint(self.distance_range[0], self.distance_range[1]),
            'updated_at': self.generate_date_now(),
            'created_at': self.generate_date_now()
        }
        
        transactions = self.generate_transactions(seller_id, consumer_id, mcc_idx)
                
        return {
            "consumer": consumer,
            'transactions': transactions
        }