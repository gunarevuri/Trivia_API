# Full Stack API Final Project

#### Database : Postgresql

#### Frontend : React

#### Backend  : Flask

#### API keys : Not needed

#### Authentication : not implemented

### Overview


This project is a flask framework based application, which includes two models(Tables)  Questions and Categories having a One-to-one relationship between those two models. Each model had different Endpoints includes GET, POST, PATCH, DELETE, search pattern also implemented to search for a specific question. We can get questions for each category by clicking that endpoint.API keys and  Authentication were not implemented in this project. We can use either Curl or postman to test endpoints and can check those responses. Error-handling methods also implemented for each endpoint. 

Go through README.md file in /backend directory to get full documentation about API implementation and endpoint testing.

To test this application first clone the project using url in the terminal.


```
git clone https://github.com/gunarevuri/Trivia_API.git
```

make sure you are using vertual environment for the project. To enable vertual environment copy these commnads if you are using mac

```
cd  /project_directory

python3 -m venv env

source env/bin/activate

```


After cloning make sure you have to run backend before running frontend.

```
cd frontend

npm i 

(or)

npm install
 
```

then npm will take care of all the required packages to run application.After installing required package run below command

```
npm start

```

After you runnin bash npm start react automatically loads all required packages from package.json file.Automatically you redicted to http://localhost:3000 url.

Then open another tab in terminal and go to backend directory and make sure you have enabled vertual environment.

Go to README.md file in backend directory and which had detailed information how to start flask application.




