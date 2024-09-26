import config


def check_resource_usage():
    if config['resource_monitoring']:
        import psutil
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        log_entry = f"Resource Usage - CPU: {cpu_usage}% Memory: {memory_info.percent}%"
        write_log_entry(log_entry)

def is_app_allowed():
    if not config['application_filter']:
        return True
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() in [app.lower() for app in config['application_filter']]:
                return True
    except ImportError:
        pass
    return False

def write_log_entry(entry):
    with open(config['log_file_path'], 'a') as log_file:
        log_file.write(entry + '\n')
