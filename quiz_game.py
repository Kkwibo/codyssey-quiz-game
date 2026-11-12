import json
import os
import shutil
from pathlib import Path

from quiz import Quiz
from quiz_data import get_default_quizzes

# 프로젝트 루트(이 파일이 있는 폴더)에 두는 데이터 파일들
BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / "state.json"            # 현재 데이터
BACKUP_FILE = BASE_DIR / "state.json.bak"       # 직전 저장본 (자동 백업)
CORRUPT_FILE = BASE_DIR / "state.json.corrupt"  # 손상된 파일 보관용
TEMP_FILE = BASE_DIR / "state.json.tmp"         # 저장 중 임시 파일

# 파일이 손상되었다고 판단할 오류들
CORRUPT_ERRORS = (json.JSONDecodeError, KeyError, TypeError, ValueError)


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


def read_state(path):
    """path의 JSON 파일을 읽어 (퀴즈 목록, 최고 점수)를 돌려준다. 형식이 잘못되면 예외를 낸다."""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
    best_score = data.get("best_score")
    if best_score is not None and (not isinstance(best_score, int) or not 0 <= best_score <= 100):
        raise ValueError("최고 점수는 0~100 사이 정수여야 합니다.")

    return quizzes, best_score


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스."""

    def __init__(self):
        self.quizzes = []        # Quiz 객체들의 list
        self.best_score = None   # 최고 점수 (아직 안 풀었으면 None)
        self.load()

    # ---------- 파일 저장 / 불러오기 ----------

    def load(self):
        """state.json을 불러온다. 없거나 손상되면 백업에서 복구하고, 백업도 없으면 기본 데이터를 쓴다."""
        try:
            self.quizzes, self.best_score = read_state(STATE_FILE)
            score_text = "없음" if self.best_score is None else f"{self.best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고 점수 {score_text})")
            return
        except FileNotFoundError:
            if self.restore_backup():
                return
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
        except CORRUPT_ERRORS:
            print("⚠️ 저장 파일이 손상되었습니다. 손상된 파일은 state.json.corrupt로 보관합니다.")
            self.keep_corrupt_file()
            if self.restore_backup():
                return
            print("⚠️ 사용할 수 있는 백업이 없어 기본 퀴즈로 복구합니다.")
        except OSError:
            print("⚠️ 저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다.")
            print("   파일 권한을 확인하세요: ls -l state.json  (필요하면 chmod 644 state.json)")

        self.quizzes = get_default_quizzes()
        self.best_score = None

    def restore_backup(self):
        """state.json.bak에서 데이터를 복구한다. 성공하면 True를 돌려준다."""
        try:
            self.quizzes, self.best_score = read_state(BACKUP_FILE)
        except (OSError, *CORRUPT_ERRORS):
            return False

        print(f"♻️ 백업 파일(state.json.bak)에서 복구했습니다. (퀴즈 {len(self.quizzes)}개)")
        self.save()
        return True

    def keep_corrupt_file(self):
        """손상된 state.json을 지우지 않고 state.json.corrupt로 이름을 바꿔 보관한다."""
        try:
            os.replace(STATE_FILE, CORRUPT_FILE)
        except OSError:
            pass

    def save(self):
        """현재 데이터를 state.json에 저장한다. 직전 저장본은 state.json.bak으로 백업한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            # 1) 임시 파일에 먼저 끝까지 쓴다 (쓰는 도중 꺼져도 원본은 안전)
            with open(TEMP_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            # 2) 기존 state.json을 백업으로 복사한다
            if STATE_FILE.exists():
                shutil.copyfile(STATE_FILE, BACKUP_FILE)
            # 3) 임시 파일을 state.json으로 한 번에 교체한다
            os.replace(TEMP_FILE, STATE_FILE)
        except OSError:
            print("⚠️ 파일 저장 중 오류가 발생했습니다. 폴더 쓰기 권한을 확인하세요.")

    # ---------- 게임 기능 ----------

    @staticmethod
    def calculate_score(correct, total):
        """정답 수와 문제 수로 점수(100점 만점, 반올림)를 계산한다."""
        return round(correct / total * 100)

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

        score = self.calculate_score(correct, total)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
            self.save()
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
        self.save()
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
                self.save()
                print("💾 저장 완료! 👋 프로그램을 종료합니다.")
                break