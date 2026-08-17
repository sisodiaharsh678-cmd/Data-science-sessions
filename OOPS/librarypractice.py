class library:
    def __init__(self):
        self.books=[]
    
    def addBook(self ,Book_name):
        self.books.append(Book_name)
        print(f'"{Book_name}" added to the library')

    def issueBook(self,Book_name):
        if Book_name in self.books:
            self.books.remove(Book_name)
            print(f'you have issued {Book_name}')    
        else:
            print(f'sorry , {Book_name} is not available.')

    def showBooks(self):
        print("Available books : " , self.books)

library = library()
library.addBook("python advance")
library.addBook("Machine learning")

while True:
    print("*" *50)
    print("1 . Add Book")
    print("2 . Issue Book")
    print("3 . Show Book ")
    print("4 . Exit")
    print("*" *50)

    choice = int(input("Enter choice : "))
    if choice == 1:
        book = input("Enter book name: ")
        library.addBook(book)
    elif choice == 2:
        book = input("Enter book name to issue: ")
        library.issueBook(book)
    elif choice == 3:
        library.showBooks()
    elif choice == 4:
        print("Exiting library system.")
        break
    else:
        print("Invalid choice.")