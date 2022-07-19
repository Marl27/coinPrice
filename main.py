from sql_alchemy_dir.push_to_db import populate_coin_data
from strategies.ttm_squeeze import get_coin_data_from_table
import time
start_time = time.time()

###########################
populate_coin_data()
###########################

populate_coin_data_end_time = time.time()
time_taken_to_populate = populate_coin_data_end_time - start_time

line_1 = f'start_time - {time.ctime(start_time)} \n'
line_2 = f'time_taken_to_populate_table - {time_taken_to_populate/60} \n'

###########################
#ttm_squeeze
line_3 = f'get_coin_data_from_table - {get_coin_data_from_table()}\n'
###########################

end_time = time.time()
total_time = end_time - start_time

line_4 = f'end_time - {time.ctime(end_time)} \n'
line_5 = f'time_to_run_ttm_squeeze - {str(total_time/60 - time_taken_to_populate/60)} \n'
line_6 = f'total_time - {str(total_time/60)} \n'
with open('logging.txt', 'a') as f:
    f.writelines('**********************\n')
    f.writelines(line_1)
    f.writelines(line_2)
    f.writelines(line_3)
    f.writelines(line_4)
    f.writelines(line_5)
    f.writelines(line_6)
