from flask import Flask, render_template, request, session, abort
from models import *
import pdb

app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': 'sid',
    'db': 'book',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
engine= 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def teacherlogin():
    if request.method == 'POST':
        u_name = request.form.get('id')
        u_pwd = request.form.get('password')
        obj = Teacher.query.filter(Teacher.name == u_name, Teacher.password == u_pwd).first()
        all = Student.query.all()
        session["main_key"] = obj.id
        if obj is not None:
            return render_template('options.html', all=all)
        else:
            abort(401)
    else:
        return render_template('login_teacher.html')


@app.route("/viewteacher", methods=['POST', 'GET'])
def viewMarks():
    mar = {}
    student = Student.query.all()
    marks = Marks.query.all()

    for s in student:
        mar[s.Name] = []
        admno = s.admno
        for m in marks:
            if m.admno == admno:
                if m.id == session["main_key"]:
                    mar[s.Name].append({'admno': m.admno, 'marks': m.marks})
    return render_template('marksview.html',mar=mar)

@app.route('/loginstudent', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        u_name = request.form.get('admno')
        u_pwd = request.form.get('password')
        log = Student.query.filter(Student.admno == u_name, Student.password == u_pwd).first()
        result = Marks.query.filter_by(admno=u_name).all()
        if log is not None:
            return render_template('MarksViewStudent.html', u_name=u_name, result=result)
        else:
            abort(401)
    else:
        return render_template('login_student.html')


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        admno = request.form.get('admno')
        marks = request.form.get('marks')
        addid = request.form.get('id')
        loginid = str(session["main_key"])
        if loginid == addid:
            query = Marks(admno, marks, addid)
            db.session.add(query)
            db.session.commit()
            return 'record added'
        else:
            abort(401)


@app.route("/delete/<admno>/<marks>", methods=['GET', 'POST'])
def delete(admno,marks):
    queryrm = Marks.query.filter_by(admno=admno, marks=marks).all()
    for i in queryrm:
        db.session.delete(i)
        db.session.commit()
    return 'record removed'


@app.route("/addoption")
def addoption():
    return render_template('markscrud.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
