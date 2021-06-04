import mariadb
import dbcreds
import traceback
from post import Post
# dBeaver Starting PROCESSLIST id = 224

initial_options = [
  {'number': 1, 'option': "Write a post"},
  {'number': 2, 'option': "See all posts"},
  {'number': 3, 'option': "Quit"},
]

# Function to get the users selection 
#! unsure if it makes sense to have a function to set the username, then call it to a variable here, more code, feels more clean.
def getUserSelection():
  while True:
    try:
      user = getUserName()
      print('Options: \n 1: Write a post \n 2: See all posts \n 3: Quit')
      user_selection = int(input(f'{user}, Make a selection: '))
      if(user_selection == 3):
        quit()
      elif(user_selection == 1):
        createPost(user, input(f'Hey {user}, enter your post content: '))
      elif(user_selection > 3 or user_selection <= 0):
        print('Enter 1, 2 or 3')
        continue
      break 
    except ValueError:
      print('You must enter a number')
    except: 
      traceback.print_exc()
  return user_selection

# Function to get username 
def getUserName():
  try:
    user = input('Welcome, please enter a username: ')
    return user
  except:
    print('Error with username!')
    traceback.print_exc()

# create post function, seems to worl well, #? uses Post Class 
#! Should createPost be in Post class? Will think about this, since it is a "function" of a post...  kinda
def createPost(username, content):
  try:
    Post(username, content)
    cursor.execute(f"INSERT INTO blog_post (username, content) VALUES ('{username}', '{content}')")
    conn.commit()
    print('Post Created')
  except:
    print('Unknown error creating post!')
    traceback.print_exc()

# Function to quit app
def quit():
  try:
    print('Quitting app')
    return
  except:
    print('Error quitting app')

try:
  conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
  print('Connected!')
except:
  print('Error connecting to database!')
  traceback.print_exc()

cursor = conn.cursor()

getUserSelection()

try:
  cursor.close()
except:
  print('Error closing cursor')
  traceback.print_exc()

try:
  conn.close()
  print('Connection Closed!')
except:
  print('Error closing connection')
  traceback.print_exc()