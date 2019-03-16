## PhoneBook
Example of REST API based as example of PhoneBook.

#### How to run the code
You may build from source
```
git clone https://github.com/lzalewsk/phonebook.git
cd phonebook
docker build --rm -t lzalewsk/phonebook .
```
or use image from Docker Hub
```
docker run -itd --name phonebook \
    -e PHONEBOOK_USER=<auth_user> \
    -e PHONEBOOK_PASS=<auth_password> \
    -e PHONEBOOK_TOKEN=<token> \
    -p 5000:5000 \
    lzalewsk/phonebook
```

#### API usage by example

Create new entities(contact informatin) by
POST  
one entity
```
curl -d '{"username": "user1", "phone": "+48123456001", "email": "lu01@example.com"}' \
    -H 'Content-Type: application/json' \
    -H 'X-PhoneBook-Token: <token>' \
    -X POST http://127.0.0.1:5000/api/v1/contacts
```
or multiple entities data
```
curl -d '[{"username": "user6", "phone": "+48123456006", "email": "lu06@example.com"},
          {"username": "user7", "phone": "+48123456007", "email": "lu07@example.com"},
          {"username": "user8", "phone": "+48123456008", "email": "lu08@example.com"}]' \
     -H 'Content-Type: application/json' \
     -H 'X-PhoneBook-Token: <token>' \
     -X POST http://127.0.0.1:5000/api/v1/contacts
```
or using PUT with new <id>
```
curl -d '{"username": "user99", "phone": "+48123456099", "email": "lu99@example.com"}' \
        -H 'Content-Type: application/json' \
        -H 'X-PhoneBook-Token: <token>' \
        -X PUT http://127.0.0.1:5000/api/v1/contacts/<id>
```

GET  
all data
```
curl -H 'Content-Type: application/json' \
     -H 'X-PhoneBook-Token: <token>' \
     -X GET http://127.0.0.1:5000/api/v1/contacts
```
or with <id>
```
curl -H 'Content-Type: application/json' \
     -H 'X-PhoneBook-Token: <token>' \
     -X GET http://127.0.0.1:5000/api/v1/contacts/<id>
```

DELETE
particular <id>
```
curl -H 'Content-Type: application/json' \
     -H 'X-PhoneBook-Token: <token>' \
     -X DELETE http://127.0.0.1:5000/api/v1/contacts/<id>
```

Update operations by    
PUT  
particular <id>
```
curl -d '{"username": "user1", "phone": "+48123456001", "email": "lu01@example.com"}' \
     -H 'Content-Type: application/json' \
     -H 'X-PhoneBook-Token: <token>' \
     -X PUT http://127.0.0.1:5000/api/v1/contacts/<id>
```
or using PATCH
```
curl -d '{"phone": "+48000000000"}' \
     -H 'Content-Type: application/json' \
     -H 'X-PhoneBook-Token: <token>' \
     -X PATCH http://127.0.0.1:5000/api/v1/contacts/<id>
```