from quiz_game import QuizGame, get_number

MENU_MIN = 1
MENU_MAX = 5


def show_menu():
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


def main():
    """프로그램의 시작점. 종료를 고를 때까지 메뉴를 반복한다."""
    game = QuizGame()

    while True:
        show_menu()
        choice = get_number("선택: ", MENU_MIN, MENU_MAX)

        if choice == 1:
            game.play()
        elif choice == 2:
            print("📌 퀴즈 추가 기능은 준비 중입니다.")
        elif choice == 3:
            print("📋 퀴즈 목록 기능은 준비 중입니다.")
        elif choice == 4:
            print("🏆 점수 확인 기능은 준비 중입니다.")
        elif choice == 5:
            print("👋 프로그램을 종료합니다.")
            break


if __name__ == "__main__":
    main()