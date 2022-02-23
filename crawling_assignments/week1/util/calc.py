from timeit import time

def calc_time(func):
    def wrap_func(*args, **kwargs):
        start_time = time.time()
        val = func(*args, **kwargs)
        end_time = time.time()
        print('\n-------------')
        print('Function Name:', func.__name__)
        print('Response Time: %fs' % (end_time - start_time))
        print('-------------')
        return val
    return wrap_func