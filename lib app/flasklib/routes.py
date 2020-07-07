from flasklib.models import student,books,borrow,history,teacher
from flasklib import app,db
from flask import render_template,url_for,flash,redirect,request
from flasklib.forms import BookForm,ReturnForm,DisplayForm,HistoryForm,HistoryForm2,DisplayForm2,InsertForm,DeleteForm
from sqlalchemy import text
from datetime import date,datetime
import csv
import pandas as pd
import os

sheader=['Unique Id','Name','Standard']
theader=['Unique Id','Name']
bheader=['Unique Id','Name','std','Book id','Book name','Date borrowed','Penalty']
bookheader=['Date','Acc No','Author','Title','Publisher','Place of publication','Year of publication','Edition/Volume','Pages','Cost','Supplier order no','Supplier','Classification No']

@app.route("/")
@app.route("/home")
def home():
    global flag
    print(flag)
    sql = text('select count(*) from borrow')
    result = db.engine.execute(sql)
    names = [row[0] for row in result]
    t_d=date.today()
    t_d=datetime.fromordinal(t_d.toordinal())
    if flag:
        print("Here")
        for it in borrow.query.all():
            temp=date.today()-it.date_given.date()
            temp=temp.days
            x=33
            print(temp)
            if temp>30 and temp<=33: 
                it.penalty=10
                db.session.commit()
            if x+7==temp or x+7==temp+1:
                x=temp
                it.penalty+=10
                db.session.commit()

        flag=False
    result2=borrow.query.filter_by(date_given=t_d).all()
    return render_template('home.html',posts=names,today=len(result2),todaylend=result2)

@app.route("/issue",methods=['GET','POST'])
def issue():
    form=BookForm()
    if form.validate_on_submit():
        btemp= borrow(sid=form.sid.data,bid=form.bid.data)
        db.session.add(btemp)
        db.session.commit()
        flash(f'Book can be lended to the student/teacher','success')
        return redirect(url_for('home'))
    return render_template('issue.html',title='Issue',form=form)

@app.route("/returnb",methods=['GET','POST'])
def returnb():
    form=ReturnForm()
    if form.validate_on_submit():
        b1=borrow.query.filter_by(bid=form.fbid.data,sid=form.fsid.data).first()
        h1=history(sid=b1.sid,bid=b1.bid,date_given=b1.date_given,penalty=b1.penalty)
        db.session.delete(b1)
        db.session.add(h1)
        db.session.commit()
        flash(f'Book returned successfully','success')
        return redirect(url_for('home'))
    return render_template('returnb.html',title='Return',form=form)

@app.route("/display",methods=['GET','POST'])
def display():
    form=DisplayForm()
    form2=DisplayForm2()
    if form.validate_on_submit():
        var=borrow.query.filter_by(sid=form.fsid.data).all()
        return render_template('display.html',title='display',posts=var)
    if form2.validate_on_submit():
        date_req=datetime.fromordinal(form2.date_given.data.toordinal())
        a=(request.form.get('Item_1'))
        temp=borrow.query.filter_by(date_given=date_req).all()
        if a=="Student":
            for data in temp:
                if data.sid[0] != "S":
                    temp.remove(data)
        elif a=="Teacher":
            for data in temp:
                if data.sid[0] != "T":
                    temp.remove(data)
        return render_template('display.html',title='display',posts=temp)
    return render_template('displayform.html',title='displayform',form=form,form2=form2)

@app.route("/getHistory",methods=['GET','POST'])
def getHistory():
    form=HistoryForm()
    form2=HistoryForm2()
    if form.validate_on_submit():
        a=(request.form.get('Item_1'))
        temp=[]
        if a=="Student":
            for data in history.query.all():
                if data.sid[0] == "S" and data.date_given.date().year==int(form.year.data):
                    temp.append(data)
        elif a=="Teacher":
            for data in history.query.all():
                if data.sid[0] == "T" and data.date_given.date().year==int(form.year.data):
                    temp.append(data)
        return render_template('historydisplay.html',title='display',posts=temp)
    if form2.validate_on_submit():
        temp=history.query.filter_by(sid=form2.fsid.data).all()
        return render_template('historydisplay.html',title='display',posts=temp)
    return render_template('history.html',title='get history',form=form,form2=form2)

@app.route("/insert",methods=['GET','POST'])
def insert():
    form=InsertForm()
    form2=DeleteForm()
    if form.validate_on_submit():
        a=(request.form.get('Item_1'))
        if a=="Student":
            if form.fid.data[0]!="S":
                flash(f'Student id should start with S','danger')
                return redirect(url_for('home'))
            stemp=student(name=form.fname.data,std=form.fstd.data,id=form.fid.data)
            db.session.add(stemp)
            db.session.commit()
            flash(f'Student added successfully','success')
        elif a=="Teacher":
            if form.fid.data[0]!="T":
                flash(f'Teacher id should start with T','danger')
                return redirect(url_for('home'))
            ttemp=teacher(name=form.fname.data,id=form.fid.data)
            db.session.add(ttemp)
            db.session.commit()
            flash(f'Teacher added successfully','success')
    if  form2.validate_on_submit():
        btemp=borrow.query.filter_by(sid=form2.fsid.data).first()
        if btemp is not None:
            flash(f'Student/Teacher has borrowed a book','danger')
            return redirect(url_for('home'))
        if form2.fsid.data[0]=="S":
            stemp=student.query.filter_by(id=form2.fsid.data).first()
            db.session.delete(stemp)
            flash(f'Student deleted successfully','success')
        elif form2.fsid.data[0]=="T":
            stemp=teacher.query.filter_by(id=form2.fsid.data).first()
            db.session.delete(stemp)
            flash(f'Teacher deleted successfully','success')
        else:
            stemp=books.query.filter_by(id=form2.fsid.data).first()
            db.session.delete(stemp)
            flash(f'Book deleted successfully','success')    
        db.session.commit()
    return render_template('insert.html',title='Insert',form=form,form2=form2)

@app.route("/export",methods=['GET','POST'])
def export():
    if request.method == 'POST' and 'export' in request.form:
        a=(request.form.get('Item_1'))
        if a=="Student":
            i=1
            os.chdir('C:/Users/Usman Khan/Desktop')
            while os.path.exists("students_%s.csv" % i):
                i+=1
            with open('C:/Users/Usman Khan/Desktop/students_%s.csv' % i,'w+',newline='') as write_file:
                writer = csv.writer(write_file)
                writer.writerow(sheader)
                for row in student.query.all():
                    temp=[]
                    temp.append(row.id)
                    temp.append(row.name)
                    temp.append(row.std)
                    writer.writerow(temp)
                flash(f'Student file downloaded','success')
        elif a=="Books":
            i=1
            os.chdir('C:/Users/Usman Khan/Desktop')
            while os.path.exists("books_%s.csv" % i):
                i+=1
            with open('C:/Users/Usman Khan/Desktop/books_%s.csv' % i,'w+',newline='') as write_file:
                writer = csv.writer(write_file)
                writer.writerow(bookheader)
                for row in books.query.order_by(books.id).all():
                    temp=[]
                    temp.append(row.date)
                    temp.append(row.id)
                    temp.append(row.author)
                    temp.append(row.bname)
                    temp.append(row.publisher)
                    temp.append(row.place)
                    temp.append(row.year)
                    temp.append(row.edvol)
                    temp.append(row.pages)
                    temp.append(row.cost)
                    temp.append(row.orderno)
                    temp.append(row.supplier)
                    temp.append(row.classno)
                    writer.writerow(temp)   
                flash(f'Books file downloaded','success')
        elif a=="Borrowed":
            i=1
            os.chdir('C:/Users/Usman Khan/Desktop')
            while os.path.exists("booksBorrowed_%s.csv" % i):
                i+=1
            with open('C:/Users/Usman Khan/Desktop/booksBorrowed_%s.csv' % i,'w+',newline='') as write_file:
                writer = csv.writer(write_file)
                writer.writerow(bheader)
                for row in borrow.query.all():
                    temp=[]
                    temp.append(row.sid)
                    if row.sid[0]=="S":
                        temp.append(row.name.name)
                        temp.append(row.name.std)
                    elif row.sid[0]=="T":                      
                        temp.append(row.tname.name)
                        temp.append(" ")
                    temp.append(row.bid)
                    temp.append(row.book_name.bname)
                    temp.append(row.date_given)
                    temp.append(row.penalty)
                    writer.writerow(temp)   
                flash(f'Borrowed Books file downloaded','success')
        elif a=="Teacher":
            i=1
            os.chdir('C:/Users/Usman Khan/Desktop')
            while os.path.exists("Teacher_%s.csv" % i):
                i+=1
            with open('C:/Users/Usman Khan/Desktop/Teacher_%s.csv' % i,'w+',newline='') as write_file:
                writer = csv.writer(write_file)
                writer.writerow(theader)
                for row in teacher.query.all():
                    temp=[]
                    temp.append(row.id)
                    temp.append(row.name)
                    writer.writerow(temp)
                flash(f'Teacher\'s file downloaded','success')
    if request.method == 'POST' and 'import' in request.form:
        a=(request.form.get('Item_2'))
        df = pd.read_excel(request.files.get('file'))
        if a=="Student":
            student.query.delete()
            for index,row in df.iterrows():
                stemp=student(name=row[0],std=row[1],id=row[2])
                db.session.add(stemp)
                db.session.commit()
            flash(f'Done uploading student details','success')
        elif a=="Teacher":
            for index,row in df.iterrows():
                check=teacher.query.filter_by(id=row[1])
                if check is not None:
                    flash(f'Unique constraint violated\n','danger')
                    return redirect(url_for('home'))
                ttemp=teacher(name=row[0],id=row[1])
                db.session.add(ttemp)
                db.session.commit()
            flash(f'Done uploading teacher details','success')
        elif a=="Books":
            for index,row in df.iterrows():
                check=books.query.filter_by(id=row[1]).first()
                if check is not None:
                    flash(f'Unique constraint violated\n','danger')
                    return redirect(url_for('home'))
                btemp=books(id=row[1],date=str(row[0]),author=row[2],bname=row[3],publisher=row[4],place=row[5],year=row[6],edvol=row[7],pages=row[8],cost=row[9],orderno=row[10],supplier=row[11],classno=row[12])
                db.session.add(btemp)
                db.session.commit()
                print("done")
            flash(f'Done uploading book details','success')
        elif a=="Update":
            for index,row in df.iterrows():
                check=books.query.filter_by(id=row[1]).first()
                if check is None:
                    flash(f'There is no book with this id\n','danger')
                    return redirect(url_for('home'))
                db.session.delete(check)
                db.session.commit()
                btemp=books(id=row[1],date=row[0],author=row[2],bname=row[3],publisher=row[4],place=row[5],year=row[6],edvol=row[7],pages=row[8],cost=row[9],orderno=row[10],supplier=row[11],classno=row[12])
                db.session.add(btemp)
                db.session.commit()
                print("done")
            flash(f'Done uploading book details','success')
    return render_template('export.html',title='Export')

flag=True
