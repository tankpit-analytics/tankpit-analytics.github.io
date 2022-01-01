from get_all_tanks import *

#----- main

if __name__ == '__main__':
    print('#####')
    print(time_now)
    start_time = time.time()
    y2022_tanks = get_all_tanks(ranks_dict_2022, '2022')
    y2022_tanks['time_now'] = time_now
    y2022_tanks.to_csv(y2022_tanks_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
