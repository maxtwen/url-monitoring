Tested under docker v17 configuration

usage:

    docker-compose -f ./docker-compose.yml -f ./app/docker-compose.yml -f ./db/docker-compose.yml -f ./worker/docker-compose.yml -f ./reporter/docker-compose.yml up -d


App RESTful api:

    Add worker/reporter task:
    
        curl -H "Content-Type: application/json" -X POST -d '{"url": "ya.ru", "interval": 5, "is_active": true}' http://localhost:5002/api/v1/(worker|reporter)_task/
        
    Get all worker/reporter tasks
    
        curl -X GET http://localhost:5002/api/v1/(worker|reporter)_task/
        
    Patch worker/reporter task
    
        curl -H "Content-Type: application/json" -X PATCH -d '{"params": {""url": "ya.ru", "interval": 5}, "is_active": true}' http://localhost:5002/api/v1/(worker|reporter)_task/task_id/

