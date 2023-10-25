# Assigning Functions to Variables

# def plus_one(number):
#     return number + 1

# add_one = plus_one
# add_one(2)
# print(add_one(2))


# Defining Functions Inside other Functions 
# def plus_one(number):
#     def add_one(number): 
#         return number + 1
#     result = add_one(number)
#     return result

# print(plus_one(3))   


# Passing Functions as Arguments to other Functions

# def plus_one(number):
#     return number + 1

# def function_call(function):
#     number_to_add = 5
#     return function(number_to_add)

# function_call(plus_one)

# Functions Returning other Functions

# def say_hii():
#     return "HII"

# def hello_function(function):
#     return function()

# print(hello_function(say_hii))

# Nested Functions have access to the Enclosing Function's Variable Scope

# def print_message(message):
#     "Function enclosing"
#     def message_sender():
#         "Nested function"
#         print(message)
    
#     message_sender()

# print_message("Some random message")

# Creating Decorators
# def uppercase_decorater(function):
#     def wrapper():
#         func = function()
#         make_uppercase = func.upper()
#         return make_uppercase
#     return wrapper


# def say_hii():
#     return 'hello_there'

# decorate = uppercase_decorater(say_hii)
# print(decorate())

# Creating Decorators in simple way.
# @uppercase_decorater
# def say_hii():
#     return 'hello_there'
# print(say_hii())


# def split_string(function):
#     def wrapper():
#         func = function()
#         splitted_string = func.split()
#         return splitted_string
#     return wrapper

# @split_string
# @uppercase_decorater
# def say_hii():
#     return 'hello there'
# print(say_hii())

# Accepting Arguments in Decorator Functions
# def decorater_with_arguments(function):
#     def wrapper_accepting_arguments(arg1, arg2):
#         print("My arguments are: {0}, {1}".format(arg1, arg2))
#         function(arg1, arg2)
#     return wrapper_accepting_arguments

# @decorater_with_arguments
# def cities(city_one, city_two):
#     print("Cities I love are {0} and {1}".format(city_one, city_two))

# print(cities("Sikar", "Jaipur"))

# Iterators & Generators.
# string = "GFG"
# ch_iterator = iter(string)

# print(next(ch_iterator))
# print(ch_iterator)
# print(ch_iterator)

class Birds:

    def intro(self): 
        print('There are many type of birds.')

    def flight(self): 
        print('Most of the birds can fly but some cannot.')

class sparrow(Birds):
    def flight(self): 
        print('sparrow can fly.')

class ostrich(Birds):
    def flight(self): 
        print('Ostrich cannot fly.')

obj_bird = Birds()
obj_sparrow = sparrow()
obj_ostrich = ostrich()

obj_bird.intro()
obj_bird.flight()

obj_sparrow.intro()
obj_sparrow.flight()

obj_ostrich.intro()
obj_ostrich.flight()

