class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        print(f'Welcome {self.owner}')

    def __str__(self):
        return (
            f"{'='*35}\n"
            f"  Account Owner : {self.owner}\n"
            f"  Balance       : ${self.balance:,.2f}\n"
            f"  Account Type  : Bank Account\n"
            f"{'='*35}"
        )

    def deposit(self):
        deposit_amount = float(input('Enter deposit amount: '))
        self.balance += deposit_amount
        print(f"Deposited: ${deposit_amount:,.2f} | Current balance: ${self.balance:,.2f}")

    def withdraw(self):
        withdraw_amount = float(input('Enter withdraw amount: '))
        while withdraw_amount > self.balance: 
            withdraw_amount = float(input(f'Your current balance is not enough, please try again: '))
        self.balance -= withdraw_amount
        print(f"Withdrew: ${withdraw_amount:,.2f} | Current balance: ${self.balance:,.2f}")

    def get_balance(self):
        print(f'Your current balance: ${self.balance:,.2f}')


class SavingAccount(BankAccount):

    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate  

    def __str__(self):
        return (
            f"{'='*35}\n"
            f"  Account Owner : {self.owner}\n"
            f"  Balance       : ${self.balance:,.2f}\n"
            f"  Interest Rate : {self.interest_rate * 100:.1f}%\n"
            f"  Account Type  : Saving Account\n"
            f"{'='*35}"
        )

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Interest applied: +${interest:,.2f} | New balance: ${self.balance:,.2f}")


if __name__ == "__main__":
    hung_account = BankAccount("Hung Thai", 1000.0)
    print(hung_account)
    hung_account.deposit()
    hung_account.withdraw()
    hung_account.get_balance()


    saving_account = SavingAccount("Hung Thai", 5000.0, interest_rate=0.05)
    print(saving_account)
    saving_account.apply_interest()
    saving_account.withdraw()
    saving_account.get_balance()
