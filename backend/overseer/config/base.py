import os


DB_NAME = os.getenv('DB_NAME', 'test_db')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')

MODELS = [
    'overseer.db.users.User',
]
