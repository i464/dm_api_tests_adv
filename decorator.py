def decorator(func):
    def wrapper(name,*args, **kwargs):
        print('............')
        func(name,*args, **kwargs)
        print('............')
        return
    return wrapper

@decorator
def my_print(name):
    print(f'Hello,{name}')

@decorator
def my_print1(name):
    print(f'Hello,{name}')

@decorator
def my_print2(name):
    print(f'Hello,{name}')


my_print(name='All')
my_print1(name='Mam')
my_print2(name='Dad')

