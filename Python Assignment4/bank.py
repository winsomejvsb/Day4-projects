import hashlib

class Wallet:
    def __init__(self, account_name, account_number, phone_number, username, password, login_pin, transaction_pin):
        self.account_name = account_name
        self.account_number = account_number
        self.phone_number = phone_number
        self.username = username
        self.password = self._hash_password(password)
        self.login_pin = login_pin
        self.transaction_pin = transaction_pin
        self.debit_wallet = 0.0
        self.credit_wallet = 0.0

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self._hash_password(password) == self.password

    def verify_transaction_pin(self, pin):
        return self.transaction_pin == pin

    def check_balance(self, pin, wallet_type):
        if self.verify_transaction_pin(pin):
            if wallet_type == 'debit':
                return self.debit_wallet
            elif wallet_type == 'credit':
                return self.credit_wallet
        else:
            return "Incorrect transaction PIN."

    def fund_wallet(self, pin, amount, wallet_type):
        if self.verify_transaction_pin(pin):
            if wallet_type == 'debit':
                self.debit_wallet += amount
            elif wallet_type == 'credit':
                self.credit_wallet += amount
            return "Wallet funded successfully."
        else:
            return "Incorrect transaction PIN."

    def transfer_funds(self, pin, target_wallet, amount, wallet_type):
        if not self.verify_transaction_pin(pin):
            return "Incorrect transaction PIN."
        if wallet_type == 'debit' and self.debit_wallet >= amount:
            self.debit_wallet -= amount
            target_wallet.debit_wallet += amount * 0.925
            return "Transfer successful."
        elif wallet_type == 'credit' and self.credit_wallet >= amount:
            self.credit_wallet -= amount
            target_wallet.credit_wallet += amount * 0.925
            return "Transfer successful."
        else:
            return "Insufficient balance."

# Sample users (In real application, use a database)
users = {
    '12345': Wallet('John Doe', '12345', '123-456-7890', 'johndoe', 'password123', '1111', '2222'),
    '67890': Wallet('Jane Smith', '67890', '098-765-4321', 'janesmith', 'password456', '3333', '4444')
}

def main():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        account_number = input("Enter account number: ")

        if account_number in users and users[account_number].username == username and users[account_number].verify_password(password):
            print(f"Welcome {users[account_number].account_name}!")
            while True:
                print("1. Check balance")
                print("2. Transfer funds")
                print("3. Fund wallet")
                print("4. Logout")
                choice = input("Choose an option: ")

                if choice == '1':
                    wallet_type = input("Enter wallet type (debit/credit): ").lower()
                    pin = input("Enter transaction PIN: ")
                    balance = users[account_number].check_balance(pin, wallet_type)
                    print(f"{wallet_type.capitalize()} Wallet Balance: {balance}")
                elif choice == '2':
                    target_account_number = input("Enter target account number: ")
                    if target_account_number in users:
                        target_wallet = users[target_account_number]
                        print(f"Target Account Name: {target_wallet.account_name}")
                        amount = float(input("Enter amount to transfer: "))
                        pin = input("Enter transaction PIN: ")
                        wallet_type = input("Enter wallet type (debit/credit): ").lower()
                        result = users[account_number].transfer_funds(pin, target_wallet, amount, wallet_type)
                        print(result)
                    else:
                        print("Target account not found.")
                elif choice == '3':
                    wallet_type = input("Enter wallet type (debit/credit): ").lower()
                    amount = float(input("Enter amount to fund: "))
                    pin = input("Enter transaction PIN: ")
                    result = users[account_number].fund_wallet(pin, amount, wallet_type)
                    print(result)
                elif choice == '4':
                    print("Logged out successfully.")
                    break
                else:
                    print("Invalid option. Please try again.")
        else:
            print("Invalid credentials. Please try again.")

if __name__ == "__main__":
    main()
