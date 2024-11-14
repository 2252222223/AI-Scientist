import pandas as pd


class Human_Review:
    def __init__(self):
        pass

    def review_result(self, note, result):
        if isinstance(result, str):
            print(note)
            user_input = input("user input:")
            if user_input.lower() == 'yes':
                return result
            elif user_input.lower()== "correct":
                return "yes"
            else:
                return user_input
        elif isinstance(result, pd.DataFrame):
            print(note)
            user_input = input("user input:")
            if user_input.lower() == 'yes':
                return result
            else:
                num = user_input.split(",")
                aa = [int(i) for i in num]
            return result.loc[aa, :]