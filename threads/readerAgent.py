from utils.logger import Logger

logger = Logger("readerAgent")


def job(recorderQueue):
    # The code that should be executed
    print("write your request: ")
    user_input = input()
    logger.info("user input: " + user_input)
    recorderQueue.put(user_input)


def run_job(recorderQueue):
    # Run the readerAgent job continuously
    while True:
        try:
            job(recorderQueue)
        except Exception as e:
            logger.error("An error occurred while executing job: " + str(e))
