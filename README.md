# Myriad API 

## Guidelines
#### Myriad Standards 
* Python3
* PEP8
* UnitTests using pytest module
* linting using pylint module
* type hints using Typing module

#### Deployment     
Current stack    
* apache2  
* mod_wsgi  

Looking to go with   
* nginx  
* gunicorn  

---

## Structure Guide
* routes/   
    Includes all the routes attached to the API
    * vendor routes
    * dashboard routes
    * onboard routes
    * script routes

* services/  
    Includes all the utility services consumable by the overall API components  
    * email
    * scheduling
    * monitoring

* creds/  
    Stores the credentials we use from within this API  
    * db connection creds
    * API keys
        
* models/  
    Model classes for the API  
    * rds class
    * dynamo class
    * s3 class

* templates/  
    Templates for our website
    
* assets/  
    Static files 
        
* myriad.wsgi  
    flask project endpoint 