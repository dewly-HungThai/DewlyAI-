import time 
import random

#Timer Decorator
def timer(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"'{func.__name__}' took: {execution_time:.4f}s to run") 
        return result
    return wrap

#Retry Decorator
def retry(n_retries=3, delay=1, exception = [ValueError]):
    def func(f):
        def wrapper(*args, **kwargs):
            current_retry = 0
            while current_retry < n_retries:
                try:
                    return f(*args, **kwargs)
                except tuple(exception):
                    current_retry += 1
                    print(f"{f.__name__} failed ({current_retry}), retrying...")
                    time.sleep(delay)
            raise Exception("Max retries exceeded")
        return wrapper
    return func

#Tesing Decorator
@timer
@retry(n_retries = 10, delay = 1, exception = [ValueError])
def test_retry():
    random_value = random.choice(range(0,8))
    if random_value == 1:
        print('pass')
    else:
        raise ValueError("Fail")


#Fibonacci Generator
def fibonacci(n):
    a = 0
    b = 1
    count = 0
    if n == 0:
        raise ValueError("Invalid Input")
    if n ==1 or n == 2:
        return 1
    else:
        for i in range(0,n,1):
            if i == 0:
                print(0)
                continue
            temp = b
            b = a+b
            a= temp
            yield b 
            
#Read line by line Generator
def readline(file_path):
    with open(file_path) as f:
        for i in f:
            yield i.strip()

if __name__ == "__main__":
    print("="*50)
    print("Test Decorator\n")
    test_retry()
    print("="*50+"\n")
    
    
    print("="*50)
    print("Test Fibonacci Generator\n")
    for i in fibonacci(9):
        print(i)
    print("="*50+"\n")
    
    print("="*50)
    print("Test Read lines Generator\n")
    for i in readline('test.txt'):
        print(i)
    print("="*50+"\n")
    