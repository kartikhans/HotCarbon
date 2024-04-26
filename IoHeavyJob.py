import os

from google.cloud import bigquery
from google.oauth2 import service_account
import names
import random
import uuid
from datetime import datetime
from dotenv import load_dotenv

card_types = ['VISA', 'MASTERCARD', 'RUPAY']
status_types = ['ACTIVE', 'INACTIVE']
transaction_status = ['INPROGRESS', 'COMPLETE']

load_dotenv(dotenv_path='.env')
table_id_directory = dict(user=os.environ['USER_TABLE'], credit_card=os.environ['CREDIT_TABLE'],
                          transaction=os.environ['TRANSACTION_TABLE'])


def generate_random_transaction_data(credit_card_id):
    return [dict(transaction_id=str(uuid.uuid4()), amount=random.randint(1, 1000),
                 datetime=str(datetime.now()), status=random.choice(transaction_status),
                 credit_card_id=credit_card_id)]


def generate_random_credit_data(user_id):
    return [dict(card_id=str(uuid.uuid4()), last_four=random.randint(1001, 9999), category=random.choice(card_types),
                 user_id=user_id, status=random.choice(status_types))]


def generate_random_user_data():
    return [dict(user_id=str(uuid.uuid4()), name=names.get_full_name(), country='US', age=random.randint(1, 100))]


class IoHeavyJob:
    def __init__(self, key_path, user_count):
        self.credentials = service_account.Credentials.from_service_account_file(key_path,
                                                                                 scopes=[
                                                                                     'https://www.googleapis.com/auth/bigquery'])
        self.client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)

        self.last_userid = None
        self.user_count = user_count

    def execute_query(self, query):
        return self.client.query(query).result()

    def clean_db(self):
        for key in table_id_directory.keys():
            query = f'DELETE FROM {table_id_directory.get(key)} WHERE true;'
            print(query)
            self.execute_query(query)

    def push_data(self, data, table_id):
        print(data, table_id)
        errors = self.client.insert_rows_json(table_id, data)

        return errors

    def execute(self):
        # self.clean_db()
        for i in range(1, self.user_count + 1):
            user_data = generate_random_user_data()
            self.push_data(user_data, table_id_directory.get('user'))

            for j in range(3):
                credit_card_data = generate_random_credit_data(user_data[0]['user_id'])
                self.push_data(credit_card_data, table_id_directory.get('credit_card'))

                for k in range(5):
                    transaction_data = generate_random_transaction_data(credit_card_data[0]['card_id'])
                    self.push_data(transaction_data, table_id_directory.get('transaction'))

            if i % 3 == 0:
                query = f'SELECT * FROM {table_id_directory.get('user')} WHERE user_id = "{self.last_userid}" LIMIT 1000;'
                self.execute_query(query)

            self.last_userid = user_data[0]['user_id']


if __name__ == '__main__':
    key_path = '/Users/kushhans/Documents/system-413600-04d1ac1ca37d.json'
    x = IoHeavyJob(key_path=key_path, user_count=4)
    x.execute()
