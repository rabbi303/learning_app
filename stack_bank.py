class Stack():
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return "Account is Empty"
        return self.items.pop()

    def balance(self):
        return sum(self.items)

    def __str__(self):
        return str(self.items)



stack = Stack()

while True:

  
    print("\n====== Bank Menu ======")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Exit")

    take = int(input("Enter Your Choice: "))

    if take == 1:
        print("Balance is:", stack.balance())

    elif take == 2:
        add_money = int(input("Enter amount to deposit: "))
        stack.push(add_money)
        print("Deposited successfully.")
        print("Your Balance is:", stack.balance())

    elif take == 3:
        if stack.is_empty():
            print("Account is Empty")
        else:
            withdraw_amount = int(input("Enter amount to withdraw: "))
            current_balance = stack.balance()
            if withdraw_amount > current_balance:
                print("Insufficient Balance")
            else:
                withdrawn = 0
                while withdrawn < withdraw_amount and not stack.is_empty():
                    top = stack.pop()
                    if withdrawn + top <= withdraw_amount:
                        withdrawn += top
                    else:
                        remaining = top - (withdraw_amount - withdrawn)
                        withdrawn = withdraw_amount
                        stack.push(remaining)
                print(f"Successfully Withdrawn: {withdrawn}")
                print("Now Your Balance is:", stack.balance())

    elif take == 4:
        print("Thank you! Exiting.")
        break

    else:
        print("Invalid Choice. Try again.")
