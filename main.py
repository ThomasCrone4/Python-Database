from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from create_schema import User

engine = create_engine('sqlite:///ecommerce.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Update a user's email
def update_user_email(user_id, new_email):
    # Query the user by user_id
    user = session.query(User).filter(User.user_id == user_id).first()
    
    if user:
        # Update the email
        user.email = new_email
        # Commit the changes
        session.commit()
        print(f"User {user_id}'s email has been updated to {new_email}")
    else:
        print(f"User with id {user_id} not found")

def remove_user(user_id):
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"User {user_id} has been removed")
        else:
            print(f"User with id {user_id} not found")
    except Exception as e:
        print(f"Error removing user {user_id}: {e}")
        session.rollback()

# Update the email of user with id 1
update_user_email(1, 'email@123.com')

# Add a new user
new_user = User(username='stev_doe', email= "stve@example.com", password='securepassword')  
session.add(new_user)
try:
    session.commit()
    print("New user added successfully")
except IntegrityError as e:
    session.rollback()
    print("Error: {e.orig}. A user with this username or email already exists")

new_user_1 = User(username='tm_doe', email='tm@example.com', password='securepassword')
session.add(new_user_1)
try:
    session.commit()
    print("New user added successfully")
except IntegrityError as e:
    session.rollback()
    print("Error: {e.orig}. A user with this username or email already exists")

remove_user(5)
remove_user(6)


# Verify the user was added
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM users"))
    for row in result:
        print(row)