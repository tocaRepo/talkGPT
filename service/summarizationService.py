from gensim.summarization import summarize
from nltk.tokenize import sent_tokenize
import nltk

nltk.download("punkt")
from utils.logger import Logger

# Create a logger instance with the name "summarizationService"
logger = Logger("summarizationService")


def summarize_text(original_text):
    if len(original_text) > 50:
        sentences = sent_tokenize(original_text)

        # check if the input text has only one sentence
        if len(sentences) <= 1:
            # if the input text has only one sentence, return the original text
            return original_text

        # join the sentences into a single string
        text = " ".join(sentences)

        try:
            summary = summarize(text, word_count=80)
            if summary:
                # return the summary
                logger.info("summary:" + summary)
                return summary
        except:
            logger.info("An exception occurred")
            # summarize the text using the TextRank algorithm
            return original_text
    return original_text
