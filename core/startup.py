def initialize_logger():
   from utils.logger import logger as log
   log.log_info("Startup", "The logger initialized now.")

   
def load_environment():

   import docs.config as config 
   assistant_name = config.ASSISTANT_NAME
   wake_word = config.WAKE_WORD
   ollama_host = config.OLLAMA_HOST
   ollama_model = config.OLLAMA_MODEL
   voice_rate = config.VOICE_RATE
   voice_volume = config.VOICE_VOLUME
   debug = config.DEBUG
   log_level = config.LOG_LEVEL
