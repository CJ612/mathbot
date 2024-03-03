from ai import TestAi
from send_error_msg import send_error_msg_to_admnin

class TestResult:
    def __init__(self) -> None:
        self.answer_list = [("- A) 27", "- B) 30", "- C) 15", "- D) 18"),
                            ("- A) 3", "- B) 6", "- C) 9", "- D) 0"),
                            ("- A) 45 градусов", "- B) 90 градусов", "- C) 180 градусов", "- D) 30 градусов"),
                            ("- A) 14", "- B) 19", "- C) 17", "- D) 12"),
                            ("- A) 8", "- B) 16", "- C) 32", "- D) 64")
                            ]
        self.right_answers = (self.answer_list[0][0], 
                              self.answer_list[1][0], 
                              self.answer_list[2][1], 
                              self.answer_list[3][1], 
                              self.answer_list[4][1]
                              )
        self.results = ({(0, 20): '''Вы не прошли тест. 
            Начнем с малого! Учитесь и практикуйтесь.
            '''},
            {(20, 40):'''Вы успешно прошли тест на 20% правильно.
            Ваша умственная острота начинает пробиваться  
            сквозь туман неверных ответов. 
            Продолжайте учиться и расти!
            '''},
            {(40, 60): '''Вы успешно прошли тест на 40% правильно.
            Вы на верном пути! 
            Не забывайте изучать те вопросы, 
            где допущены ошибки.
            '''},
            {(60, 80): '''Вы успешно прошли тест на 60% правильно.
            Ваши знания растут! 
            Ошибки — это всего лишь шаги к успеху.
            '''},
            {(80, 100): '''Вы успешно прошли тест на 80% правильно.
            Вы близки к совершенству! 
            Продолжайте учиться так же усердно.
            '''},
            {(100, 110): '''Вы успешно прошли тест на 100% правильно. 
            Ваша умственная острота впечатляет!
            '''}
            )

    def define_result(self, fsm_result) -> int:
        answers = self.generate_answers(fsm_result)
        sum = 0
        for key, value in answers.items():
            if value == self.right_answers[key]:
                sum += 20
        return sum

    def generate_answers(self, fsm_result: dict) -> dict:
        result = {}
        for i in range(5):
            result[i] = fsm_result['Q' + str(i + 1)]
        return result

    def show_result(self, result: int) -> tuple:
        for dict_result in self.results:
            for key, value in dict_result.items():
                if key[0] <= result < key[1]:
                    text = value
                    break

        test = TestAi('cute cat wearing graduation cap and glasses reading a book, 3d art')
        try:
            img_url = test.generate_ai_image()
        except Exception:
            img_url = 'https://img.freepik.com/premium-photo/cat-with-glasses-book_840789-530.jpg'
        return (text, img_url)