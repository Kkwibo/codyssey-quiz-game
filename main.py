from quiz_game import QuizGame


def main():
    """프로그램의 시작점. 게임 객체를 만들고 실행한다."""
    game = QuizGame()

    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        game.save()
        print("💾 저장 완료! 👋 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()