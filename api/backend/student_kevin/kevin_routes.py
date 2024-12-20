from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Kevin routes 

kevin = Blueprint('kevin', __name__)

@kevin.route('/community/<communityid>/housing', methods=['GET'])
# Route for retrieving housing for students in the same community
def community_housing(communityid):
    cleanliness_filter = request.args.get('cleanliness', type=int)
    lease_duration_filter = request.args.get('lease_duration', type=str)
    budget_filter = request.args.get('budget', type=int)
    
    query = '''
    SELECT s.Name, s.Major, s.Company, c.Location, s.HousingStatus, s.Budget, s.LeaseDuration, s.Cleanliness, s.Lifestyle, s.Bio
    FROM Student s
    JOIN CityCommunity c ON s.CommunityID=c.CommunityID
    WHERE c.Location = %s
    '''
    
    params = [communityid]  

    if cleanliness_filter is not None:
        query += ' AND s.Cleanliness >= %s'
        params.append(cleanliness_filter)

    if lease_duration_filter and lease_duration_filter != "Any":
        query += ' AND s.LeaseDuration = %s'
        params.append(lease_duration_filter)

    if budget_filter is not None:
        query += ' AND s.Budget <= %s'
        params.append(budget_filter)

    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))  
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


@kevin.route('/community/<communityid>/carpool', methods=['GET'])
def community_carpool(communityid):
    time_filter = request.args.get('commute_time', type=int)
    days_filter = request.args.get('commute_days', type=int)

    query = '''
    SELECT s.Name, s.Major, s.Company, c.Location, s.CarpoolStatus, s.Budget, s.CommuteTime, s.CommuteDays, s.Bio
    FROM Student s
    JOIN CityCommunity c ON s.CommunityID=c.CommunityID
    WHERE c.Location = %s
    '''
    params = [communityid]  

    if time_filter is not None:
        query += ' AND s.CommuteTime <= %s'
        params.append(time_filter)

    if days_filter is not None:
        query += ' AND s.CommuteDays <= %s'
        params.append(days_filter)


    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))  
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# retrieve kevin's profile
@kevin.route('/profile/<name>', methods=['GET'])
def get_profile(name):
    query = '''
    SELECT *
    FROM Student s
    JOIN CityCommunity c
    ON s.CommunityID = c.CommunityID
    WHERE s.Name = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (name, ))  
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# kevins profile - update
@kevin.route('/profile', methods=['PUT'])
def update_profile():
    the_data = request.json
    current_app.logger.info(the_data)

    #company = the_data.get('Company')
    #location = the_data.get('Location')
    housing_status = the_data.get('HousingStatus')
    carpool_status = the_data.get('CarpoolStatus')
    #lease_duration = the_data.get('LeaseDuration')
    budget = the_data.get('Budget')
    cleanliness = the_data.get('Cleanliness')
    lifestyle = the_data.get('Lifestyle')
    time = the_data.get('CommuteTime')
    days = the_data.get('CommuteDays')
    #bio = the_data.get('Bio')
    name = the_data.get('Name')

    query = '''
    UPDATE Student
    SET HousingStatus = %s,
        CarpoolStatus = %s, Budget = %s,
        Cleanliness = %s, Lifestyle=%s, CommuteTime=%s, CommuteDays=%s
    WHERE Name = %s
    '''
    
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (housing_status, carpool_status, budget, cleanliness, lifestyle, time, days, name))
    db.get_db().commit()

    response = make_response({"message": "Profile updated successfully"})
    response.status_code = 200
    return response

# obtain housing resources based on location
@kevin.route('/community/<community_id>/housing-resources', methods=['GET'])
def get_resources(community_id):
    query = '''
    SELECT * FROM
    CityCommunity c
    JOIN Housing h
    ON c.CommunityID=h.CommunityID
    WHERE c.CommunityID = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (community_id, ))  
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# route to provide feedback to advisor
@kevin.route('/feedback', methods=['POST'])
def give_feedback():
    data = request.json
    current_app.logger.info(data)

    description = data['Description']
    date = data['Date']
    rating = data['ProgressRating']
    student_id = data['StudentID']
    advisor_id = data['AdvisorID']

    query = '''
    INSERT INTO Feedback (Description, Date, ProgressRating, StudentID, AdvisorID)
        VALUES (%s, %s, %s, %s, %s)
    '''

    current_app.logger.info(query)
    connection = db.get_db()  
    cursor = connection.cursor()  

    cursor.execute(query, (description, date, rating, student_id, advisor_id))
    connection.commit() 

    cursor.close()  

    response = make_response("Successfully added feedback")
    response.status_code = 200
    return response

@kevin.route('/students/<student_id>/feedback/<feedback_id>', methods=['DELETE'])
def del_feedback(student_id, feedback_id):
    try:
        query = '''
        DELETE FROM Feedback
        WHERE StudentID = %s AND FeedbackID = %s
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (student_id, feedback_id))
        
        db.get_db().commit()

        if cursor.rowcount == 0:
            response = make_response(jsonify({
                "error": "No feedback entry found for the given student ID and feedback ID."
            }))
            response.status_code = 404
            return response
        
        response = make_response(jsonify({"message": "Feedback entry deleted successfully."}))
        response.status_code = 200
        return response
    except Exception as e:
        response = make_response(jsonify({"error": str(e)}))
        response.status_code = 500
        return response
    
    




from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Kevin routes 

kevin = Blueprint('kevin', __name__)

@kevin.route('/community/<communityid>/housing', methods=['GET'])
# Route for retrieving housing for students in the same community
def community_housing(communityid):
    cleanliness_filter = request.args.get('cleanliness', type=int)
    lease_duration_filter = request.args.get('lease_duration', type=str)
    budget_filter = request.args.get('budget', type=int)
    
    query = '''
    SELECT s.Name, s.Major, s.Company, c.Location, s.HousingStatus, s.Budget, s.LeaseDuration, s.Cleanliness, s.Lifestyle, s.Bio
    FROM Student s
    JOIN CityCommunity c ON s.CommunityID=c.CommunityID
    WHERE c.Location = %s
    '''
    
    params = [communityid]  

    if cleanliness_filter is not None:
        query += ' AND s.Cleanliness >= %s'
        params.append(cleanliness_filter)

    if lease_duration_filter and lease_duration_filter != "Any":
        query += ' AND s.LeaseDuration = %s'
        params.append(lease_duration_filter)

    if budget_filter is not None:
        query += ' AND s.Budget <= %s'
        params.append(budget_filter)

    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))  
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


@kevin.route('/community/<communityid>/carpool', methods=['GET'])
def community_carpool(communityid):
    time_filter = request.args.get('commute_time', type=int)
    days_filter = request.args.get('commute_days', type=int)

    query = '''
    SELECT s.Name, s.Major, s.Company, c.Location, s.CarpoolStatus, s.Budget, s.CommuteTime, s.CommuteDays, s.Bio
    FROM Student s
    JOIN CityCommunity c ON s.CommunityID=c.CommunityID
    WHERE c.Location = %s
    '''
    params = [communityid]  

    if time_filter is not None:
        query += ' AND s.CommuteTime <= %s'
        params.append(time_filter)

    if days_filter is not None:
        query += ' AND s.CommuteDays <= %s'
        params.append(days_filter)


    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))  
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# retrieve kevin's profile
@kevin.route('/profile/<name>', methods=['GET'])
def get_profile(name):
    query = '''
    SELECT *
    FROM Student s
    JOIN CityCommunity c
    ON s.CommunityID = c.CommunityID
    WHERE s.Name = %s
    '''
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query, (name, ))  
    theData = cursor.fetchall()
    
    # Format the response
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# kevins profile - update
@kevin.route('/profile', methods=['PUT'])
def update_profile():
    the_data = request.json
    current_app.logger.info(the_data)

    company = the_data.get('Company')
    location = the_data.get('Location')
    housing_status = the_data.get('HousingStatus')
    carpool_status = the_data.get('CarpoolStatus')
    lease_duration = the_data.get('LeaseDuration')
    budget = the_data.get('Budget')
    cleanliness = the_data.get('Cleanliness')
    lifestyle = the_data.get('Lifestyle')
    time = the_data.get('CommuteTime')
    days = the_data.get('CommuteDays')
    bio = the_data.get('Bio')
    name = the_data.get('Name')

    query = '''
    UPDATE Student
    SET Company = %s, Location = %s, HousingStatus = %s,
        CarpoolStatus = %s, Budget = %s, LeaseDuration = %s, 
        Cleanliness = %s, Lifestyle=%s, CommuteTime=%s, CommuteDays=%s, Bio = %s
    WHERE Name = %s
    '''
    
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (company, location, housing_status, carpool_status, budget, lease_duration, cleanliness, lifestyle, time, days, bio, name))
    db.get_db().commit()

    response = make_response({"message": "Profile updated successfully"})
    response.status_code = 200
    return response

# obtain housing resources based on location
@kevin.route('/community/<community_id>/housing-resources', methods=['GET'])
def get_resources(community_id):
    query = '''
    SELECT * FROM
    CityCommunity c
    JOIN Housing h
    ON c.CommunityID=h.CommunityID
    WHERE c.CommunityID = %s
    '''
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query, (community_id, ))  
    theData = cursor.fetchall()
    
    # Format the response
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response



# route to provide feedback to advisor
@kevin.route('/feedback', methods=['POST'])
def give_feedback():
    data = request.json
    current_app.logger.info(data)

    description = data['Description']
    date = data['Date']
    rating = data['ProgressRating']

    student = st.session_state['first_name']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT StudentID, AdvisorID FROM Student WHERE Name = %s', (student,))
    result = cursor.fetchone()

    student_id, advisor_id = result


    insert_query = '''
    INSERT INTO Feedback (Description, Date, ProgressRating, StudentID, AdvisorID)
        VALUES (%s, %s, %s, %s, %s)
    '''

    cursor.execute(insert_query, (description, date, rating, student_id, advisor_id))
    db.commit()

    response = make_response("Feedback Submitted")
    response.status_code = 200
    return response




