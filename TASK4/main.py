import json
from difflib import get_close_matches

def load_data_base(file_path:str):
    with open(file_path,'r') as file:
        data:dict=json.load(file)
    return data

def save_data_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question:str,questions:list[str]) ->str|None:
    matches:list=get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question:str,data_base:dict)->str|None:
    for q in data_base["questions"]:
        if q["question"]==question:
            return q["answer"]
    return None


def chatbot():
    data_base:dict=load_data_base('data_base.json')
    while True:
        user_input:str=input("YOU: ")

        if user_input.lower()=='quit':
            break
        best_match:str|None=find_best_match(user_input,[q["question"] for q in data_base["questions"]])
        
        if best_match:
            answer:str=get_answer_for_question(best_match,data_base)
            print(f"Bot:{answer}")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer: str = input("Type the answer or 'skip' to skip: ")

            if new_answer.lower() != 'skip':
                data_base["questions"].append({"question": user_input, "answer": new_answer})
                save_data_base('data_base.json', data_base)
                print("Bot: Thank you! I've learned something new.")

if __name__ == "__main__":
    chatbot()
