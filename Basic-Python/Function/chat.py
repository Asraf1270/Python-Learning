# Basic-Python/Function/chat.py
# define a function to greet the user by name
def helloName(name):
    return "Wow, nice name " + name + "!"

# define a function to greet the user by age
def helloAge(age):
    if(age < 13):
        return "Ohh, you are a child!"
    elif(age <= 20):
        return "You are a teenager!"
    elif(age <= 40):
        return "You are a young adult!"
    elif(age < 60):
        return "You are an adult!"
    else:
        return "You are a senior!"

# Bye the user
def byeUser(name):
    return "Bye, " + name + "! Take care"

# main program
# helloName
print ("Hi, How are you?")
name = input("What's your name? \n")
print(helloName(name))

# helloAge
age = input("How old are you? \n")
print(helloAge(int(age)))

# byeUser
print(byeUser(name))
