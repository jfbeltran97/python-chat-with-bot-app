# Django Chat App + Stock Bot

This is a Django based web application developed with some helper libraries like Django channels. There's some minimum set up to be done but you should be able to get it up and working with no major issues.

## Steps

 1. `git clone https://github.com/jfbeltran97/python-chat-with-bot-app.git`

 2. `python3 -m venv env`
 3. `source env/bin/activate` -> activates virtual environment
 4. `pip install -r requirements.txt`

 5. Now you need to open another terminal, [install docker](https://docs.docker.com/engine/install/ubuntu/) and run the RabbitMQ community image in port 5678 (or just copy the command below after installing docker):
`docker run -it --rm --name rabbitmq -p 5678:5672 -p 15672:15672 rabbitmq:3-management` 

 6. Once RabbitMQ is running, make sure to have another terminal with the activated virtual environment (step 3). Go to the `stockbot` directory
 7. Run `python main.py`
 8. Now get another terminal with the activated virtual environment. Go to the `chatroom` directory and run the migrations: `python manage.py migrate`
 9. Run `python manage.py chat_initial_setup`. 2 users, and a chatroom are going to be generated. Check credentials.
 10. Run server `python manage.py runserver`
 11. Go to a web browser and enter: `localhost:8000/admin`. Login with the credentials of step 9. 
 12. Create two users for testing. Go to Users -> Add user (top right corner). Fill the information.
 13. That's it. Go to the login page in two different browsers to authenticate with the two users created. `localhost:8000/login`
 14. Have fun. 
