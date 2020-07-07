from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,DateField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flasklib.models import student,books,borrow,history,teacher
from datetime import date,datetime

class BookForm(FlaskForm):
    sid = StringField('Student id', validators=[DataRequired()])
    bid = StringField('Book id',validators=[DataRequired()])
    submit = SubmitField('Lend Book')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        temp=date.today().toordinal()
        result=history.query.filter_by(sid=self.sid.data,bid=self.bid.data,date_given=datetime.fromordinal(temp)).first()
        if result is not None:
            self.sid.errors.append('cannot buy the same book')
            return False
        return True

    def validate_sid(self,sid):
        user1=student.query.filter_by(id=sid.data).first()
        user2=teacher.query.filter_by(id=sid.data).first()
        if user1 is None and user2 is None:
            raise ValidationError('Student/Teacher Doesnt exists with this id in the database')
        result=borrow.query.filter_by(sid=sid.data).first()
        if result is not None:
            raise ValidationError('Student/Teacher has already borrowed a book')    

    def validate_bid(self,bid):
        user2=books.query.filter_by(id=bid.data).first()
        if not(user2):
            raise ValidationError('Book doesnt exists in the database with the given id')
        temp=borrow.query.filter_by(bid=bid.data).first()
        if temp is not None:
            raise ValidationError('Book already taken with this id')
        
    
    
class ReturnForm(FlaskForm):
    fsid = StringField('Student id', validators=[DataRequired()])
    fbid = StringField('Book id',validators=[DataRequired()])
    submit = SubmitField('get back')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        
        user1=student.query.filter_by(id=self.fsid.data).first()
        user2=teacher.query.filter_by(id=self.fsid.data).first()
        if user1 is None and user2 is None:
            self.fsid.errors.append('Student/Teacher Doesnt exists with this id in the database')
            return False
        
        user1=borrow.query.filter_by(sid=self.fsid.data).first()
        if not(user1):
            self.fsid.errors.append('Student/Teacher hasn\'t borrowed any book')
            return False
        
        usertemp2=books.query.filter_by(id=self.fbid.data).first()
        if not(usertemp2):
            self.fbid.errors.append('Book doesnt exists in the database with the given id')
            return False

        user2=borrow.query.filter_by(bid=self.fbid.data).first()
        if not(user2):
            self.fbid.errors.append('The book is not lended to anyone')
            return False

        result=borrow.query.filter_by(sid=self.fsid.data,bid=self.fbid.data).first()
        if result is None:
            self.fsid.errors.append('Unique id and book do not match')
            return False
        return True


class DisplayForm(FlaskForm):
    fsid = StringField('Student id', validators=[DataRequired()])
    submit = SubmitField('display books')

    def validate_fsid(self,fsid):
        user1=student.query.filter_by(id=fsid.data).first()
        user2=teacher.query.filter_by(id=fsid.data).first()
        if user1 is None and user2 is None:
            raise ValidationError('Student/Teacher Doesnt exists with this id in the database')    

class DisplayForm2(FlaskForm):
    date_given=DateField('Date Given',validators=[DataRequired()])
    submit = SubmitField('display books')

class HistoryForm(FlaskForm):
    year=StringField('Year',validators=[DataRequired()])
    submit = SubmitField('Get history')

class HistoryForm2(FlaskForm):
    fsid = StringField('Student id', validators=[DataRequired()])
    submit = SubmitField('Get history')


class InsertForm(FlaskForm):
    fname = StringField('Student name', validators=[DataRequired()])
    fstd = StringField('Student std')
    fid=StringField('Unique Id',validators=[DataRequired()])
    submit = SubmitField('Insert Entries')

    def validate_fid(self,fid):
        if fid.data[0]!="S":
            if fid.data[0]!="T":
                raise ValidationError('Unique id should start with either S or T')
        
        res=student.query.filter_by(id=fid.data).first()
        res2=teacher.query.filter_by(id=fid.data).first()
        if res is not None or res2 is not None:
            raise ValidationError("Unique Id already exists")


class DeleteForm(FlaskForm):
    fsid = StringField('Student id', validators=[DataRequired()])
    submit = SubmitField('Delete')

    def validate_fsid(self,fsid):
        res=student.query.filter_by(id=fsid.data).first()
        res2=teacher.query.filter_by(id=fsid.data).first()
        res3=books.query.filter_by(id=fsid.data).first()
        if res is None and res2 is None and res3 is None:
            raise ValidationError('Student/Teacher Doesnt exists with this id in the database')



