import json
import re


class Parser:
    @staticmethod
    def is_valid_json(json_str):
        if json_str is not None:
            try:
                json.loads(json_str)
                return True
            except ValueError:
                pass
        return False

    @staticmethod
    def extract_code(response):
        pattern1 = r"```(?:json\n)?\s*({[\s\S]*?})\s*```"
        pattern2 = r"```json\n\s*({[\s\S]*?})\s*```"
        pattern3 = r"```(?:json\n)?([\s\S]*?)```"
        match1 = re.search(pattern1, response)
        match2 = re.search(pattern2, response)
        match3 = re.search(pattern3, response)
        if match1:
            #print("extract_code match1")
            return match1.group(1) or match1.group(2)
        elif match2:
            #print("extract_code match2")
            return match2.group(1) or match2.group(2)
        elif match3:
            #print("extract_code match3")
            return match3.group(1) or match3.group(2)
        else:
            return Parser.extract_code_generic(response)

    @staticmethod
    def extract_code_generic(response):
        pattern = r"```(?:\w+\n)?([\s\S]+?)```"
        match = re.search(pattern, response)
        if match:
            #print("extract_code_generic match")
            return match.group(1) or match.group(2)
        else:
            return None

    @staticmethod
    def contains_code(text):
        pattern = r"```(?:\w+\n)?([\s\S]+?)```"
        match = re.search(pattern, text)
        if match:
            return match.group(1) or match.group(2)
        else:
            return None

    @staticmethod
    def parse_json_string(json_string):
        try:
            parsed_json = json.loads(json_string)
            return parsed_json
        except ValueError:
            return None


# result = Parser.extract_code("""Thank you for the additional requirements. Here is a Python script that meets all of the requirements for the Folder Size extension:
# ```
# python folder_size.py /path/to/folder
# ```
# """)
# print(result)
