import mariadb
import dbcreds
import traceback
from post import Post

# dBeaver Starting PROCESSLIST id = 224

# Function to get the users selection
# ? continues in elif blocks to go back into the loop
#! unsure if it makes sense to have a function to set the username, then call it to a variable here, more code, feels more clean.
# ? changed quit functiuonality to send you back to login rathe than running the quit function, so that the connection remains open and can re login.


def getUserSelection(user):
  # user = getUserName()
  while True:
    try:
      print("Options: \n 1: Write a post \n 2: See all posts \n 3: Quit")
      user_selection = int(input(f"{user}, Make a selection: "))
      if (user_selection == 3):
        break
      elif (user_selection == 1):
        createPost(user, input(
            f"Hey {user}, enter your post content: "))
        continue
      elif (user_selection == 2):
        getAllPosts()
        continue
      elif (user_selection > 3 or user_selection <= 0):
        print("Enter 1, 2 or 3")
        continue
      break
    except ValueError:
      print("You must enter a number")
    except:
      traceback.print_exc()
  return user_selection


# Function to get username
# ? this was for the original assignment, not used after bonus!
# def getUserName():
#   while True:
#     try:
#       user = input('Welcome, please enter a username: ')
#       return user
#     except:
#       print('Error with username!')
#       traceback.print_exc()

# login function, Loops, fair amount of error elifs, should catch most cases?
# ? you will get multiple error prints from the error catching elif's! one for every user in the database, not ideal, but works!
def login():
  while True:
    try:
      print("Please login to see options!")
      print("Options: \n 1: Login \n 2: Quit")
      selection = int(input("Make a selection: "))

      if(selection == 1):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        cursor.execute("SELECT * FROM user")
        all_users = cursor.fetchall()
        for user in all_users:
          if (username == user[0] and password == user[1]):
            print(f"Welcome {user[0]}, You have logged in!")
            getUserSelection(username)
          elif (username == user[0] and password != user[1]):
            print(
                f"Sorry {username}, You have entered the wrong password!")
            continue
          elif (username != user[0]):
            print("Invalid username!")
            continue
          elif (username != user[0] or password != user[1]):
            print("invalid user information")
            continue
      elif (selection == 2):
        quit()
        break
      elif (selection > 2 or selection <= 0):
        print("Please enter a valid option!")
    except ValueError:
      print("You must enter a number")
    except:
      print("Error with seleciton!")
      traceback.print_exc()


# create post function, seems to worl well, #? uses Post Class
#! Should createPost be in Post class? Will think about this, since it is a "function" of a post...  kinda
def createPost(username, content):
  try:
    Post(username, content)
    cursor.execute(
        f"INSERT INTO blog_post (username, content) VALUES ('{username}', '{content}')"
    )
    conn.commit()
    print("Post Created")
  except:
    print("Unknown error creating post!")
    traceback.print_exc()


def getAllPosts():
  try:
    cursor.execute("SELECT * FROM blog_post")
    posts = cursor.fetchall()
    for post in posts:
      print(f"\n User: {post[0]} ---------- Post ID: {post[2]}")
      print(post[1])
      print("---------------------------------------")
    # print(posts)
  except:
    print("Unknown error getting posts")
    traceback.print_exc()


# Function to quit app, closes cursor and connection
def quit():
  try:
    cursor.close()
    print("Cursor Closed")
  except:
    print("Error closing cursor")
    traceback.print_exc()

  try:
    conn.close()
    print("Connection Closed!")
  except:
    print("Error closing connection")
    traceback.print_exc()


try:
  conn = mariadb.connect(
      user=dbcreds.user,
      password=dbcreds.password,
      host=dbcreds.host,
      port=dbcreds.port,
      database=dbcreds.database,
  )
  print("Connected!")
except:
  print("Error connecting to database!")
  traceback.print_exc()

cursor = conn.cursor()

login()
