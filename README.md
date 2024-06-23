# B2Broker-test-task

### Start the project
#### 1. Clone the repo
    git clone https://github.com/Olim2508/b2broker-test-task
#### 2. Build and run with docker-compose
    docker-compose up -d --build

#### Project will run on [http://localhost:8000](http://localhost:8000)

### What is done
1. REST APIs for: Transaction and Wallet models with business logic implemented as in task description
2. Sorting, Filtering, Pagination: Supported
3. Linter Usage: Flake8, Black, Isort
4. Test Coverage: Provided
5. Swagger API documentation: Integrated

### Additional
* Command to run tests - ```docker-compose exec backend python manage.py test```
* Access to admin panel and swagger with creds after start up: Email - ```admin@gmail.com```, password - ```admin```