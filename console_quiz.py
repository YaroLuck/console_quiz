import sys
import re
import signal

class Option:
    def __init__(self, text, is_correct=False):
        self._text = text
        self._is_correct = is_correct

    def __str__(self):
        return self._text

    @property
    def is_correct(self):
        return self._is_correct

class Question:
    def __init__(self, text):
        self._text = text
        self._options = []

    @property
    def text(self):
        return self._text

    @property
    def options(self):
        return self._options

    def add_option(self, text, is_correct=False):
        self._options.append(Option(text, is_correct))
        
    def get_correct_indices(self):
        return [i for i, option in enumerate(self._options) if option.is_correct]

class Answer:
    def __init__(self, question, user_answers, is_correct):
        self._question = question
        self._user_answers = user_answers
        self._is_correct = is_correct

    @property
    def question(self):
        return self._question

    @property
    def user_answers(self):
        return self._user_answers

    @property
    def is_correct(self):
        return self._is_correct

class Statistic:
    def __init__(self):
        self._total_count = 0
        self._correct_count = 0
        self._answers = []

    def add_answer(self, question, user_answers, is_correct):
        self._total_count += 1
        if is_correct:
            self._correct_count += 1
        self._answers.append(Answer(question, user_answers, is_correct))

    def print(self):
        print("\n=== Статистика ===")
        print(f"Всего вопросов: {self._total_count}")
        print(f"Правильных ответов: {self._correct_count}")
        print(f"Процент правильных ответов: {self._get_percentage():.2f}%")
        print("\nДетальная статистика:")
        for i, answer in enumerate(self._answers, 1):
            status = "✅" if answer.is_correct else "❌"
            user_answer_str = ", ".join(str(x) for x in answer.user_answers)
            correct_answer_str = ", ".join(str(x) for x in answer.question.get_correct_indices())
            print(f"Вопрос {i}: {answer.question.text}")
            print(f"Ваш ответ: [{user_answer_str}] {status}")
            if not answer.is_correct:
                print(f"Правильный ответ: [{correct_answer_str}]")

    def _get_percentage(self):
        return (self._correct_count / self._total_count * 100) if self._total_count > 0 else 0

class Quiz:
    def __init__(self):
        self._questions = []
        self._statistic = Statistic()

    def run(self):
        file_path = "questions.txt"
        if not self._read_questions(file_path) or not self._questions:
            print("Вопросы не найдены!")
            return
        
        self.__print_instructions()
        
        for question in self._questions:
            print(f"\n{question.text}")
            for i, option in enumerate(question.options):
                print(f"[{i}] {option}")
                
            while True:
                answer = input("> ").strip().lower()
                
                if answer == 'exit':
                    self._statistic.print()
                    return
                    
                try:
                    user_answers = self.__parse_answer(answer)
                    if all(0 <= x < len(question.options) for x in user_answers):
                        break
                    else:
                        print("Некорректный номер варианта!")
                except ValueError:
                    print("Введите номера вариантов числом через пробел или в формате [номер]!")
                    
            correct = sorted(question.get_correct_indices()) == sorted(user_answers)
            self._statistic.add_answer(question, user_answers, correct)
            
            if correct:
                print("✅ Правильно!")
            else:
                print("❌ Неправильно!")
                print(f"Правильные ответы: {', '.join(str(x) for x in question.get_correct_indices())}")
            
        self._statistic.print()

    def _read_questions(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            question_blocks = content.split('\n\n')
            
            for block in question_blocks:
                if not block.strip():
                    continue
                    
                lines = block.split('\n')
                question_text = lines[0].strip()
                question = Question(question_text)
                
                for line in lines[1:]:
                    if line.strip():
                        is_correct = line.strip().startswith('[*]')
                        option_text = re.sub(r'\[\*\]|\[\]', '', line.strip()).strip()
                        question.add_option(option_text, is_correct)
                
                self._questions.append(question)
                
            return True
        except FileNotFoundError:
            print("Файл не найден!")
            return False

    def __print_instructions(self):
        print("Для выхода введите 'exit'")
        print("Вводите номера вариантов ответа через пробел (начиная с 0)")
        print("Или используйте формат [номер] для выбора")
        print("Для прерывания используйте Ctrl+C\n")

    def __parse_answer(self, answer):
        if answer.startswith('[') and answer.endswith(']'):
            return [int(answer[1:-1])]
        return [int(x) for x in answer.split()]

_quiz_instance = None

def _signal_handler(sig, frame):
    """Обработчик сигнала прерывания"""
    if _quiz_instance:
        _quiz_instance._statistic.print()
    sys.exit(0)

def main():
    global _quiz_instance
    _quiz_instance = Quiz()
    
    signal.signal(signal.SIGINT, _signal_handler)
    
    _quiz_instance.run()

if __name__ == "__main__":
    main()