class TransactionLog:

    def __init__(self, brand, transaction_date, client, amount):
        self.brand = brand
        self.transactionDate = transaction_date
        self.client = client
        self.amount = amount

    def convert_to_txt(self, brand, transactionDate, client, amount):
        return f'{brand};{transactionDate};{client};{amount}'
