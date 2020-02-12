import bottle
from bottle import run, route, static_file, get, template, request
import smtplib, ssl


from db import session
from models import Teacher as teacher, Pupil as pupil, Question as question, Choice as choice,\
    Queans as queans, Queanstest as queanstest, Testresults as test_results, Testsubmission as test_submission, \
    Test as test
import json

#app = Bottle()
app = bottle.default_app()

@route('/hello')
def hello():
    return json.dumps({"data": "App working! Please use the api"})

@route('/show_teachers')
def show_teacher():
    obj = session.query(teacher).all()
    t_list = [data.name for data in obj]
    return json.dumps({"data": t_list})

@route('/show_pupil')
def show_pupil():
    obj = session.query(pupil).all()
    p_list = [data.first_name for data in obj]
    return json.dumps({"data": p_list})

@route('/show_questions')
def show_questions():
    obj = session.query(question).all()
    q_list = [{"id": data.id, "ques": data.name} for data in obj]
    return json.dumps({"data": q_list}, indent=4)

@route('/show_choices')
def show_choice():
    obj = session.query(choice).all()
    c_list = [{"id": data.id, "choice": data.name} for data in obj]
    return json.dumps({"data": c_list}, indent=4)

@route('/show_tests')
def show_test():
    test_obj = session.query(test).all()
    t_list = [{"id": data.id, "name": data.name} for data in test_obj]
    return json.dumps({"data": t_list})

@route('/register_teacher')
def show_teacher():
    return serve_static_file('teacher_register.tpl')

@route('/show_questions_choices')
def show_questions_choices():
    """
    This methid will list of all questions and their choices
    """
    q_c = session.query(queans).all()
    q_ans_obj = {}
    for obj in q_c:
        if obj.question_id not in q_ans_obj.keys():
            q_ans_obj[obj.question_id] = [obj.choice_id]
        else:
            q_ans_obj[obj.question_id].append(obj.choice_id)

    # retrivieng ques and ans from their tables with text
    q_ans_obj_text_list = []
    
    for ques, ch in q_ans_obj.items():
        q_ans_obj_text = {}
        q_obj = session.query(question).filter(question.id==ques).all()

        if q_obj[0].id not in q_ans_obj_text.keys():
            q_ans_obj_text["name"] = q_obj[0].name
            q_ans_obj_text["id"]   = q_obj[0].id
            q_ans_obj_text["choice"] = []

        for ch_obj in ch:
            c_data = {}
            c_obj = session.query(choice).filter(choice.id==ch_obj).first()

            if c_obj.id not in q_ans_obj_text["choice"]:
                c_data.update({"id": c_obj.id, "name": c_obj.name})
                q_ans_obj_text["choice"].append(c_data)

        q_ans_obj_text_list.append(q_ans_obj_text)
        q_ans_obj_text = {}

    return {"data": q_ans_obj_text_list}

@route('/show_test_questions/<test_id>')
def show_test_questions(test_id):
    """
    This function helps to display 
    the questions and their choice 
    with the given test id
    
    input_data
    {
    "test_id": 1
    }
    
    """
    if test_id:
        test_obj = session.query(queanstest).filter(queanstest.test_id==test_id).all()
        print("test obj", test_obj)
        data = []
        data_obj = {}
        t_obj = session.query(test).filter(test.id == test_obj[0].test_id).all()[0]
        t_name, t_id = t_obj.name, t_obj.id
        data_obj.update({"test_id": t_id, "test_name": t_name, "ques_ans": []})
        for obj in test_obj:
            print("obj", vars(obj))
            q_obj = session.query(question).filter(question.id == obj.ques_id_id).first()
            
            print("q_obj", q_obj)
            
            q_c = session.query(queans).filter(queans.question_id == obj.ques_id_id).all()

            q_ans_obj = {}
            for obj in q_c:
                if obj.question_id not in q_ans_obj.keys():
                    q_ans_obj[obj.question_id] = [obj.choice_id]
                else:
                    q_ans_obj[obj.question_id].append(obj.choice_id)

            print(q_ans_obj)
            # retrivieng ques and ans from their tables with text
            q_ans_obj_text_list = []
            
            for ques, ch in q_ans_obj.items():
                q_ans_obj_text = {}
                q_q_obj = session.query(question).filter(question.id==ques).all()
                print("q Obj", q_q_obj[0].id, q_q_obj[0].name)
                if q_q_obj[0].id not in q_ans_obj_text.keys():
                    q_ans_obj_text["choice"] = []
                for ch_obj in ch:
                    c_data = {}
                    c_obj = session.query(choice).filter(choice.id==ch_obj).first()
                    if c_obj.id not in q_ans_obj_text["choice"]:
                        c_data.update({"id": c_obj.id, "name": c_obj.name})
                        q_ans_obj_text["choice"].append(c_data)
                q_ans_obj_text_list.append(q_ans_obj_text)
                q_ans_obj_text = {}
            data_obj['ques_ans'].append({"ques_id": q_obj.id, "ques_name": q_obj.name, 
                    "ques_choice_data": q_ans_obj_text_list[0]["choice"]})
        return json.dumps({"data": data_obj}, indent=4)
    else:
        return json.dumps({"data": "invalid format"})
        
@route('/add_teacher', method="POST")
def add_teacher():
    data = request.json
    t_obj = teacher(name=data['name'], contact=data['contact'])
    session.add(t_obj)
    session.commit()
    session.close()
    return json.dumps({"data": "{} - Added Succesfully ".format(data['name'])})

@route('/add_test', method="POST")
def add_test():
    data = request.json
    t_obj = test(name=data['name'])
    session.add(t_obj)
    session.commit()
    session.close()
    return json.dumps({"data": "{} Added Succesfully".format(data['name'])})
    

@route('/pupil_register', method="POST")
def pupil_register():
    data = request.json
    p_obj = pupil(first_name=data['first_name'], sur_name=data['sur_name'], email_add=data['email_add'])
    session.add(p_obj)
    session.commit()
    session.close()
    return json.dumps({"data": "{} - Added Succesfully ".format(data['first_name'])}) 

@route('/add_question', method="POST")
def add_question():
    data = request.json
    if isinstance(data['name'], str):
        return json.dumps({"data": "Submit questions must be in valid format"})
    q_obj = question(name=data['name'])
    session.add(q_obj)
    session.commit()
    session.close()
    return json.dumps({"data": "{} - Added Succesfully ".format(data['name'])}) 

@route('/add_choice', method="POST")
def add_choice():
    data = request.json
    c_obj = choice(name=data['name'])
    session.add(c_obj)
    session.commit()
    session.close()
    return json.dumps({"data": "{} - Added Succesfully ".format(data['name'])})

@route('/assign_ques_choice', method="POST")
def add_ques_choice():
    """
    This function accepts question id 
    and multiple choice ids
    
    Note more than 3 nor less than 3 choices cannot be
    assigned
    
    input format:
    {
    "question_id": 1,
    "choice_id": [2, 5, 10]
    }
    
    """
    data = request.json
    if isinstance(data['choice_id'], list) and len(data["choice_id"]) == 3:
        
        que_obj = session.query(question).filter(question.id == data["question_id"]).all()
        if not que_obj:
            return json.dumps({"data": "Question id not found"})

        ques_in_queans = session.query(question).filter(question.id == data["question_id"]).all()
        if ques_in_queans:
            return json.dumps({"data": "Question id exists"})

        choice_obj = session.query(choice.id).all()
        for ch in data['choice_id']:
            que_choice_obj = queans(question_id = data['question_id'], choice_id=ch)
            session.add(que_choice_obj)
        session.commit()
        session.close()
        return json.dumps({"data": "Question {} with Choices {} - Added Succesfully ".format(
                            data['question_id'], data['choice_id'])})
    else:
        return json.dumps({"data": "Invalid data format"})
    
@route('/assign_ques_test', method="POST")
def assign_ques_test():
    """
    This function accepts question id 
    and test id and teacher id who creates the test
    
    # questions can be n number for a test
    
    input format:
    {
    "question_id": [1,2,3,4,5],
    "test_id": 1,
    "teacher_id": 1
    }
    
    """
    data = request.json
    if isinstance(data['question_id'], list) and isinstance(data['test_id'], int) and isinstance(data['teacher_id'], int):
        teacher_obj = session.query(teacher).filter(teacher.id == data['teacher_id']).first()
        que_obj = session.query(question.id).all()
        
        print("*"*20, [id[0] for id in que_obj])
        
        if teacher_obj:
            for ques in data['question_id']:
                if ques not in [id[0] for id in que_obj]:
                    return json.dumps({"data": "Question id's not found"})
                que_test_teach_obj = queanstest(ques_id_id=ques, test_id=data['test_id'], teacher_id=data['teacher_id'])
                session.add(que_test_teach_obj)
            session.commit()
            session.close()
            return json.dumps({"data": "Test  Succesfully "})
        else:
            return json.dumps({"data": "No records found for teacher"})
    else:
        return json.dumps({"data": "Invalid data format"})

@route('/submit_test', method="POST")
def test_sumbission():
    """
    This function accepts question id and selected choice id
    and test id and teacher id who creates the test and pupil 
    id who writes the test
    
    input format:
    {
    "question_ans": {"1": 2, "2": 3, "4":1},
    "test_id": 1,
    "teacher_id": 1
    "pupil_id": 1
    }
    
    """
    data = request.json
    
        
    if isinstance(data['question_ans'], dict) and isinstance(data['test_id'], int) and isinstance(data['teacher_id'], int)\
        and isinstance(data['pupil_id'], int):
        for que, ans in data['question_ans'].items():
            test_submission_obj = test_submission(pupil_id = data['pupil_id'], ques_id=int(que), test_id=data['test_id'], teacher_id=data['teacher_id'], choice_id=ans)
            session.add(test_submission_obj)
        session.commit()
        session.close()
        return json.dumps({"data": "Test  Succesfully submitted"})
    else:
        return json.dumps({"data": "Invalid data format"})

@route('/show_submitted_test_list/<test_id>')
def show_submitted_tests(test_id):
    """
    This function recieves a test id 
    and return backs with actual text of the data
    
    It collects the test data from test_submission table
    and pairs the ques and answers 
    
    test_ans syntax: {test_id: [{ques: ans}, {ques: ans}]}
    test_ans: {1: [{1:2}, {2:4}]}
    
    Then calls the 'show_test_questions' with test_id
    to get actual textual represenation of the test_ans
    to get below format

    output format:
    {"ques": "pupil_entered_choice"}
    
    ex output:
    {"5-2": 3, "10*10": 10}
    """
    t_obj = session.query(test_submission).filter(test_submission.test_id==test_id).all()
    test_ans = {} # {1: [{1:2}, {2:4}]}

    for obj in t_obj:
        if obj.test_id not in test_ans.keys():
            test_ans[obj.test_id] = []
        test_ans[obj.test_id].append({obj.ques_id: obj.choice_id})  

    data = json.loads(show_test_questions(test_id))
    
    ques_ans_list = data["data"]["ques_ans"]
    
    
    #ques_ans_list data looks like: 
    #[{u'ques_id': 1, u'ques_choice_data': [{u'id': 1, u'name': u'0'}, 
    #    {u'id': 2, u'name': u'10'}, {u'id': 4, u'name': u'20'}], u'ques_name': u'10 - 10'}, 
    #{u'ques_id': 2, u'ques_choice_data': [{u'id': 2, u'name': u'10'}, {u'id': 4, u'name': u'20'}, 
    #    {u'id': 5, u'name': u'25'}], u'ques_name': u'5 * 4'}, 
    #{u'ques_id': 3, u'ques_choice_data': [{u'id': 4, u'name': u'20'}, {u'id': 5, u'name': u'25'}, 
    #    {u'id': 6, u'name': u'7'}], u'ques_name': u'which of the below number is odd number'}]


    final_data = {"test_data": []}
    for data in test_ans[int(test_id)]:
        for q_data in ques_ans_list:
            if q_data["ques_id"] == list(data.keys())[0]:
                ans = [obj['name'] for obj in q_data['ques_choice_data'] 
                                if obj['id'] == list(data.values())[0]][0]
                #final_data.update({q_data['ques_name']: ans})
                final_data['test_data'].append({q_data['ques_name']: ans})

    final_data.update({"test_id": test_id, "pupil_id": t_obj[0].pupil_id})
    return json.dumps(final_data, indent=4)

@route('/test_result', method="POST")
def test_result():
    """
    This function saves the results of the test
    by the teacher with status and perc with pupil id
    
    input format:
    {
    "pupil_id": 1,
    "test_id": 1,
    "status": "pass",
    "test_data": [{"ques_1": "right ans"}, {"ques_2": "right_ans"}, {"ques_3": "wrong_ans"}],
    "correct_answers": ["ques_1", "ques_2"],
    "teacher_id": 1
    }
    
    percentage will be internally caluclated
    100.0 * ques_ans/total_ques 
    
    ex: 100.0 * 3/5 = 60.0
    
    """
    data = request.json
    for k, v in data.items():
        print("type", k, type(v))
        
    if isinstance(data['pupil_id'], int) and isinstance(data['test_id'], int) and (isinstance(str(data['status']), str) and data['status'] in ["pass", "fail"])\
        and isinstance(data['teacher_id'], int):
        
        # getting the teacher id from the Queanstest table
        # as only the right teacher has to submit the result 
        
        teacher_obj = session.query(queanstest).filter(queanstest.test_id == data['test_id']).first()
        
        if data['teacher_id'] == teacher_obj.teacher_id:
        
            # caluclate percentage
            no_of_ques = len(data["test_data"])
            no_of_correct_ans = len(data["correct_answers"])
            
            # percentage
            perc = 100.0 * no_of_correct_ans/ no_of_ques
        
            test_result_submission = test_results(pupil_id=data['pupil_id'], test_id=data['test_id'], status=data['status'], perc=round(perc))
            session.add(test_result_submission)
            session.commit()
            
            # unblock and configure below code to send mail as a notification
            # data = "Test Status: {} , Percentage: {}".format(data['status'], perc)
            # send_email_to_pupil(data)

        else:
            json.dumps({"data": "No permission to submit result for other teacher tests"})
        session.close()
        return json.dumps({"data": "Test  Succesfully submitted"})
    else:
        return json.dumps({"data": "Invalid data format"})

@route('/show_student_test_status')
def show_student_test_status():
    std_test_status_obj = session.query(test_results).all()
    std_test_res_list = []
    for res_obj in std_test_status_obj:
            dictret = dict(res_obj.__dict__); 
            dictret.pop('_sa_instance_state', None)
            std_test_res_list.append(dictret)
    return json.dumps({"data": std_test_res_list}, indent=4)

def send_email_to_pupil(data):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "my@gmail.com"  # Enter your address
    receiver_email = "your@gmail.com"  # Enter receiver address
    password = input("Type your password and press enter: ")
    message = """\
    Subject: Hi there

    This message is sent from Quiz app . 
    
    {}
    """.format(data)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

@route('/static/<filename:path>')
def serve_static_file(filename):
    return static_file(filename, root='../static')
    
@route('/remove_ques_id/<test_id>')
def delete_test_id(test_id):
    session.query(test_submission).filter(test_submission.test_id == test_id).delete()
    session.commit()
    print("ddelet")
    


if __name__ == "__main__":
    #run(app, host='0.0.0.0', port=9060)
    #run(app, host='0.0.0.0')
    run(host="0.0.0.0", port=8080, debug=True, reloader=True)