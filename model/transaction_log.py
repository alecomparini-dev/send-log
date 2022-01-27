class TransactionLog:

    def __init__(self, brand, transaction_date, client, amount):
        self.brand = brand
        self.transaction_date = transaction_date
        self.client = client
        self.amount = amount

    def convert_to_txt(self, brand, transaction_date, client, amount):
        return f'{brand};{transaction_date};{client};{amount}'
