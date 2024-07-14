import asyncio
import time
import inspect
import random
import string


config = {'start': False}

data = {

}

# data = {
#     'function': {
#         'current_tasks': {
#             'task_id': {
#                 'start_time': 1488,
#                 'slow_time': 1488
#             }
#         },
#         'last_times': [
#             [1488, 1488],
#             [1488, 1488]
#         ]
#     }
# }

def start(basic_slow: float, temperature = 1.0, switch = True, max_calculating_units = 200, calculating_units_livetime = 180):
    global config
    config = {
        'start': True,
        'temperature': temperature,
        'basic_slow': basic_slow,
        'switch': switch,
        'max_calculating_units': max_calculating_units,
        'calculating_units_livetime': calculating_units_livetime
    }

async def initialize_data(func_name):
    global data
    if func_name not in data:
        data[func_name] = {
            'current_tasks': {},
            'last_times': []
        }


async def _time_control(func):
    global data
    last = data[func]['last_times']
    for i in range(len(last) - 1, -1):
        if last[i][1] < time.time() - config['calculating_units_livetime']:
            del last[i]
    data[func]['last_times'] = last


async def _get_average(func):
    average = 0
    await _time_control(func)
    last = data[func]['last_times']
    if len(last) != 0:
        for i in last:
            average += i[0]
        return average / len(last)
    return average

async def _get_task_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def get_task_id(length=32):
    stack = inspect.stack()
    await initialize_data(str(stack[2].function))
    while True:
        task_id = await _get_task_id(length)
        if task_id not in data[str(stack[2].function)]['current_tasks']:
            data[str(stack[2].function)]['current_tasks'][task_id] = {
                'start_time': 0,
                'slow_time': 0
            }
            return task_id


async def calculate_slow(ignore=False, temperature=1.0):
    stack = inspect.stack()
    func = str(stack[2].function)
    task_id = await get_task_id()
    global data
    if ignore:
        data[func]['current_tasks'][task_id]['slow_time'] = 0
        data[func]['current_tasks'][task_id]['start_time'] = time.time()
        return [0.0, task_id]
    else:
        average = await _get_average(func)
        slow = average * temperature * config['temperature']
        if slow < config['basic_slow']:
            slow = config['basic_slow']
        data[func]['current_tasks'][task_id]['slow_time'] = slow
        data[func]['current_tasks'][task_id]['start_time'] = time.time()
        return [slow, task_id]


async def hui(svo):
    global data
    task_id = svo[1]
    stack = inspect.stack()
    func = str(stack[2].function)
    last_time = time.time() - data[func]['current_tasks'][task_id]['start_time'] + data[func]['current_tasks'][task_id]['slow_time']
    del (data[func]['current_tasks'][task_id])
    data[func]['last_times'].append([last_time, time.time()])
    if len(data[func]['last_times']) >= config['max_calculating_units']:
        del (data[func]['last_times'][0])

