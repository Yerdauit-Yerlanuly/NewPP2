class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(amount, self.balance)
    
    def withdraw(self, amount):
        if amount > self.balance:
            print()
        else:
            self.balance -= amount
            print(amount, self.balance)

owner = input()
initial_balance = float(input())

account = Account(owner, initial_balance)

while True:
    action = input().lower()
    
    if action == 'deposit':
        amount = float(input())
        account.deposit(amount)
    elif action == 'withdraw':
        amount = float(input())
        account.withdraw(amount)
    elif action == 'exit':
        break
    else:
        print()
