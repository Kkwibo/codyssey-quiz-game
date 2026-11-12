from quiz import Quiz
from quiz_data import get_default_quizzes


def get_number(prompt, min_value, max_value):
    """min_value ~ max_value 사이의 숫자를 입력받을 때까지 반복한다."""
    while True:
        raw = input(prompt).strip()

        if raw == "":
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue

        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        if number < min_value or number > max_value:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number


def get_text(prompt):
    """비어 있지 않은 글자를 입력받을 때까지 반복한다."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("⚠️ 내용이 비어 있습니다. 다시 입력하세요.")


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스."""

    def __init__(self):
        self.quizzes = get_default_quizzes()  # Quiz 객체들의 list
        self.best_score = None # 최고 점수

    def play(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여 준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            user_answer = get_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

    def add_quiz(self):
        """사용자에게 문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = get_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = get_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = get_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print("✅ 퀴즈가 추가되었습니다!")

    def show_quizzes(self):
        """등록된 퀴즈의 문제 목록을 출력한다."""
        # 1. 퀴즈가 없으면 안내하고 끝내기
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        # 2. 제목과 개수 출력
        print(f"\n 📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")

        # 3. 구분선
        print("=" * 40)

        # 4. 번호와 문제를 하나씩 출력
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")

        # 5. 구분선
        print("=" * 40)

    def show_score(self):
        """최고 점수를 출력한다."""
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.")
            return
        
        print(f"\n🏆 최고 점수: {self.best_score}점")

    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print()
        print("=" * 40)
        print("     🎯 나만의 퀴즈 게임 (개발 상식) 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self):
        """종료를 고를 때까지 메뉴를 보여 주고 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = get_number("선택: ", 1, 5)

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("👋 프로그램을 종료합니다.")
                break