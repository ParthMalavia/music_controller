# Music Controller


## Installation steps

### Install Django app requirements

1. Create an python environment 

     - ```python -m venv venv```

2. Activate the environment

    - For windows: ```venv\Scripts\activate```

    - For Linux: ```. venv/bin/activate```

3. Install dependencies: ```pip install -r requirement.txt```


### Install React app dependencies

1. Move to 'frontend' directory

2. Install react app dependencies: ```npm i```


## Run backend and frontend server

1. Run backend server (From base directory): ```python manage.py runserver```

2. Run frontend server (Move to 'frontend' directory): ```npm start``` 

### Note

- Django app will be running on port 8000 of local server

- React App will be running on port 3000 of local server

Open the http://localhost:3000/ or http://127.0.0.1:3000/ to use the music controller app