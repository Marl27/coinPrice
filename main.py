from sql_alchemy_dir.push_to_db import populate_coin_data
import time
start_time = time.time()
populate_coin_data()

populate_coin_data_end_time = time.time()
time_taken_to_populate = populate_coin_data_end_time - start_time

#ttm_squeeze

from strategies import ttm_squeeze

end_time = time.time()
total_time = end_time - start_time

line_1 = f'start_time - {time.ctime(start_time)} \n'
line_2 = f'end_time - {time.ctime(end_time)} \n'
line_3 = f'time_taken_to_populate_table - {time_taken_to_populate/60} \n'
line_4 = f'time_to_run_ttm_squeeze - {str(total_time/60 - time_taken_to_populate/60)} \n'
line_5 = f'total_time - {str(total_time/60)} \n'
with open('logging.txt', 'a') as f:
    f.writelines('**********************\n')
    f.writelines(line_1)
    f.writelines(line_2)
    f.writelines(line_3)
    f.writelines(line_4)
    f.writelines(line_5)
