import logging

def customLog():
    #logger configurations
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(lineno)d:%(levelname)s:%(message)s')


    file_Handler = logging.FileHandler('log\\gkcaLogger.log', mode = 'w')
    file_Handler.setFormatter(formatter)
    
    logger.addHandler(file_Handler)
    
    return logger