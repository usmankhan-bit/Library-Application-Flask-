from flasklib import db
from datetime import date

class student(db.Model):
    id=db.Column(db.String(10),primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    std=db.Column(db.String(120),nullable=False)
    sbrelation=db.relationship('borrow',backref='name',lazy=True)

    def __repr__(self):
        return f"User('{self.name}','{self.id}')"

class teacher(db.Model):
    id=db.Column(db.String(10),primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    tbrelation=db.relationship('borrow',backref='tname',lazy=True)

    def __repr__(self):
        return f"Teacher('{self.name}','{self.id}')"


class books(db.Model):
    id=db.Column(db.String(10),primary_key=True)
    bname=db.Column(db.String(100),nullable=False)
    date=db.Column(db.String(20),nullable=False)
    author=db.Column(db.String(50),nullable=False)
    publisher=db.Column(db.String(50),nullable=False)
    place=db.Column(db.String(50),nullable=False)
    year=db.Column(db.String(20),nullable=False)
    edvol=db.Column(db.String(50),nullable=False)
    pages=db.Column(db.String(10),nullable=False)
    cost=db.Column(db.String(10),nullable=False)
    orderno=db.Column(db.String(10),nullable=False)
    supplier=db.Column(db.String(50),nullable=False)
    classno=db.Column(db.String(10),nullable=False)
    borrower=db.relationship('borrow',backref='book_name',lazy=True)
    back_history=db.relationship('history',backref='book',lazy=True)

    
    def __repr__(self):
        return f"Book('{self.id}','{self.bname}')"

class borrow(db.Model):
    sid=db.Column(db.String(10),db.ForeignKey('student.id'),db.ForeignKey('teacher.id'),nullable=False)
    bid=db.Column(db.String(10),db.ForeignKey('books.id'),nullable=False,primary_key=True)
    date_given=db.Column(db.DateTime,nullable=False,default=date.today())
    penalty=db.Column(db.Integer,default=0)

    def __repr__(self):
        return f"Book('{self.sid}','{self.bid}','{self.date_given}','{self.penalty}')"

class history(db.Model):
    sid=db.Column(db.String(10),nullable=False,primary_key=True)
    bid=db.Column(db.String(10),db.ForeignKey('books.id'),nullable=False,primary_key=True)
    date_given=db.Column(db.DateTime,nullable=False,primary_key=True)
    date_returned=db.Column(db.DateTime,nullable=False,default=date.today())
    penalty=db.Column(db.Integer,default=0)

    def __repr__(self):
        return f"history('{self.sid}','{self.bid}','{self.date_given}','{self.date_returned}','{self.penalty}')"

