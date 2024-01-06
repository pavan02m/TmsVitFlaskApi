from application import app
from models import *
import random as rnd
from flask import request, jsonify
app.app_context().push()


class Data:
    def __init__(self):
        self._rooms = Room.query.all()
        self._meetingTimes = MeetingTime.query.all()
        self._instructors = Instructor.query.all()
        self._courses = Course.query.all()
        self._depts = Department.query.all()

    def get_rooms(self): return self._rooms

    def get_instructors(self): return self._instructors

    def get_courses(self): return self._courses

    def get_depts(self): return self._depts

    def get_meetingTimes(self): return self._meetingTimes


class Class:
    def __init__(self, id, dept, section, course):
        self.section_id = id
        self.department = dept
        self.course = course
        self.instructor = None
        self.meeting_time = None
        self.room = None
        self.section = section

    def get_id(self): return self.section_id

    def get_dept(self): return self.department

    def get_course(self): return self.course

    def get_instructor(self): return self.instructor

    def get_meetingTime(self): return self.meeting_time

    def get_room(self): return self.room

    def set_instructor(self, instructor): self.instructor = instructor

    def set_meetingTime(self, meetingTime): self.meeting_time = meetingTime

    def set_room(self, room): self.room = room


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        sections = Section.objects.all()
        for section in sections:
            dept = section.department
            n = section.num_class_in_week
            if n <= len(MeetingTime.objects.all()):
                courses = dept.courses.all()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_inst = course.instructors.all()
                        newClass = Class(self._classNumb, dept,
                                         section.section_id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes(
                        )[rnd.randrange(0, len(MeetingTime.objects.all()))])
                        newClass.set_room(
                            data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_instructor(
                            crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
            else:
                n = len(MeetingTime.objects.all())
                courses = dept.courses.all()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_inst = course.instructors.all()
                        newClass = Class(self._classNumb, dept,
                                         section.section_id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes(
                        )[rnd.randrange(0, len(MeetingTime.objects.all()))])
                        newClass.set_room(
                            data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_instructor(
                            crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)

        return self

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                            (classes[i].section_id != classes[j].section_id) and (classes[i].section == classes[j].section):
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].instructor == classes[j].instructor:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[
                0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[
                0]
            crossover_pop.get_schedules().append(
                self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(
                pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


data = Data()

############################################################################


def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    cls = {}
    for i in range(len(classes)):
        cls["section"] = classes[i].section_id
        cls['dept'] = classes[i].department.dept_name
        cls['course'] = f'{classes[i].course.course_name} ({classes[i].course.course_number}, ' \
                        f'{classes[i].course.max_numb_students}'
        cls['room'] = f'{classes[i].room.r_number} ({classes[i].room.seating_capacity})'
        cls['instructor'] = f'{classes[i].instructor.name} ({classes[i].instructor.uid})'
        cls['meeting_time'] = [classes[i].meeting_time.pid,
                               classes[i].meeting_time.day, classes[i].meeting_time.time]
        context.append(cls)
    return context


def timetable(request):
    schedule = []
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()

    return {'schedule': schedule, 'sections': Section.objects.all(),
            'times': MeetingTime.objects.all()}

############################################################################

# For rooms
# Create


def create_room(r_number, seating_capacity):
    new_room = Room(r_number=r_number, seating_capacity=seating_capacity)
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"message": "Room created successfully!"})

# Read


def get_all_rooms():
    rooms = Room.query.all()
    result = []
    for room in rooms:
        result.append({"id": room.id, "r_number": room.r_number,
                      "seating_capacity": room.seating_capacity})
    return jsonify({"rooms": result})

# Update


def update_room(room_id, r_number, seating_capacity):
    room = Room.query.get(room_id)
    room.r_number = r_number
    room.seating_capacity = seating_capacity
    db.session.commit()
    return jsonify({"message": "Room updated successfully!"})

# Delete


def delete_room(room_id):
    room = Room.query.get(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted successfully!"})


# ###################### INstructor ###############################
# Create
def create_instructor(uid, name):
    new_instructor = Instructor(uid=uid, name=name)
    db.session.add(new_instructor)
    db.session.commit()
    return jsonify({"message": "Instructor created successfully!"})

# Read


def get_all_instructors():
    instructors = Instructor.query.all()
    result = []
    for instructor in instructors:
        result.append(
            {"id": instructor.id, "uid": instructor.uid, "name": instructor.name})
    return jsonify({"instructors": result})

# Update


def update_instructor(instructor_id, uid, name):
    instructor = Instructor.query.get(instructor_id)
    instructor.uid = uid
    instructor.name = name
    db.session.commit()
    return jsonify({"message": "Instructor updated successfully!"})

# Delete


def delete_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({"message": "Instructor deleted successfully!"})


# ################### meeting time ###################
# Create


def create_meeting_time(pid, time, day):
    new_meeting_time = MeetingTime(pid=pid, time=time, day=day)
    db.session.add(new_meeting_time)
    db.session.commit()
    return jsonify({"message": "MeetingTime created successfully!"})

# Read


def get_all_meeting_times():
    meeting_times = MeetingTime.query.all()
    result = []
    for meeting_time in meeting_times:
        result.append({"pid": meeting_time.pid,
                      "time": meeting_time.time, "day": meeting_time.day})
    return jsonify({"meeting_times": result})

# Update


def update_meeting_time(meeting_time_pid, time, day):
    meeting_time = MeetingTime.query.get(meeting_time_pid)
    meeting_time.time = time
    meeting_time.day = day
    db.session.commit()
    return jsonify({"message": "MeetingTime updated successfully!"})

# Delete


def delete_meeting_time(meeting_time_pid):
    meeting_time = MeetingTime.query.get(meeting_time_pid)
    db.session.delete(meeting_time)
    db.session.commit()
    return jsonify({"message": "MeetingTime deleted successfully!"})


# ################# Course ####################
# Create
def create_course(course_number, course_name, max_numb_students, instructor_ids):
    new_course = Course(course_number=course_number,
                        course_name=course_name, max_numb_students=max_numb_students)
    for instructor_id in instructor_ids:
        instructor = Instructor.query.get(instructor_id)
        new_course.instructors.append(instructor)
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course created successfully!"})

# Read


def get_all_courses():
    courses = Course.query.all()
    result = []
    for course in courses:
        instructors = [{"id": instructor.id, "uid": instructor.uid,
                        "name": instructor.name} for instructor in course.instructors]
        result.append({"course_number": course.course_number, "course_name": course.course_name,
                       "max_numb_students": course.max_numb_students, "instructors": instructors})
    return jsonify({"courses": result})

# Update


def update_course(course_number, course_name, max_numb_students, instructor_ids):
    course = Course.query.get(course_number)
    course.course_name = course_name
    course.max_numb_students = max_numb_students
    course.instructors.clear()
    for instructor_id in instructor_ids:
        instructor = Instructor.query.get(instructor_id)
        course.instructors.append(instructor)
    db.session.commit()
    return jsonify({"message": "Course updated successfully!"})

# Delete


def delete_course(course_number):
    course = Course.query.get(course_number)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted successfully!"})


# ############### Department ###############
# Create
def create_department(dept_name, course_numbers):
    new_department = Department(dept_name=dept_name)
    for course_number in course_numbers:
        course = Course.query.get(course_number)
        new_department.courses.append(course)
    db.session.add(new_department)
    db.session.commit()
    return jsonify({"message": "Department created successfully!"})

# Read


def get_all_departments():
    departments = Department.query.all()
    result = []
    for department in departments:
        courses = [{"course_number": course.course_number, "course_name": course.course_name,
                    "max_numb_students": course.max_numb_students} for course in department.courses]
        result.append({"dept_name": department.dept_name, "courses": courses})
    return jsonify({"departments": result})

# Update


def update_department(dept_name, course_numbers):
    department = Department.query.filter_by(dept_name=dept_name).first()
    department.courses.clear()
    for course_number in course_numbers:
        course = Course.query.get(course_number)
        department.courses.append(course)
    db.session.commit()
    return jsonify({"message": "Department updated successfully!"})

# Delete


def delete_department(dept_name):
    department = Department.query.filter_by(dept_name=dept_name).first()
    db.session.delete(department)
    db.session.commit()
    return jsonify({"message": "Department deleted successfully!"})


# ################ SECTION ######################
# Create
def create_section(section_id, department_name, num_class_in_week, course_number, meeting_time_pid, room_number, instructor_uid):
    department = Department.query.filter_by(dept_name=department_name).first()
    course = Course.query.get(course_number)
    meeting_time = MeetingTime.query.get(meeting_time_pid)
    room = Room.query.filter_by(r_number=room_number).first()
    instructor = Instructor.query.filter_by(uid=instructor_uid).first()

    new_section = Section(section_id=section_id, department=department, num_class_in_week=num_class_in_week,
                          course=course, meeting_time=meeting_time, room=room, instructor=instructor)

    db.session.add(new_section)
    db.session.commit()
    return jsonify({"message": "Section created successfully!"})

# Read


def get_all_sections():
    sections = Section.query.all()
    result = []
    for section in sections:
        result.append({"section_id": section.section_id, "department_name": section.department.dept_name,
                       "num_class_in_week": section.num_class_in_week, "course_number": section.course.course_number,
                       "meeting_time_pid": section.meeting_time.pid, "room_number": section.room.r_number,
                       "instructor_uid": section.instructor.uid})
    return jsonify({"sections": result})

# Update


def update_section(section_id, department_name, num_class_in_week, course_number, meeting_time_pid, room_number, instructor_uid):
    section = Section.query.filter_by(section_id=section_id).first()
    department = Department.query.filter_by(dept_name=department_name).first()
    course = Course.query.get(course_number)
    meeting_time = MeetingTime.query.get(meeting_time_pid)
    room = Room.query.filter_by(r_number=room_number).first()
    instructor = Instructor.query.filter_by(uid=instructor_uid).first()

    section.department = department
    section.num_class_in_week = num_class_in_week
    section.course = course
    section.meeting_time = meeting_time
    section.room = room
    section.instructor = instructor

    db.session.commit()
    return jsonify({"message": "Section updated successfully!"})

# Delete


def delete_section(section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "Section deleted successfully!"})
