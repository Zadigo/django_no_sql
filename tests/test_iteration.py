"""Main module for testing the iterator iteration loop
and base core functionnalities that it uses
"""

import multiprocessing
import queue
import threading
from collections import OrderedDict

import pandas

import timeit

QUERY = [
    {'id': 1, 'name': 'Kendall'}, 
    {'id': 2, 'name': 'Kylie'}, 
    {'id': 3, 'name': 'Hailey'},
    {'id': 4, 'name': 'Aurélie'},
    {'id': 5, 'name': 'Marie'},
    {'id': 7, 'name': 'Pierrette'},
    {'id': 8, 'name': 'Carine'},
    {'id': 9, 'name': 'Lucile'},
    {'id': 10, 'name': 'Corinne'},
]

KEYS_DICT = ['id', 'name']

SEARCHED_VALUES = [1, 'Kendall']


# SERIAL PROCESSING

start1 = timeit.default_timer()

def iterator1():
    for item in QUERY:
        truth_array = []
        for index, key in enumerate(KEYS_DICT):
            searched_value = SEARCHED_VALUES[index]

            if item[key] == searched_value:
                truth_array.append(True)
            else:
                truth_array.append(False)
            
        if all(truth_array):
            print('Matched', item)

iterator1()

print('Finished in:', round(timeit.default_timer() - start1, 4))

# MULTI PROCESSING

# queue = queue.Queue()

# def iterator2(item, result, keys_dict, searched_values):
#     print(item)
#     truth_array = []
#     for index, key in enumerate(keys_dict):
#         searched_value = searched_values[index]

#         if item[key] == searched_value:
#             truth_array.append(True)
#         else:
#             truth_array.append(False)

#     if all(truth_array):
#         result.put(item)

# processes = [multiprocessing.Process(target=iterator2, args=[item, queue, KEYS_DICT, SEARCHED_VALUES]) for item in QUERY]    
# for process in processes:
#     process.start()
#     process.join()

# print(queue.empty())


# THREADING

start2 = timeit.default_timer()

def threading_queryset():
    results = queue.Queue()
    def iterator2(item, result, keys_dict, searched_values, index=None):
        truth_array = []
        for index, key in enumerate(keys_dict):
            searched_value = searched_values[index]

            if item[key] == searched_value:
                truth_array.append(True)
            else:
                truth_array.append(False)

        if all(truth_array):
            result.put(item)


    threads = [
        threading.Thread(
            target=iterator2, 
            args=[item, results, KEYS_DICT, SEARCHED_VALUES],
            kwargs={'index': i}
        ) 
        for i, item in enumerate(QUERY)
    ]
    for thread in threads:
        thread.start()
        if thread.is_alive():
            thread.join()

    for _ in threads:
        try:
            print(results.get_nowait())
        except:
            pass

threading_queryset()

print('Finished in:', round(timeit.default_timer() - start2, 4))
