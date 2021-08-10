from ramajudicial import verify_process, start_session, end_session
from processparser import read_processes
from gmail import send_email
import traceback

if __name__ == '__main__':
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
            traceback.print_exc()
    end_session()
    send_email(active_processes, failed_processes)
