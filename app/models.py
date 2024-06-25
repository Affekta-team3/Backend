from app import db
import uuid

class Problem(db.Model):
    __tablename__ = 'problem'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    input_format = db.Column(db.String(100), nullable=True)
    output_format = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.Integer, nullable=False)
    totalSubmissions = db.Column(db.Integer, nullable=False, default=0)
    successfulSubmissions = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f'<Problem {self.title}>'

class Submission(db.Model):
    __tablename__ = 'submission'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_id = db.Column(db.String(36), db.ForeignKey('problem.id'), nullable=False)
    code_text = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(200), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    memory = db.Column(db.Integer, nullable=False)
    
    problem = db.relationship('Problem', backref=db.backref('submissions', lazy=True))
    
    def __repr__(self):
        return f'<Submission {self.id}>'

class User(db.Model):
    __tablename__ = 'user'
    
    userId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    totalSubmissions = db.Column(db.Integer, nullable=False, default=0)
    successfulSubmissions = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f'<User {self.username}>'
