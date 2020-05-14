import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)


  # @app.route('/')
  # def index():
  #   return jsonify({
  #     'success':True
  #     })


  cors=CORS(app,resources={r"/api/*":{"origins":"*"}})

  #CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods","GET,PUT,POST,PATCH,DELETE,OPTIONS")
    return response


  def pagination(request,selection):
    page=request.args.get('page',1,type=int)
    #calculate stant and end slicing

    start=(page-1)*QUESTIONS_PER_PAGE
    end=start+QUESTIONS_PER_PAGE
    #format selection into list of dicts and slices using python slciing

    cur_questions=[p.format() for p in selection]

    return cur_questions[start:end]


  @app.route('/')
  def index():
    return jsonify({
      "hello":"word;"
      })
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''


  #-------endpoints for questions--------#
  @app.route('/questions',methods=['GET'])
  def get_questions():

    selection=Question.query.order_by(Question.id).all()
    paginated_questions=pagination(request,selection)

    if len(paginated_questions)==0:
      abort(404)
    categories = Category.query.all()
    categories = {category.id:category.type for category in categories}
    
    return jsonify({
      'success':True,
      'questions':paginated_questions,
      'total_questions':len(selection),
      'categories':categories,
      'current_category':"Null"
      })



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions/<int:id>',methods=['DELETE'])
  def delete_question(id):
    question = Question.query.filter(Question.id == id).first()

    if not question:
      abort(400)

    try:
      question.delete()
      return jsonify({
        'success':True,
        'deleted':id
        })
    except:
      abort(422)



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    question = body.get('question', '')
    answer = body.get('answer','')
    category =  body.get('category', '')
    difficulty = body.get('difficulty', '')
    if not (question and answer and category and difficulty):
      abort(422)
    new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
    new_question.insert()
    question_id = new_question.id
    return jsonify({
      "success": True,
      "question_id": question_id
    })

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body.get('searchTerm', '')
    if not search_term:
      abort(422)
    question=Question.query.filter(Question.question.contains(search_term)).all()
    questions=[q.format() for q in question]

    return jsonify({
      "success": True,
      "total_questions": len(questions),
      "questions": questions,
      "current_category": "Null"
    })
    
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  #-----endpoints for categories---#
  @app.route("/categories")
  def get_categories():
    categories = Category.query.all()
    categories = {category.id:category.type for category in categories}
    return jsonify({
        "success": True,
        "categories": categories,
        "total_categories": len(categories)
    })








  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown.
  '''

  @app.route('/categories/<string:cat>/questions',methods=['GET'])
  def get_questions_of_specific_category(cat):

    #query all questions that match cat
    selection=Question.query.filter(Question.category==str(cat)).order_by(Question.id).all()

    if not selection:
      abort(400)
    paginated_questions=pagination(request,selection)

    if not paginated_questions:
      abort(404)

    return jsonify({
      'success':True,
      'questions':paginated_questions,
      'total_questions':len(selection),
      'current_category':cat
      })





  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    data = json.loads(request.data)
    validation = ['previous_questions', 'quiz_category']
    for key in validation:
      if key not in data.keys():
        abort(400)
    result = Question.query.filter(Question.id.notin_(data['previous_questions'])).all()
    questions_unfiltered = [question.format() for question in result]
    questions_filtered = [question for question in questions_unfiltered if question['category'] == data['quiz_category']['id']]
    if not questions_filtered:
      abort(404)
    question = random.choice(questions_filtered)

    return jsonify({
      'success': True,
      'question': question
    }), 200



  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success':False,
      'error':400,
      'message':'bad request'
      })

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'messge':"resource not found"
      })

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success':False,
      'error':405,
      'messge':"method not allowed"
      })
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'messge':"unprocessable"
      })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    