import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

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

    categories=Category.query.all()
    categories_all=[c.format() for c in categories]

    categories_return=[]
    for cat in categories_all:
      categories_return.append(cat['type'])
    
    return jsonify({
      'success':True,
      'questions':paginated_questions,
      'total_questions':len(selection),
      'categories':categories_return,
      'current_category':categories_return
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
    question = Question.query.filter(Question.id == id).one_or_none()

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
  @app.route('/questions',methods=['POST'])
  def add_question():

    body=request.get_json()

    if not body:
      abort(400)

    search_term=body.get('searchTerm',None)

    if search_term:
      questions=Question.query.filter(Question.question.contains(search_term)).all()

      if not questions:
        abort(404)

      questions_found=[q.format() for q in questions]
      questions_asc=Question.query.order_by(Question.id).all()

      #query for categories
      categories=Category.query.all()
      categories_all=[c.format() for c in categories]

      return jsonify({
        'success':True,
        'questions':questions_asc,
        'total_questions':len(questions_asc),
        'current_category':categories_all
        })

    new_question=body.get('question',None)
    new_answer=body.get('answer',None)
    new_category=body.get('category',None)
    new_difficulty=body.get('difficulty',None)

    if (not new_question) or (not new_answer) or (not new_difficulty) or (not new_category):
      abort(400)


    try:
      question=Question(
        question=new_question,
        answer=new_answer,
        category=new_category,
        difficulty=new_difficulty
        )

      question.insert()

      selection=Question.query.filter(Question.id).all()
      paginated_questions=pagination(request,selection)

      #return successful response of paginated questions

      return jsonify({
        'successful':True,
        'created':question.id,
        'questions':paginated_questions,
        'total_questions':len(selection)
        })

    except:
      abort(422)









  



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
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories=Category.query.all()
    if not categories:
      abort(404)

    formatted_categories=[c.format() for c in categories]
    #empty categories list
    categories_list=[]
    for cat in formatted_categories:
      categories_list.append(cat['type'])

    return jsonify({
      'success':True,
      'categories':categories_list
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

    