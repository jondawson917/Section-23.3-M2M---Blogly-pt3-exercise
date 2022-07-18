"""Seed file to make sample data for db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Drop existing Tables
db.drop_all()
# Create all tables
db.create_all()

u1 = User(first_name="Ronald", last_name = "Reagan", image_url="https://as1.ftcdn.net/v2/jpg/00/64/67/52/1000_F_64675209_7ve2XQANuzuHjMZXP3aIYIpsDKEbF5dD.jpg")
u2 = User(first_name="George", last_name = "Bush Sr.", image_url="https://as2.ftcdn.net/v2/jpg/02/71/67/33/1000_F_271673320_eI9mFEvtrjNNPW5AxGWbLpxu8s2rLUoq.jpg")
u3 = User(first_name="Bill", last_name = "Clinton", image_url="https://bestprofilepictures.com/wp-content/uploads/2021/05/Broly-Profile-Picture.jpg")
u4 = User(first_name="George", last_name = "Bush Jr.", image_url="https://as2.ftcdn.net/v2/jpg/01/98/79/33/1000_F_198793380_80mniUCcA53NlJNRu8xQwrT5JVdKnKjm.jpg")
u5 = User(first_name="Barack", last_name = "Obama", image_url="https://st.depositphotos.com/2101611/3925/v/950/depositphotos_39258143-stock-illustration-businessman-avatar-profile-picture.jpg")

#Make a bunch of tags
t1 = Tag(name="freestyle")

t2 = Tag(name="bloop")

t3 = Tag(name="womanCrushWednesday")

# Make a bunch of Posts
p1 = Post(title="What are you thinking", content="Pensive thoughts are built with lorem", user_id='1')

p2 = Post(title="What are you doing", content="Idle hands don't complete work", user_id='2')

p3 = Post(title="How to change a car tire", content="Step 1 park the car. Step 2 Jack up the car halfway. Step 3 Loosen nuts on tire until the tire is off of the car", user_id='3')

p4 = Post(title="Wise words of a magician.", content="Excellent guess, kreskin. Wrong! But, excellent.", user_id='4')

p5 = Post(title="Sounds like Billy Joel", content="Can you control everything in your life? No! Think about the song 'I'm just waiting...waiting for the world to change'", user_id='5')

p6 = Post(title="Miss South Carolina", content="I personally believe that the reason some Americans can't find the United States on a map is because some people out there don't have maps. And we need to help the Middle Eastern countries, South Africa, and Asian people such as.", user_id='5')

p7 = Post(title="Mr. Spock", content="The needs of the many outweigh the needs of the few. It's only...logical.", user_id='3')




db.session.rollback()
db.session.add_all([u1, u2, u3, u4, u5, p1, p2, p3, t1, t2, t3])



db.session.commit()


