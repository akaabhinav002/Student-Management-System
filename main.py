from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import UserMixin
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json


# MY db connection
app = Flask(__name__)
app.secret_key = 'kusumachandashwini'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'mite'
# app.config['MYSQL_DB'] = 'student db'
db_user='root'
db_password='mite'
db_host='localhost'
db_name='students'
# db = MySQL(app)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mite@localhost/students'
db = SQLAlchemy(app)

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# # app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
# app.config['SQLALCHEMY_DATABASE_URL']='mysql://root:mite@localhost/students'
# db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class Department(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    branch=db.Column(db.String(100))

# class Attendence(db.Model):
#     aid=db.Column(db.Integer,primary_key=True)
#     rollno=db.Column(db.String(100))
#     attendance=db.Column(db.Integer())
class attendance(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(20))
    course1 = db.Column(db.Integer)
    course2 = db.Column(db.Integer)
    course3 = db.Column(db.Integer)
    course4 = db.Column(db.Integer)
    course5 = db.Column(db.Integer)
    
class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))





class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(50))
    sname=db.Column(db.String(50))
    sem=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    branch=db.Column(db.String(50))
    email=db.Column(db.String(50))
    number=db.Column(db.String(12))
    address=db.Column(db.String(100))
    

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/studentdetails')
def studentdetails():
    # query=db.engine.execute(f"SELECT * FROM `student`") 
    query=Student.query.all() 
    return render_template('studentdetails.html',query=query)

@app.route('/triggers')
def triggers():
    # query=db.engine.execute(f"SELECT * FROM `trig`") 
    query=Trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/department',methods=['POST','GET'])
def department():
    if request.method=="POST":
        dept=request.form.get('dept')
        query=Department.query.filter_by(branch=dept).first()
        if query:
            flash("Department Already Exist","warning")
            return redirect('/department')
        dep=Department(branch=dept)
        db.session.add(dep)
        db.session.commit()
        flash("Department Addes","success")
    return render_template('department.html')

@app.route('/addattendance',methods=['POST','GET'])
# def addattendance():
#     # query=db.engine.execute(f"SELECT * FROM `student`") 
#     query=Student.query.all()
#     if request.method=="POST":
#         rollno=request.form.get('rollno')
#         attend=request.form.get('attend')
#         print(attend,rollno)
#         atte=Attendence(rollno=rollno,attendance=attend)
#         db.session.add(atte)
#         db.session.commit()
#         flash("Attendance added","warning")
def addattendance():
    query = Student.query.all()

    if request.method == "POST":
        rollno = request.form.get('rollno')
        course1 = request.form.get('course1')
        course2 = request.form.get('course2')
        course3 = request.form.get('course3')
        course4 = request.form.get('course4')
        course5 = request.form.get('course5')

         

        atte = attendance(rollno=rollno, course1=course1, course2=course2, course3=course3, course4=course4, course5=course5)
        db.session.add(atte)
        db.session.commit()
        flash("Attendance added", "warning")
    try:
        # Insert into the attendance table
        # This is where your trigger will be executed
        # The trigger will check the attendance values before inserting
        # If any value is not between 0 and 100, it will raise an error
        # which will be caught here
        pass  # Insert query goes here

    except Exception as e:
        return f'Error: {str(e)}'

    

        
    return render_template('attendance.html',query=query)

@app.route('/search',methods=['POST','GET'])

def search():
    if request.method == "POST":
        rollno = request.form.get('roll')
        bio = Student.query.filter_by(rollno=rollno).first()
        attend = attendance.query.filter_by(rollno=rollno).first()
        return render_template('search.html', bio=bio, attend=attend)

    return render_template('search.html')
# def search():
#     if request.method == "POST":
#         rollno = request.form.get('roll')
#         student = Student.query.filter_by(rollno=rollno).first()

#         # Check if the student exists
#         if student:
#             # Fetch attendance details for the student
#             attend = attendance.query.filter_by(rollno=rollno).first()
#             return render_template('search.html', student=student, attend=attend)

#         flash("Student not found", "danger")

#     return render_template('search.html')
@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    post=Student.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    # db.engine.execute(f"DELETE FROM `student` WHERE `student`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/studentdetails')


@app.route("/edit/<string:id>",methods=['POST','GET'])
@login_required
def edit(id):
    # dept=db.engine.execute("SELECT * FROM `department`")    
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        # query=db.engine.execute(f"UPDATE `student` SET `rollno`='{rollno}',`sname`='{sname}',`sem`='{sem}',`gender`='{gender}',`branch`='{branch}',`email`='{email}',`number`='{num}',`address`='{address}'")
        post=Student.query.filter_by(id=id).first()
        post.rollno=rollno
        post.sname=sname
        post.sem=sem
        post.gender=gender
        post.branch=branch
        post.email=email
        post.number=num
        post.address=address
        db.session.commit()
        flash("Slot is Updates","success")
        return redirect('/studentdetails')
    dept=Department.query.all()
    posts=Student.query.filter_by(id=id).first()
    return render_template('edit.html',posts=posts,dept=dept)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        newuser=User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addstudent',methods=['POST','GET'])
@login_required
def addstudent():
    # dept=db.engine.execute("SELECT * FROM `department`")
    
    dept = Department.query.all()

    if request.method == "POST":
        rollno = request.form.get('rollno')
        sname = request.form.get('sname')
        sem = request.form.get('sem')
        gender = request.form.get('gender')
        branch = request.form.get('branch')
        email = request.form.get('email')
        num = request.form.get('num')
        address = request.form.get('address')
        
        # Check if roll number already exists
        existing_student = Student.query.filter_by(rollno=rollno).first()
        if existing_student:
            flash("Roll number already exists. Please enter a different roll number.", "danger")
        else:
            # Insert the student record into the database
            new_student = Student(rollno=rollno, sname=sname, sem=sem, gender=gender, branch=branch, email=email, number=num, address=address)
            db.session.add(new_student)
            db.session.commit()
            flash("Student Added", "info")

        try:
        # Insert into the attendance table
        # This is where your trigger will be executed
        # The trigger will check the attendance values before inserting
        # If any value is not between 0 and 100, it will raise an error
        # which will be caught here
            pass  # Insert query goes here

        except Exception as e:
                return f'Error: {str(e)}'

    return render_template('student.html', dept=dept)

@app.route('/about')
def about():
    return render_template('about.html')
    


@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    