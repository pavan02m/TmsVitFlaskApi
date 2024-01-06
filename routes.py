from application import app
from flask import request
from views import *
app.app_context().push()
# Room CRUD routes


@app.route("/")
def index():
    return " bacchi tu kar lenga dar mat"


@app.route('/rooms', methods=['POST'])
def create_room_route():
    data = request.get_json()
    return create_room(data['r_number'], data['seating_capacity'])


@app.route('/rooms', methods=['GET'])
def get_all_rooms_route():
    return get_all_rooms()


@app.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room_route(room_id):
    data = request.get_json()
    return update_room(room_id, data['r_number'], data['seating_capacity'])


@app.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room_route(room_id):
    return delete_room(room_id)


# Instructor CRUD routes


@app.route('/instructors', methods=['POST'])
def create_instructor_route():
    data = request.get_json()
    return create_instructor(data['uid'], data['name'])


@app.route('/instructors', methods=['GET'])
def get_all_instructors_route():
    return get_all_instructors()


@app.route('/instructors/<int:instructor_id>', methods=['PUT'])
def update_instructor_route(instructor_id):
    data = request.get_json()
    return update_instructor(instructor_id, data['uid'], data['name'])


@app.route('/instructors/<int:instructor_id>', methods=['DELETE'])
def delete_instructor_route(instructor_id):
    return delete_instructor(instructor_id)


# MeetingTime CRUD routes


@app.route('/meeting_times', methods=['POST'])
def create_meeting_time_route():
    data = request.get_json()
    return create_meeting_time(data['pid'], data['time'], data['day'])


@app.route('/meeting_times', methods=['GET'])
def get_all_meeting_times_route():
    return get_all_meeting_times()


@app.route('/meeting_times/<string:meeting_time_pid>', methods=['PUT'])
def update_meeting_time_route(meeting_time_pid):
    data = request.get_json()
    return update_meeting_time(meeting_time_pid, data['time'], data['day'])


@app.route('/meeting_times/<string:meeting_time_pid>', methods=['DELETE'])
def delete_meeting_time_route(meeting_time_pid):
    return delete_meeting_time(meeting_time_pid)

# Course CRUD routes


@app.route('/courses', methods=['POST'])
def create_course_route():
    data = request.get_json()
    return create_course(data['course_number'], data['course_name'], data['max_numb_students'], data['instructor_ids'])


@app.route('/courses', methods=['GET'])
def get_all_courses_route():
    return get_all_courses()


@app.route('/courses/<string:course_number>', methods=['PUT'])
def update_course_route(course_number):
    data = request.get_json()
    return update_course(course_number, data['course_name'], data['max_numb_students'], data['instructor_ids'])


@app.route('/courses/<string:course_number>', methods=['DELETE'])
def delete_course_route(course_number):
    return delete_course(course_number)

# Department CRUD routes


@app.route('/departments', methods=['POST'])
def create_department_route():
    data = request.get_json()
    return create_department(data['dept_name'], data['course_numbers'])


@app.route('/departments', methods=['GET'])
def get_all_departments_route():
    return get_all_departments()


@app.route('/departments/<string:dept_name>', methods=['PUT'])
def update_department_route(dept_name):
    data = request.get_json()
    return update_department(dept_name, data['course_numbers'])


@app.route('/departments/<string:dept_name>', methods=['DELETE'])
def delete_department_route(dept_name):
    return delete_department(dept_name)

# Section CRUD routes


@app.route('/sections', methods=['POST'])
def create_section_route():
    data = request.get_json()
    return create_section(data['section_id'], data['department_name'], data['num_class_in_week'],
                          data['course_number'], data['meeting_time_pid'], data['room_number'], data['instructor_uid'])


@app.route('/sections', methods=['GET'])
def get_all_sections_route():
    return get_all_sections()


@app.route('/sections/<string:section_id>', methods=['PUT'])
def update_section_route(section_id):
    data = request.get_json()
    return update_section(section_id, data['department_name'], data['num_class_in_week'],
                          data['course_number'], data['meeting_time_pid'], data['room_number'], data['instructor_uid'])


@app.route('/sections/<string:section_id>', methods=['DELETE'])
def delete_section_route(section_id):
    return delete_section(section_id)


# TIME TABLE GENERATION

@app.route('/timetable-generation')
def generate_timetable():
    return timetable(request)
