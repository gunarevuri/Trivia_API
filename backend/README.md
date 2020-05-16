# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized.Here instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
requirements.txt file had all required packages to run project and respective versions also mentioned . if you face any problem with versions you can delete package name from `requirements.txt` file and download that package separately.

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
In this project we use postgres database for backend. you can use sqlite also by updating in config file.
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Resource endpoint library
### View Categories
```bash
GET '/categories'
```
- this endpoint return json object having id's and their corrospoinding catergory name's

- Resquested arguements None
- method of request "GET"
- Return json object having categories.key value pairs format


Example  ``` curl http://localhost:5000/categories```
``` bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```


### View Questions
Endpoint ```GET '/questions```

- Return a json object having following keys:

  -- categories: A list of category objects, where each object contains a dictionary with the keys id and type.

  --questions: A list of questions objects, where each object contains a dictionary with the keys question, answer, category,         difficulty.
  -- total questions: An integer representing the total number of questions in the database.

  -- current category: This defaults to 'all' for this route.
  
-Request Arguments:

  -- page: An integer that represents the requested page. It is optional and defaults to 1.
  -- max: An integer that represents the maximum number of questions per page. It is optional and defaults to 10.
  
  - endpoint to request response
  
  ```curl http://localhost:5000/questions?page=1```
  
 ```bash
 {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Null", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
 
 ```
 
 ### Delete Question
 Endpoint ```DELETE /questions/id```
 
 - Delete specific question using its id which is unique to every question we enter.
 - Return response object having two keys success(true) and deleted question(id)
 - if request is unsuccessfull return error (404)
 
 ```bash
 curl -X DELETE http://localhost:5000/questions/5
 
 #gives output
 
{
  "deleted": 5, 
  "success": true
}
```

- If we again try to delete same question.

``` bash
curl -X DELETE http://localhost:5000/questions/5

#return output as below

{
  "error": 400, 
  "message": "bad request", 
  "success": false
}
```
### View Questions by category

the requested endpoint using CURL

``` curl http://localhost:5000/categories/1/questions```

- Return object contains

  -- Requested category id
  
  -- List of questions under that category which are represented in object format and each object has qustion , category          answer,difficulty  ,id
  
  -- Total questions containing in the database of that category
  
  -- succuss True
  
 ```  
  curl http://localhost:5000/categories/2/questions
  ```
  
  ```
{
  "current_category": "2", 
  "questions": 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
 ```
 
 ### Add a Question
 - Adding questions takes 4 mandatery arguements 'question','category','answer','difficulty'. If any of there not present error will be displayed
 
 - Response object contain id of question added and success "true"
 
 ``` bash 
 curl -X POST 'http://localhost:5000/questions' -d '{"\""question"\"": "\""Who is father of cricket?"\"", "\""answer"\"": "\""Sachin Tendulkar"\"", "\""category"\"": 5, "\""difficulty"\"": 5}' -H 'Content-Type: application/json'
 
 ```
 
 ```
 Request:
 {
 "question":"who is father of cricket",
 "answer":"Sachin Tendulkar",
 "category:6,
 "difficulty":5
 }
 ```
 
 ```
 Response
 {
 {
  "data": {
    "answer": "sachin tendulkar",
    "category": 6,
    "difficulty": 5,
    "id": 23,
    "question": "who is father of cricekt"
  },
  "success": true
}

 }
 ```
 
 ### Search Question based on search term
 
- This endpoint performs a case insensitive search based on a provided search term.

- It returns a json object with the following keys:

- current_category: defaults to null

- questions: A list of questions objects, where each object contains a dictionary with the keys question, answer, category, difficulty.

- total_questions: total number of questions found containing the search term


```bash
curl -X POST 'http://localhost:5000/questions' -d '{"\""searchTerm"\"": "\""cricekt"\""}' -H 'Content-Type: application/json'

```


```
Response
{
  "current_category": null,
  "questions": [
    {
      "answer": "Sachin tendulkar",
      "category": 6,
      "difficulty": 5,
      "id": 25,
      "question": "who is father of cricket"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### Error handling

- Occuring errors are returned as json objects with the following format.
- The API can return the following errors:
  - 400 Bad Request
  - 404 Not Found
  - 422 Unprocessable Entity
  - 500 Internal Server Error
  
  
#### Error (400)

  ```
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success':False,
      'error':400,
      'message':'bad request'
      })
```

#### Error(404)

```
@app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'messge':"resource not found"
      })
      
 ```
 
 #### Error(405)
 
 ```
   @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success':False,
      'error':405,
      'messge':"method not allowed"
      })
  ```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
