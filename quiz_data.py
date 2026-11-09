from quiz import Quiz


def get_default_quizzes():
    """처음 실행할 때(state.json이 없을 때) 사용할 기본 퀴즈 목록을 돌려준다."""
    return [
        # ── 리눅스 ──
        Quiz(
            "비어 있는 디렉토리를 삭제하는 리눅스 명령은?",
            ["rmdir", "rm", "redir", "mkdir"],
            1,
        ),
        Quiz(
            "파일 권한 rwxr-xr-x를 숫자로 표기하면?",
            ["644", "751", "777", "755"],
            4,
        ),
        Quiz(
            "현재 작업 중인 디렉토리의 경로를 출력하는 명령은?",
            ["ls -a", "pwd", "cd", "whoami"],
            2,
        ),
        Quiz(
            "src 디렉토리를 안의 내용물까지 dst로 복사하는 명령은?",
            ["cp src dst", "cp -d src dst", "cp -r src dst", "mv src dst"],
            3,
        ),
        # ── Git ──
        Quiz(
            "Git 사용자 이름을 kim으로 전역 설정하는 명령은?",
            [
                'git config --global user.name "kim"',
                'git remote --global user.name "kim"',
                'git exec --global user.name "kim"',
                'git init user.name "kim"',
            ],
            1,
        ),
        Quiz(
            "원격 저장소를 origin이라는 이름으로 추가하는 명령은?",
            [
                "git push add origin URL",
                "git remote origin URL",
                "git init add URL",
                "git remote add origin URL",
            ],
            4,
        ),
        Quiz(
            "원격 저장소를 내 컴퓨터로 복제하는 명령은?",
            ["git cp URL", "git clone URL", "git pull URL", "git copy URL"],
            2,
        ),
        # ── Docker ──
        Quiz(
            "다운로드한 Docker 이미지 목록을 출력하는 명령은?",
            ["docker ps -a", "docker list", "docker images", "docker image"],
            3,
        ),
        Quiz(
            "실행 중인 web 컨테이너에 bash로 접속하는 명령은?",
            [
                "docker exec -it web bash",
                "docker bash web",
                "docker exec -it web",
                "docker run -it web bash",
            ],
            1,
        ),
        Quiz(
            "실행 중인 site 컨테이너를 강제로 삭제하는 명령은?",
            ["docker rm site", "docker rmi site", "docker stop -f site", "docker rm -f site"],
            4,
        ),
    ]