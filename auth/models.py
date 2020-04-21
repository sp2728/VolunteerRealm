import enum
from flask_login import UserMixin
from app import db


class Permission(enum.Enum):
    ADMIN = 1
    USER = 2
    NONE = 10  # can be used to disable users


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(15), unique=True)
    gender = db.Column(db.String(10))
    permission = db.Column(db.Enum(Permission), default=Permission.USER)

    def is_admin(self):
        return self.permission == Permission.ADMIN

    def is_none(self):
        return self.permission == Permission.NONE


class Organisation(db.Model):
    org_id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(100), unique=True)
    org_address= db.Column(db.String(100))


class Jobs(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    job_description = db.Column(db.String(2000))
    '''job_location = db.column(db.String(100))'''

'''
class OrgJobs(db.Model):
    orgJob_id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.org_id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))


class UserOrgJobs(db.Model):
    uoj_id = db.Column(db.Integer, primary_key=True)
    orgJob_id = db.Column(db.Integer, db.ForeignKey('org_jobs.orgJob_id'))
    id = db.Column(db.Integer, db.ForeignKey('User.id'))
'''