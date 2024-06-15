import json

def read_json_file(filepath):
    """Reads a JSON file and returns the data."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(filepath, data):
    """Writes data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def validate_answers(articles):
    """Validates that all answers are one of 'A', 'B', 'C', 'D', 'E'."""
    valid_answers = {'A', 'B', 'C', 'D', 'E'}
    for i, article in enumerate(articles):
        new_answers = {}
        for key, value in article['answers'].items():
            if value not in valid_answers:
                print(f"Article {i+1}, Question {key}: Invalid answer '{value}'")
                new_key = input(f"Enter the correct question number for Question {key}: ")
                new_value = input(f"Enter the correct answer for Question {new_key}: ")
                while new_value not in valid_answers:
                    print("Invalid answer. Please enter one of 'A', 'B', 'C', 'D', or 'E'.")
                    new_value = input(f"Enter the correct answer for Question {new_key}: ")
                new_answers[new_key] = new_value
            else:
                new_answers[key] = value
        article['answers'] = new_answers
    return articles

def main():

    data_path = "./data/raw_data/"
    
    filename = "QnA_test.json"
    # filename = "QnA_summary_zho_Territorial_disputes_in_the_South_China_Sea_100.json"
    # filename = "QnA_summary_zho_Gaza_100.json"
    # filename = "QnA_summary_hin_India_election_2024_100.json"

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
    articles = validate_answers(articles)
    
    # Write the modified data back to the JSON file
    write_json_file(filepath, articles)

if __name__ == "__main__":
    main()
