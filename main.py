from ramajudicial import verify_process, start_session, end_session
from processparser import read_processes
from gmail import send_email

import traceback
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    processes = read_processes('processes.xlsx')
    start_session()
    failed_processes = []
    active_processes = []
    for process in processes:
        process_id = process['id']
        try:
            if verify_process(process_id, process['city'], process['entity']):
                active_processes.append(process_id)
        except:
            failed_processes.append(process_id)
            logging.exception('Error processing process {id}'.format(id=process_id))
    end_session()
    logging.info('Active processes: {p}'.format(p=active_processes))
    logging.info('Failed processes: {p}'.format(p=failed_processes))
    send_email(active_processes, failed_processes)
