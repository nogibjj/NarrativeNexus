import json

def read_json_file(filepath):
    """Reads a JSON file and returns the data."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(filepath, data):
    """Writes data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_valid_choices(limit):
    """Returns a set of valid choices based on the limit."""
    choices = ['A', 'B', 'C', 'D', 'E']
    return set(choices[:limit])

def validate_answers(articles, valid_limits):
    """Validates that all answers adhere to the allowed options."""
    valid_choices = {i: get_valid_choices(limit) for i, limit in enumerate(valid_limits, 1)}
    for i, article in enumerate(articles):
        new_answers = {}
        for key, value in article['answers'].items():
            question_num = int(key)
            if value not in valid_choices[question_num]:
                print(f"Article {i+1}, Question {key}: Invalid answer '{value}'")
                new_value = input(f"Enter the correct answer for Question {key} (valid choices: {valid_choices[question_num]}): ")
                while new_value not in valid_choices[question_num]:
                    print(f"Invalid answer. Please enter one of {valid_choices[question_num]}.")
                    new_value = input(f"Enter the correct answer for Question {key}: ")
                new_answers[key] = new_value
            else:
                new_answers[key] = value
        article['answers'] = new_answers
    return articles

# def validate_answers(articles):
#     """Validates that all answers are one of 'A', 'B', 'C', 'D', 'E'."""
#     valid_answers = {'A', 'B', 'C', 'D', 'E'}
#     for i, article in enumerate(articles):
#         new_answers = {}
#         for key, value in article['answers'].items():
#             if value not in valid_answers:
#                 print(f"Article {i+1}, Question {key}: Invalid answer '{value}'")
#                 new_key = input(f"Enter the correct question number for Question {key}: ")
#                 new_value = input(f"Enter the correct answer for Question {new_key}: ")
#                 while new_value not in valid_answers:
#                     print("Invalid answer. Please enter one of 'A', 'B', 'C', 'D', or 'E'.")
#                     new_value = input(f"Enter the correct answer for Question {new_key}: ")
#                 new_answers[new_key] = new_value
#             else:
#                 new_answers[key] = value
#         article['answers'] = new_answers
#     return articles

def get_choices_limits(questions):
    """Returns a list of the number of possible choices for each question."""
    choices_limits = []
    for q_key in sorted(questions.keys(), key=lambda x: int(x[1:])):
        num_choices = len(questions[q_key]['choices'])
        choices_limits.append(num_choices)
    return choices_limits


def main():
    # data_path = "./data/raw_data/"
    data_path = "./data/QnA_data/"
    questions = read_json_file("./data/QnA_data/questions.json")

    # Get the number of choices for each question
    valid_limits = get_choices_limits(questions)
    
    # Ensure the list has 80 elements
    if len(valid_limits) != 80:
        print(f"Warning: The number of questions is {len(valid_limits)}, expected 80.")

    # filename = "QnA_test.json"

    # filename = "QnA_summary_zho_Territorial_disputes_in_the_South_China_Sea_100.json"
    # filename = "QnA_summary_eng_Territorial_disputes_in_the_South_China_Sea_100.json"
    # filename = "QnA_summary_zho_Gaza_100.json"
    # filename = "QnA_summary_eng_Gaza_100.json"
    # filename = "QnA_summary_hin_India_election_2024_100.json"
    filename = "QnA_summary_eng_India_election_2024_100.json"
    filepath = data_path + filename

    # Read the JSON file
    articles = read_json_file(filepath)
    
    # Ensure all articles have exactly 80 answers
    total_questions = 80
    for i, article in enumerate(articles):
        if 'answers' not in article:
            print(f"Article {i+1} is missing the 'answers' key.")
            print(f"Article {i+1} has 0 answers.")
            return
        if len(article['answers']) != total_questions:
            print(f"Article {i+1} has {len(article['answers'])} answers.")
            return
    print(f"All articles have {total_questions} answers.")

    # Validate and correct answers
    articles = validate_answers(articles, valid_limits)
    print("All answers have been validated.")
    # Write the modified data back to the JSON file
    write_json_file(filepath, articles)

if __name__ == "__main__":
    main()
