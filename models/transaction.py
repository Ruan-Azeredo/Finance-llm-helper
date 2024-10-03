
class Transaction():
    def __init__(self, id, date, amount, memo):

        self.id: str = id
        self.date: str = date
        self.value: float = amount
        self.description: str = memo

    def treatment_data(self):
        self.value = self.value
        self.date = self.date
        return self
    
    def format_description_transaction(self):
        return self.date.strftime("%d/%m/%Y") + '|' + self.description + '|' + self.value.__str__()
