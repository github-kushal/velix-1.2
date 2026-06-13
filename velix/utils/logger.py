import logging 
import os



logs = "D:\\Velix-1.2\\logs"

if os.path.exists(logs):
    pass
else:
    os.mkdir("logs")


log = logging.getLogger("VELIX")

log.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "============================ \n [%(asctime)s] \n  %(levelname)s \n  %(name)s \n  %(message)s \n ============================ "
)

"""
    Logs a message with INFO level.
    Modules: 
        Startup -> system.log
        Assistant -> system.log
        Router -> debug.log
        Brain -> debug.log and error.log
        Memory -> memory.log
        Executor -> execution.log
        Speaker -> debug.log
        Listener -> debug.log
        User Interaction -> conversation.log
        Exception -> error.log

"""


def file_handler(file_path): 
    file_handler = logging.FileHandler(file_path, mode="a")
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

def log_info(module, message):
    file_handler("logs\\system.log")
    log.info(f"[{module}] : [{message}]")

def log_debug(module, message):
    file_handler("logs\\debug.log")
    log.debug(f"[{module}] : [{message}]")

def log_error(module, error):
    file_handler("logs\\error.log")
    log.debug(f"[{module}] : [{error}]")

def log_conversation(user, assistant):
    file_handler("logs\\conversation.log")
    log.info(f"[User] : [{user}] \n [Velix] : [{assistant}]")

def log_execution(intent, parameters, status):
    file_handler("logs\\execution.log")
    log.info(
        f"[Intent]: \n {intent} \n\n [Parameters]: \n {parameters} \n\n [Status]: \n {status}"
    )

def log_memory(action, data):
    file_handler("logs\\memory.log")
    log.info(f"[Action]: \n {action} \n\n [Data]: \n {data}")

def log_startup(message):
    file_handler("logs\\system.log")
    log.info(f"[Startup] : [{message}]")

    def log_event(event_name, payload):
        file_handler("logs\\debug.log")
        log.info(f"[Event]: \n {event_name} \n\n [Payload]: \n {payload}")






