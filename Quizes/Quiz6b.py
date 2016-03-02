__author__ = 'Sam Broderick'


class BankAccount(object):
    def __init__(self, initial_balance):
        """Creates an account with the given balance."""
        self.balance = initial_balance
        self.fees = 0

    def deposit(self, amount):
        """Deposits the amount into the account."""
        self.balance += amount

    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance.
        """
        self.balance -= amount
        if self.balance < 0:
            self.balance -= 5
            self.fees += 5

    def get_balance(self):
        """Returns the current balance in the account."""
        return self.balance

    def get_fees(self):
        """Returns the total fees ever deducted from the account."""
        return self.fees


account1 = BankAccount(20)
account1.deposit(10)
account2 = BankAccount(10)
account2.deposit(10)
account2.withdraw(50)
account1.withdraw(15)
account1.withdraw(10)
account2.deposit(30)
account2.withdraw(15)
account1.deposit(5)
account1.withdraw(10)
account2.withdraw(10)
account2.deposit(25)
account2.withdraw(15)
account1.deposit(10)
account1.withdraw(50)
account2.deposit(25)
account2.deposit(25)
account1.deposit(30)
account2.deposit(10)
account1.withdraw(15)
account2.withdraw(10)
account1.withdraw(10)
account2.deposit(15)
account2.deposit(10)
account2.withdraw(15)
account1.deposit(15)
account1.withdraw(20)
account2.withdraw(10)
account2.deposit(5)
account2.withdraw(10)
account1.deposit(10)
account1.deposit(20)
account2.withdraw(10)
account2.deposit(5)
account1.withdraw(15)
account1.withdraw(20)
account1.deposit(5)
account2.deposit(10)
account2.deposit(15)
account2.deposit(20)
account1.withdraw(15)
account2.deposit(10)
account1.deposit(25)
account1.deposit(15)
account1.deposit(10)
account1.withdraw(10)
account1.deposit(10)
account2.deposit(20)
account2.withdraw(15)
account1.withdraw(20)
account1.deposit(5)
account1.deposit(10)
account2.withdraw(20)
print(account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees())


def list_extend_many(lists):
    result = []
    for i in range(len(lists)):
        result.extend(lists[i])
    return result


l = [[1, 2], [3], [4, 5, 6], [7]]
print(list_extend_many(l))

n = 1000
i = 0
j = 0
numbers = list(range(2, n))
results = []
while len(numbers) > 0:
    results += [numbers[0]]
    while i < len(numbers):
        if numbers[i] % results[j] == 0:
            numbers.pop(i)
        else:
            i += 1
    j += 1
    i = 0

print(len(results))

num_slow = 1000.0
num_fast = 1.0
i = 1
print('Year\tSlow\t\tFast')
while num_slow > num_fast:
    print('{0}\t\t{1}\t\t{2}'.format(i, num_slow, num_fast))
    num_slow *= 2
    num_fast *= 2
    num_slow = 0.6 * num_slow
    num_fast = 0.7 * num_fast
    i += 1
print('{0}\t\t{1}\t\t{2}'.format(i, num_slow, num_fast))
