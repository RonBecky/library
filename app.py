#all my imports
import json
from flask import Flask, jsonify ,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#connecting my database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.sqlite3"
app.config["SECRET_KEY"] = "random string"
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ------------------------------------------------------------------------SQL books table----------------------------------------------------------------------------------------------------
class books(db.Model):#creating books table
    id = db.Column("book_id", db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Author = db.Column(db.String(50))
    YearPublished = db.Column(db.String(200))
    Type = db.Column(db.String(10))
    Description = db.Column(db.String(350))
    Image = db.Column(db.String(500))

    def __init__(self, Name, Author, YearPublished, Type, Description, Image):
        self.Name = Name
        self.Author = Author
        self.YearPublished = YearPublished
        self.Type = Type
        self.Description = Description
        self.Image = Image  

    def to_dict(self):
        return {
            "id": self.id,
            "Name": self.Name,
            "Author": self.Author,
            "YearPublished": self.YearPublished,
            "Type": self.Type,
            "Description": self.Description,
            "Image": self.Image  
        }


#performing CRUD

@app.route("/")#getting the data
def getBooks():
    books_list = [book.to_dict() for book in books.query.all()]
    json_data = json.dumps(books_list)
    return json_data


@app.route("/new", methods=["POST"])#inserting new data
def new():
    data = request.get_json()
    Author = data["Author"]
    Name = data["Name"]
    YearPublished = data["YearPublished"]
    Type = data["Type"]
    Description = data["Description"]
    Image = data.get("Image", "")

    new_book = books(Name, Author, YearPublished, Description, Type, Image)
    db.session.add(new_book)
    db.session.commit()
    return "A new record was created."


@app.route("/del/<id>", methods=["DELETE"])#deleting data
def del_book(id=-1):
    book = books.query.get(id)
    if book is None:
        return {"error": "Book not found with id {}".format(id)}
    db.session.delete(book)
    db.session.commit()
    return {"delete": "success"}


@app.route("/upd/<id>", methods=["PUT"])#updating already exsisting data
def upd_book(id=-1):
    book = books.query.get(id)
    if book is None:
        return {"error": "Book not found with id {}".format(id)}
    data = request.get_json()
    book.Author = data.get("Author", book.Author)
    book.Name = data.get("Name", book.Name)
    book.YearPublished = data.get("YearPublished", book.YearPublished)
    book.Type = data.get("Type", book.Type)
    book.Description = data.get("Description", book.Description)
    book.Image = data.get("Image", book.Image)
    db.session.commit()
    return {"update": "success"}


# ------------------------------------------------------------------------SQL customers table----------------------------------------------------------------------------------------------------

class customers(db.Model):#creating customers table
    id = db.Column("customer_id", db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Adress = db.Column(db.String(50))
    Phone = db.Column(db.String(200))
    Email = db.Column(db.String(10))

    def __init__(self, Name, Address, Phone, Email):
        self.Name = Name
        self.Adress = Address
        self.Phone = Phone
        self.Email = Email

    def to_dict(self):
        return {
            "id": self.id,
            "Name": self.Name,
            "Address": self.Adress,
            "Phone": self.Phone,
            "Email": self.Email,
        }


@app.route("/getCustomers")#getting the data
def getCustomers():
    customers_list = [customer.to_dict() for customer in customers.query.all()]
    json_data = json.dumps(customers_list)
    return json_data


@app.route("/newCustomer", methods=["POST"])#inserting new data
def newCustomer():
    data = request.get_json()
    # print(data)
    cName = data["Name"]
    Adress = data["Address"]
    Phone = data["Phone"]
    Email = data["Email"]

    new_customer = customers(cName, Adress, Phone, Email)
    db.session.add(new_customer)
    db.session.commit()
    return "A new record was created."


@app.route("/delCustomer/<id>", methods=["DELETE"])#deleting data
def delete_customer(id):
    customer = customers.query.get(id)
    if customer is None:
        return {"error": "No customer with id {} found".format(id)}, 404
    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer successfully deleted"}, 200


@app.route("/updateCustomer/<id>", methods=["PUT"])#updating already exsisting data
def update_customer(id=-1):
    customer = customers.query.get(id)
    if customer is None:
        return {"update": "failed"}
    data = request.get_json()
    customer.Name = data["Name"]
    customer.Address = data["Address"]
    customer.Phone = data["Phone"]
    customer.Email = data["Email"]
    db.session.commit()
    return {"update": "success"}


# ------------------------------------------------------------------------SQL loans table----------------------------------------------------------------------------------------------------
# i tried to get the data or bookid and custid but didnt understood the assigment as for what i need that and i faild to see if it actually works
# SQL loans table
class loans(db.Model):
    id = db.Column("loan_id", db.Integer, primary_key=True)
    CustID = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    customer = db.relationship('customers',backref=db.backref('loans', lazy=True))
    BookID = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    book = db.relationship('books',backref=db.backref('loans', lazy=True))
    Loan_date = db.Column(db.String(200))
    Return_date = db.Column(db.String(10))

    def __init__(self, CustID, BookID, Loan_date, Return_date):
        self.CustID = CustID
        self.BookID = BookID
        self.Loan_date = Loan_date
        self.Return_date = Return_date

    def to_dict(self):
        return {
            "id": self.id,
            "CustID": self.CustID,
            "customer_name": self.customer.Name,  
            "BookID": self.BookID,
            "book_title": self.book.Name,
            "Loan_date": self.Loan_date,
            "Return_date": self.Return_date,
        }


@app.route("/newLoan", methods=["POST"])
def newLoan():
    data = request.get_json()
    cust_id = data.get["cust_id"]
    book_id = data.get["book_id"]
    loan_date = data["Loan_date"]
    return_date = data["Return_date"]

   
    customer = customers.query.get(cust_id)
    book = books.query.get(book_id)

   
    if (customer is None) or (book is None):
        return {"error": "Customer or book not found"}, 404

   
    new_loan = loans(customer.id, book.id, loan_date, return_date)
    db.session.add(new_loan)
    db.session.commit()

    
    return {"message": "Loan created successfully"}, 200


@app.route("/delLoan/<id>", methods=["DELETE"])
def delete_loan(id):
    loan = loans.query.get(id)
    if loan is None:
        return {"error": "No Loan with id {} found".format(id)}, 404
    db.session.delete(loan)
    db.session.commit()
    return {"message": "Loan successfully deleted"}, 200


@app.route("/updateLoan/<id>", methods=["PUT"])
def update_loan(id=-1):
    loan = loans.query.get(id)
    if loan is None:
        return {"update": "failed"}
    data = request.get_json()
    loan.CustID = data["CustID"]
    loan.BookID = data["BookID"]
    loan.Loan_date = data["Loan_date"]
    loan.Return_date = data["Return_date"]
    db.session.commit()
    return {"update": "success"}

@app.route("/getLoans")
def getLoans():
    Loan_list = [Loan.to_dict() for Loan in loans.query.all()]
    json_data = json.dumps(Loan_list)
    return json_data

#--------------------------------------------------------------------------name==main----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)