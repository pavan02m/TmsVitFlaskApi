from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from application import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qaz$02pm@localhost/timemanagementsys'

app.app_context().push()

db = SQLAlchemy(app)

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05

time_slots = (
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('10:30 - 11:30', '10:30 - 11:30'),
    ('11:30 - 12:30', '11:30 - 12:30'),
    ('12:30 - 1:30', '12:30 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_number = db.Column(db.String(6))
    seating_capacity = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.r_number


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(6))
    name = db.Column(db.String(25))

    def __repr__(self):
        return f'{self.uid} {self.name}'


class MeetingTime(db.Model):
    pid = db.Column(db.String(4), primary_key=True)
    time = db.Column(db.String(50))
    day = db.Column(db.String(15))

    def __repr__(self):
        return f'{self.pid} {self.day} {self.time}'


class Course(db.Model):
    course_number = db.Column(db.String(5), primary_key=True)
    course_name = db.Column(db.String(40))
    max_numb_students = db.Column(db.String(65))
    instructors = db.relationship('Instructor', secondary='course_instructor')

    def __repr__(self):
        return f'{self.course_number} {self.course_name}'


class CourseInstructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(
        db.String(5), db.ForeignKey('course.course_number'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(50))
    courses = db.relationship('Course', secondary='department_course')

    def __repr__(self):
        return self.dept_name


class DepartmentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    course_number = db.Column(
        db.String(5), db.ForeignKey('course.course_number'))


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.String(25))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    num_class_in_week = db.Column(db.Integer, default=0)
    course_number = db.Column(
        db.String(5), db.ForeignKey('course.course_number'))
    meeting_time_id = db.Column(
        db.String(4), db.ForeignKey('meeting_time.pid'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))

    def set_room(self, room):
        section = Section.query.get(self.id)
        section.room = room
        db.session.commit()

    def set_meetingTime(self, meetingTime):
        section = Section.query.get(self.id)
        section.meeting_time = meetingTime
        db.session.commit()

    def set_instructor(self, instructor):
        section = Section.query.get(self.id)
        section.instructor = instructor
        db.session.commit()
