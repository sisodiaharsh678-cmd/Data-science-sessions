class Bank : 

    def openAccount(self , cname , acno , balance):
        self.cname = cname 
        self.acno = acno 
        self.balance= balance
        print("hello" , cname , "your account no " , acno , "is opened with " , balance , "Rs")

    def deposit(self,amount):
        self.balance=self.balance+amount   
    def withdraw(self,amount):
        if amount <= self.balance:
            self.balance = self.balance-amount 
        else:
            print("insufficient balance ")
    def checkBalance(self):
        print("your current balance is : " , self.balance)

        
        
b1= Bank()
b1.openAccount("harsh prajapati" , 101 ,1000)

while True:

    print("*" *50)
    print("1 . Deposite")
    print("2 . Withdraw")
    print("3 . Check balance ")
    print("4 . Exit")
    print("*" *50)

    choice = int(input("Enter ur chocie : "))
    print("*" *50)

    if choice==1:
        amount = int(input("enter deposite amount : "))
        b1.deposit(amount)
        print("*" *50)
    elif choice==2:
        amount = int(input("enter withdraw amount : "))
        b1.withdraw(amount)
        print("*" *50)  
    elif choice==3:
        
        b1.checkBalance()
        print("*" *50)  
    elif choice==4:
       print("thank you for using our system ")
       print("*" *50)    
       break   
    else:
        print("invalid choice . please try again ")    



