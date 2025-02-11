import json

def load_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        sections = content.split('\n\n')
        for section in sections:
            lines = section.strip().split('\n')
            question_text = lines[0].strip()
            answers = []
            correct_answers = []
            for line in lines[1:]:
                if line.startswith('*'):
                    answer_text = line[2:].strip()
                    is_correct = 'верно' in line.lower() or 'выбрано' in line.lower()
                    answers.append(answer_text)
                    if is_correct:
                        correct_answers.append(answer_text)
            questions.append({
                'question': question_text,
                'answers': answers,
                'correct_answers': correct_answers
            })
    return questions

def ask_question(question):
    print(question['question'])
    for i, answer in enumerate(question['answers'], start=1):
        print(f"{i}. {answer}")
    user_input = input("Введите номер(а) правильного ответа(ов), разделенные пробелом или 'exit' для завершения: ").strip()
    if user_input.lower() == 'exit':
        return None
    user_answers = [int(num) - 1 for num in user_input.split()]
    selected_answers = [question['answers'][i] for i in user_answers]
    return selected_answers

def main():
    file_path = 'questions.txt'  # Укажите путь к вашему файлу с вопросами
    questions = load_questions(file_path)
    score = 0
    total_questions = len(questions)

    for i, question in enumerate(questions, start=1):
        print(f"\nВопрос {i} из {total_questions}:")
        user_answers = ask_question(question)
        if user_answers is None:
            break
        if set(user_answers) == set(question['correct_answers']):
            print("Правильно!")
            score += 1
        else:
            print("Неправильно.")
            print("Правильный(е) ответ(ы):", ', '.join(question['correct_answers']))

    print("\nТестирование завершено.")
    print(f"Правильных ответов: {score}/{total_questions}")

if __name__ == "__main__":
    main()

