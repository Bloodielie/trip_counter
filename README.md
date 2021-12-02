# Bot for controlling trips

## Install  
```
clone this repo
pip install requirements.txt
```
## Usage  
Create a .env file like .env.example file.  
Run migrations:
```
alembic upgrade head
```

Start bot:
```
python -m bot
```

## Database structure  
![database structure](db_image.png)