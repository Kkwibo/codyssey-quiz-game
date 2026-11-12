# 🎯 나만의 퀴즈 게임 - 개발 상식 퀴즈

터미널에서 동작하는 객관식 퀴즈 게임입니다.
Python 기본 문법과 클래스로 기능을 나누어 구현하고, 퀴즈와 최고 점수를 `state.json`에 저장해 프로그램을 다시 실행해도 데이터가 유지됩니다.
개발 과정은 Git으로 기능 단위 커밋, 브랜치 생성·병합, clone·pull까지 기록했습니다.

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [퀴즈 주제와 선정 이유](#2-퀴즈-주제와-선정-이유)
3. [실행 방법](#3-실행-방법)
4. [기능 목록](#4-기능-목록)
5. [실행 화면](#5-실행-화면)
6. [파일 구조와 클래스 설계](#6-파일-구조와-클래스-설계)
7. [데이터 파일 설명 (state.json)](#7-데이터-파일-설명-statejson)
8. [개발 환경](#8-개발-환경)
9. [Git 작업 기록](#9-git-작업-기록)
10. [트러블슈팅](#10-트러블슈팅)
11. [커밋 기록 (총 커밋 수)](#11-커밋-기록-총-커밋-수)
12. [클래스를 사용한 이유와 재사용성](#12-클래스를-사용한-이유와-재사용성)
13. [대용량 데이터 성능 분석 (1,000개 이상)](#13-대용량-데이터-성능-분석-1000개-이상)
14. [백업 정책과 복구 절차](#14-백업-정책과-복구-절차)
15. [유지보수 가이드 (요구 변경 시 수정 위치)](#15-유지보수-가이드-요구-변경-시-수정-위치)

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로그램 | 터미널(콘솔) 기반 객관식 퀴즈 게임 |
| 언어 | Python 3.10 이상 (표준 라이브러리만 사용) |
| 주요 기능 | 퀴즈 풀기 / 퀴즈 추가 / 퀴즈 목록 / 최고 점수 확인 / 종료 |
| 데이터 저장 | 프로젝트 루트의 `state.json` (UTF-8) |
| 코드 구조 | `Quiz`(문제 1개), `QuizGame`(게임 전체) 2개 클래스로 역할 분리 |

---

## 2. 퀴즈 주제와 선정 이유

**주제: 개발 상식 (리눅스 · Git · Docker 명령어)**

1-1 과제와 CLI 단답형 연습에서 리눅스, Git, Docker 명령을 자주 헷갈렸고, 그때 틀렸던 명령을 오답 선택지로 넣어서 반복해서 복습하려고 이 주제를 선택했습니다.

| 분야 | 문제 수 | 예시 |
|---|---|---|
| 리눅스 | 4 | 빈 디렉토리 삭제, 권한 숫자 표기(755), 현재 경로 출력, 디렉토리 복사(`-r`) |
| Git | 3 | 사용자 이름 전역 설정, 원격 저장소 추가, 저장소 복제 |
| Docker | 3 | 이미지 목록, 컨테이너 접속(`exec -it`), 강제 삭제(`rm -f`) |

---

## 3. 실행 방법

### 요구 사항

- Python **3.10 이상**
- 외부 라이브러리 설치 필요 없음 (표준 라이브러리 `json`, `os`, `shutil`, `pathlib`만 사용)

### 실행

```bash
git clone https://github.com/Kkwibo/codyssey-quiz-game.git
cd codyssey-quiz-game
python3 main.py
```

> Windows(PowerShell)에서 Python을 직접 설치한 경우 `python main.py`로 실행합니다.

### 처음 실행할 때

`state.json`이 없으면 기본 퀴즈 10개로 시작하고, 퀴즈를 추가하거나 최고 점수가 갱신되거나 종료할 때 `state.json`이 자동으로 만들어집니다.

```
📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.
```

---

## 4. 기능 목록

### 메뉴 기능

| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 저장된 퀴즈를 순서대로 출제하고, 문제마다 정답/오답을 알려 줍니다. 마지막에 정답 수와 점수(100점 만점)를 보여 주고, 최고 점수보다 높으면 갱신합니다. 퀴즈가 없으면 안내 후 메뉴로 돌아갑니다. |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호(1~4)를 입력받아 새 퀴즈를 등록하고 즉시 파일에 저장합니다. |
| 3 | 퀴즈 목록 | 등록된 퀴즈의 번호와 문제를 출력합니다. 퀴즈가 없으면 안내 메시지를 출력합니다. |
| 4 | 점수 확인 | 최고 점수를 출력합니다. 아직 퀴즈를 풀지 않았다면 안내 메시지를 출력합니다. |
| 5 | 종료 | 데이터를 저장하고 프로그램을 종료합니다. |

### 입력 / 예외 처리

| 상황 | 예시 입력 | 처리 |
|---|---|---|
| 앞뒤 공백 | ` 1 ` | 공백을 제거한 뒤 정상 처리 |
| 숫자가 아닌 입력 | `abc` | ⚠️ 안내 후 다시 입력 |
| 허용 범위 밖 숫자 | 메뉴 `9`, 정답 `0` | ⚠️ 안내 후 다시 입력 |
| 빈 입력 | Enter | ⚠️ 안내 후 다시 입력 |
| 빈 문제·선택지 (퀴즈 추가) | Enter, 공백만 | ⚠️ 안내 후 다시 입력 |
| Ctrl + C (`KeyboardInterrupt`) | | 안내 메시지 → 저장 → 안전 종료 |
| 입력 종료 (`EOFError`, Ctrl + D) | | 안내 메시지 → 저장 → 안전 종료 |
| `state.json` 없음 | | 백업(`state.json.bak`)이 있으면 복구, 없으면 기본 퀴즈 데이터로 시작 |
| `state.json` 손상 | | 손상 파일을 `.corrupt`로 보관 → 백업에서 복구 → 백업도 없으면 기본 퀴즈 |

---

## 5. 실행 화면

### 메뉴

![메뉴 화면](docs/screenshots/menu.png)

### 퀴즈 풀기

![퀴즈 풀기](docs/screenshots/play.png)

### 퀴즈 추가

![퀴즈 추가](docs/screenshots/add_quiz.png)

### 퀴즈 목록 · 점수 확인

![퀴즈 목록과 점수 확인](docs/screenshots/score.png)

---

## 6. 파일 구조와 클래스 설계

### 파일 구조

```
codyssey-quiz-game/
├── main.py              # 프로그램 시작점 (QuizGame 실행, Ctrl+C·EOF 처리)
├── quiz.py              # Quiz 클래스: 퀴즈 1문제
├── quiz_game.py         # QuizGame 클래스: 메뉴·풀기·추가·목록·점수·저장/불러오기·백업
├── quiz_data.py         # 기본 퀴즈 10문제 (state.json이 없을 때 사용)
├── tools/
│   └── benchmark.py     # 퀴즈 수에 따른 성능·메모리 측정 스크립트
├── state.json           # 실행 중 생성되는 데이터 파일 (Git 제외)
├── state.json.bak       # 직전 저장본 자동 백업 (Git 제외)
├── state.json.corrupt   # 손상 시 보관되는 원본 (Git 제외, 손상 시에만 생성)
├── .gitignore           # __pycache__, state.json* 등 제외 목록
├── README.md
└── docs/
    └── screenshots/     # 실행 화면, 개발 환경, git log 스크린샷
```

### 클래스 설계

**`Quiz`** (`quiz.py`) - 퀴즈 한 문제를 표현합니다.

| 구분 | 이름 | 설명 |
|---|---|---|
| 속성 | `question` (str) | 문제 |
| 속성 | `choices` (list) | 선택지 4개 |
| 속성 | `answer` (int) | 정답 번호 (1~4) |
| 메서드 | `display(number)` | 문제 번호와 함께 문제·선택지 출력 |
| 메서드 | `is_correct(user_answer)` | 정답 여부를 `True`/`False`로 반환 |
| 메서드 | `to_dict()` | JSON 저장용 dict로 변환 |
| 메서드 | `from_dict(data)` (classmethod) | dict에서 Quiz 객체 생성, 형식이 잘못되면 `ValueError` |

**`QuizGame`** (`quiz_game.py`) - 게임 전체를 관리합니다.

| 구분 | 이름 | 설명 |
|---|---|---|
| 속성 | `quizzes` (list) | Quiz 객체 목록 |
| 속성 | `best_score` (int 또는 None) | 최고 점수. 아직 풀지 않았으면 `None` |
| 메서드 | `run()` | 종료를 고를 때까지 메뉴 반복 |
| 메서드 | `show_menu()` | 메뉴 출력 |
| 메서드 | `play()` | 퀴즈 풀기, 점수 계산, 최고 점수 갱신 |
| 메서드 | `add_quiz()` | 퀴즈 추가 |
| 메서드 | `show_quizzes()` | 퀴즈 목록 출력 |
| 메서드 | `show_score()` | 최고 점수 출력 |
| 메서드 | `load()` / `save()` | `state.json` 불러오기 / 저장 (임시 파일 → 백업 → 원자적 교체) |
| 메서드 | `restore_backup()` / `keep_corrupt_file()` | 백업에서 복구 / 손상 파일 `.corrupt`로 보관 |
| 메서드 | `calculate_score(correct, total)` (staticmethod) | 점수 계산 (계산 방식 변경 시 이 메서드만 수정) |

입력 검증은 모듈 함수 `get_number(prompt, min, max)`와 `get_text(prompt)`로 분리해, 메뉴 선택(1~5)·정답 입력(1~4)·퀴즈 추가에서 재사용합니다.
파일 읽기와 형식 검사는 모듈 함수 `read_state(path)`로 분리해, `state.json`과 백업 파일(`state.json.bak`)을 같은 규칙으로 읽습니다.

---

## 7. 데이터 파일 설명 (state.json)

| 항목 | 내용 |
|---|---|
| 경로 | 프로젝트 루트의 `state.json` (`quiz_game.py`와 같은 폴더) |
| 인코딩 | UTF-8 (`ensure_ascii=False`로 한글을 그대로 저장) |
| 역할 | 퀴즈 목록과 최고 점수를 저장해, 프로그램을 다시 실행해도 데이터 유지 |
| 저장 시점 | 퀴즈 추가 직후, 최고 점수 갱신 직후, 종료(메뉴 5 / Ctrl+C / EOF) 시 |
| 불러오는 시점 | 프로그램 시작 시 (`QuizGame` 생성 시 `load()`) |
| Git 관리 | 실행할 때마다 내용이 바뀌는 파일이라 `.gitignore`로 제외 |

### 필드 구조

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list (str 4개) | 선택지 |
| `quizzes[].answer` | int (1~4) | 정답 번호 |
| `best_score` | int (0~100) 또는 `null` | 최고 점수 (정답 수 ÷ 문제 수 × 100, 반올림). 아직 풀지 않았으면 `null` |

### 예시

```json
{
  "quizzes": [
    {
      "question": "비어 있는 디렉토리를 삭제하는 리눅스 명령은?",
      "choices": ["rmdir", "rm", "redir", "mkdir"],
      "answer": 1
    }
  ],
  "best_score": 91
}
```

### 파일이 없거나 손상된 경우

| 상황 | 동작 |
|---|---|
| 파일 없음 (첫 실행) | `state.json.bak`이 있으면 백업에서 복구, 없으면 `📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.` |
| JSON 형식 오류, 키 누락, 선택지 개수·정답 범위·점수 범위 오류 | 손상 파일을 `state.json.corrupt`로 보관 → `state.json.bak`에서 복구 → 백업도 없거나 손상되면 기본 퀴즈 10개 |
| 파일을 읽을 수 없음 (권한 등) | `⚠️ 저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다.` + `ls -l`, `chmod 644` 안내 |

자세한 내용은 [14. 백업 정책과 복구 절차](#14-백업-정책과-복구-절차)를 참고하세요.

---

## 8. 개발 환경

| 항목 | 내용 |
|---|---|
| OS | Windows + WSL2 (Ubuntu) |
| Python | 3.14.4 |
| Git | 2.53.0 |
| 에디터 | Visual Studio Code + WSL 확장 + Python 확장 |

![개발 환경](docs/screenshots/dev_env.png)

---

## 9. Git 작업 기록

### 커밋 규칙

기능 단위로 커밋하고, 메시지 앞에 작업 종류를 붙였습니다.

| 접두어 | 의미 | 예시 |
|---|---|---|
| `Feat` | 새 기능 | `Feat: 퀴즈 목록 기능 구현` |
| `Fix` | 문제 수정 | `Fix: Ctrl+C, 입력 종료(EOF) 시 저장 후 안전하게 종료` |
| `Refactor` | 동작은 그대로, 구조 개선 | `Refactor: 메뉴 로직을 QuizGame 클래스로 이동` |
| `Docs` | 문서 | `Docs: README 작성` |
| `Test` | 테스트·측정 | `Test: 대용량 퀴즈 성능 측정 스크립트 추가` |

### 브랜치 작업

퀴즈 풀기 기능은 `feature/play` 브랜치에서 개발한 뒤 `main`에 병합했습니다.
`--no-ff` 옵션으로 병합 커밋을 남겨 그래프에서 브랜치 기록이 보이도록 했습니다.

```bash
git checkout -b feature/play      # 브랜치 생성 및 이동
# ... 퀴즈 풀기 기능 개발 ...
git commit -m "Feat: 퀴즈 풀기 기능 구현 (QuizGame 클래스, play 메서드)"
git push -u origin feature/play
git checkout main                 # main으로 이동
git merge --no-ff feature/play    # 병합
git push
```

### clone · pull

- **clone**: 학교 PC에서 작업한 저장소를 노트북에서 `git clone`으로 받아 이어서 개발했습니다.
- **복제 실습**: 저장소를 별도 디렉토리에 `clone` → README 수정 → `commit`, `push` → 원래 작업 디렉토리에서 `git pull`로 변경 사항을 가져왔습니다.

### Git 기초 명령 사용

| 명령 | 사용한 곳 |
|---|---|
| `init` | 로컬 저장소 생성 |
| `add` / `commit` | 기능 단위 커밋 |
| `push` | GitHub 업로드 |
| `checkout` | `feature/play` 브랜치 생성·이동, `main` 복귀 |
| `clone` | 노트북에서 저장소 받기, 복제 실습 |
| `pull` | 복제 실습 후 원래 디렉토리에서 변경 사항 가져오기 |

### 커밋 그래프

```bash
git log --oneline --graph
```

![git log](docs/screenshots/git_log.png)

---

## 10. 트러블슈팅

| 문제 | 원인 | 해결 |
|---|---|---|
| `wsl ~` 실행 시 `docker-desktop`으로 들어가고 `python3`, `git`이 없음 | Ubuntu가 설치되지 않아 Docker Desktop의 내부 배포판이 기본으로 지정됨 | `wsl --install -d Ubuntu`로 설치 후 `wsl.exe --set-default Ubuntu` |
| `git push` 시 터미널에서 Username을 물음 | Git이 GitHub 인증 정보를 가져올 곳이 없음 | VSCode에서 GitHub 로그인 후 VSCode(WSL) 터미널에서 push |
| 점수 확인 시 `AttributeError: 'QuizGame' object has no attribute 'show_score'` | `show_score`를 8칸 들여써서 `show_quizzes` 안의 내부 함수가 됨 | 4칸으로 맞춰 `QuizGame`의 메서드로 수정 |
| `git config --list`의 이메일이 `user.noreplay...`로 저장됨 | 이메일 주소 오타 | 올바른 noreply 주소로 `git config --global user.email` 재설정 |
| Ctrl + C를 누르면 `KeyboardInterrupt` 에러로 비정상 종료 | 예외 처리가 없었음 | `main.py`에서 `KeyboardInterrupt`, `EOFError`를 잡아 저장 후 종료 |

> 이 줄은 clone 실습을 위해 별도 디렉토리(codyssey-quiz-game-clone)에서 추가한 뒤 push했습니다.


---

## 11. 커밋 기록 (총 커밋 수)

기능 단위로 나누어 의미 있는 커밋을 남겼습니다. 이 README 작성 시점의 커밋 수는 **17개**이고(이 README 보완 커밋을 포함하면 18개), 현재 개수는 아래 명령으로 확인할 수 있습니다.

```bash
git rev-list --count HEAD                                  # 총 커밋 수
git --no-pager log --reverse --format='| %h | %s |'        # 오래된 순 커밋 목록
```

| 해시 | 커밋 메시지 |
|---|---|
| 1965ee8 | Docs: 프로젝트 초기 설정 (README, .gitignore 추가) |
| b7e19c8 | Feat: 메뉴 출력 및 입력 검증 기능 구현 |
| 0b83729 | Feat: Quiz 클래스 작성 (문제 출력, 정답 확인 메서드) |
| ee181b1 | Feat: 기본 퀴즈 데이터 추가 (개발 상식 10문제) |
| fcd9e3a | Feat: 퀴즈 풀기 기능 구현 (QuizGame 클래스, play 메서드) |
| f0e5a4e | Merge: 퀴즈 풀기 기능 병합 (feature/play → main) |
| c451256 | Feat: 퀴즈 추가 기능 구현 (문제, 선택지 4개, 정답 입력 및 건증) |
| 22f5a0a | Feat: 퀴즈 목록 기능 구현 |
| 7721794 | Feat: 점수 확인 및 최고 점수 갱신 기능 구현 |
| 3ee6f76 | Refactor: 메뉴 로직을 QuizGame 클래스로 이동, show_score 들여쓰기 정리 |
| f274e8d | Feat: state.json 저장 및 불러오기 기능 구현(UTF-8, 파일 없음/손상 처리) |
| 7c3763a | Fix: Ctrl+C, 입력 종료(EOF) 시 저장 후 안전하게 종료 |
| d5b8789 | Docs: README 작성 및 실행 화면 스크린샷 추가 |
| 67982d5 | Docs: clone 실습 - 별도 디렉토리에서 README 한 줄 추가 |
| abf34ae | Docs: 최종 커밋 그래프 스크린샷으로 교체 |
| 5e9b0be | Feat: state.json 자동 백업 및 손상 시 백업 복구, 점수 계산 메서드 분리 |
| 006b79e | Test: 대용량 퀴즈 성능 측정 스크립트 추가 |

커밋 메시지는 `Feat`(기능), `Fix`(버그 수정), `Refactor`(구조 개선), `Docs`(문서), `Test`(테스트·측정) 접두사로 구분했습니다. 브랜치 병합 흐름은 [9. Git 작업 기록](#9-git-작업-기록)의 커밋 그래프에서 확인할 수 있습니다.

---

## 12. 클래스를 사용한 이유와 재사용성

### 역할 분리

| 클래스 / 모듈 | 책임 | 모르는 것 |
|---|---|---|
| `Quiz` | 퀴즈 1개의 데이터, 출력, 정답 판정, dict 변환·검증 | 메뉴, 파일 위치, 점수 |
| `QuizGame` | 메뉴 흐름, 점수 계산, 저장/불러오기, 백업 | 퀴즈 내부 검증 규칙 (`Quiz`에 맡김) |
| `quiz_data.py` | 기본 퀴즈 데이터 | 게임 진행 방식 |

`Quiz`는 `input()`이나 파일 경로를 전혀 쓰지 않기 때문에 **다른 프로그램에서도 그대로 가져다 쓸 수 있습니다.**

### 재사용 시나리오

| 시나리오 | 재사용하는 부분 | 새로 만들 부분 |
|---|---|---|
| 웹(Flask 등) 퀴즈 페이지로 확장 | `Quiz`의 `is_correct`, `to_dict`, `from_dict` | 화면(HTML)과 라우팅만 |
| 다른 주제(영어 단어, 역사) 퀴즈 | `Quiz`, `QuizGame` 전체 | `quiz_data.py`의 기본 문제만 교체 |
| 성능 측정·테스트 | `Quiz`, `to_dict`/`from_dict` | `tools/benchmark.py`처럼 import해서 바로 사용 (실제 사용 사례) |
| 퀴즈 파일 가져오기/내보내기 | `to_dict`/`from_dict` (검증 포함) | JSON 파일 선택 기능만 |

클래스를 쓰지 않고 `dict`와 함수만으로 만들었다면 퀴즈 형식 검사 코드가 불러오기·추가·측정 스크립트마다 흩어졌을 것입니다. `Quiz.from_dict` 한 곳에 모아 두었기 때문에 **검증 규칙이 바뀌어도 한 곳만 고치면 됩니다.**

---

## 13. 대용량 데이터 성능 분석 (1,000개 이상)

### 측정 방법

```bash
python3 tools/benchmark.py
```

퀴즈를 10개 ~ 100,000개 만들어 **실제 `state.json`과 같은 형식**(JSON, UTF-8, `indent=2`, 불러올 때 `Quiz.from_dict` 검증 포함)으로 저장·불러오기 시간, 파일 크기, 메모리(`tracemalloc`), 키워드 검색 시간을 측정합니다. 임시 폴더에서만 측정해서 실제 `state.json`은 건드리지 않습니다. 실제 `save()`는 여기에 백업 복사(`state.json.bak`)가 더해지므로, 저장 시간은 측정값보다 조금 더 걸립니다.

### 측정 결과 (WSL2 Ubuntu, Python 3.14)

| 퀴즈 수 | 파일 크기 | 메모리 | 저장 | 불러오기 | 검색 |
|---:|---:|---:|---:|---:|---:|
| 10 | 2.8KB | 4.6KB | 0.2ms | 0.1ms | 0.00ms |
| 1,000 | 282.2KB | 321.6KB | 5.3ms | 2.9ms | 0.04ms |
| 10,000 | 2,831.0KB | 3,240.8KB | 81.2ms | 26.8ms | 0.21ms |
| 100,000 | 28,407.2KB | 32,592.1KB | 432.9ms | 239.5ms | 2.10ms |

### 분석

| 항목 | 시간 복잡도 | 결과 해석 |
|---|---|---|
| 불러오기 (`load`) | O(n) | 퀴즈 수에 비례. 1,000개 2.9ms로 체감 불가 |
| 저장 (`save`) | O(n) | 저장할 때마다 **파일 전체를 다시 씀** (+ 백업 복사) |
| 검색 (문제 키워드) | O(n) | list를 처음부터 끝까지 확인. 10만 개도 약 2ms |
| 목록 출력 (`show_quizzes`) | O(n) | 1,000개면 화면에 1,000줄이 출력됨 |
| 메모리 | O(n) | 퀴즈 1개당 약 0.3KB → 1,000개 약 0.3MB, 10만 개 약 32MB |

- **1,000개 수준에서는 현재 구조(list + JSON 파일)로 충분합니다.** 모든 작업이 10ms 이하입니다.
- **병목 1 — 전체 다시 쓰기:** 퀴즈 1개만 추가해도 파일 전체를 다시 저장합니다. 10만 개면 추가할 때마다 약 0.4초가 걸리고, 백업 복사까지 하면 디스크 사용량이 2배(약 56MB)가 됩니다.
- **병목 2 — 화면과 게임 길이:** 계산보다 **사람이 보는 쪽**이 먼저 한계에 닿습니다. 1,000문제를 한 번에 푸는 게임이나 1,000줄 목록은 사용하기 어렵습니다.

### 개선 방향 (데이터가 더 커질 때)

| 문제 | 개선 방법 |
|---|---|
| 한 게임에 모든 문제 출제 | `random.sample(self.quizzes, 10)`처럼 **N문제만 무작위 출제** |
| 목록이 너무 김 | 20개씩 **페이지 나누기** |
| 검색이 O(n) | 자주 찾는 키(카테고리 등)로 `dict` **인덱스**를 만들어 O(1) 조회 |
| 추가할 때마다 전체 저장 | 표준 라이브러리 **`sqlite3`**로 바꾸면 1개만 INSERT (전체 재작성 불필요) |

---

## 14. 백업 정책과 복구 절차

### 관련 파일

| 파일 | 역할 | 생성 시점 |
|---|---|---|
| `state.json` | 현재 데이터 | 저장할 때마다 |
| `state.json.bak` | **직전 저장본** (1세대 백업) | 저장할 때 기존 `state.json`을 복사 |
| `state.json.tmp` | 저장 중 임시 파일 | 저장 도중에만 잠깐 존재 |
| `state.json.corrupt` | 손상된 원본 보관 | 불러오기 중 손상이 발견되었을 때 |

네 파일 모두 `.gitignore`로 Git에서 제외합니다. 저장 시점은 퀴즈 추가, 최고 점수 갱신, 종료(메뉴 5번, Ctrl+C, EOF)입니다.

### 저장 절차 (`QuizGame.save`)

1. 데이터를 `state.json.tmp`에 **끝까지 먼저 씁니다.** 쓰는 도중 프로그램이 꺼져도 원본 `state.json`은 그대로입니다.
2. 기존 `state.json`이 있으면 `state.json.bak`으로 복사합니다 (`shutil.copyfile`).
3. `os.replace`로 임시 파일을 `state.json`으로 **한 번에 교체**합니다 (원자적 교체 → 반쯤 쓰인 파일이 남지 않음).

### 자동 복구 절차 (`QuizGame.load`)

```
state.json 읽기
 ├─ 정상 → 불러오기 완료
 ├─ 손상 → state.json.corrupt로 이름 변경(보관) → state.json.bak에서 복구 시도
 │          └─ 백업도 없거나 손상 → 기본 퀴즈 10개
 ├─ 없음 → state.json.bak이 있으면 복구, 없으면 기본 퀴즈 10개
 └─ 권한 오류 → ls -l / chmod 644 안내 + 기본 퀴즈 10개
```

백업에서 복구하면 `♻️ 백업 파일(state.json.bak)에서 복구했습니다.`를 출력하고 즉시 `state.json`을 다시 저장합니다. 손상 파일을 바로 지우지 않고 `.corrupt`로 남기는 이유는 원인을 확인하거나 직접 고쳐서 살릴 수 있게 하기 위해서입니다.

### 수동 복구 방법

```bash
# 백업으로 되돌리기 (현재 파일을 버리고 직전 저장본 사용)
cp state.json.bak state.json

# 손상 파일을 직접 고쳐서 살리기
python3 -m json.tool state.json.corrupt     # JSON 오류 위치 확인
mv state.json.corrupt state.json            # 수정 후 되돌리기

# 완전히 초기화 (기본 퀴즈로 시작)
rm state.json state.json.bak
```

### 복구 테스트 결과

```bash
python3 main.py                     # 실행 후 5번 종료 → state.json, state.json.bak 생성
echo "망가진 파일" > state.json      # 일부러 손상
python3 main.py
```

```
⚠️ 저장 파일이 손상되었습니다. 손상된 파일은 state.json.corrupt로 보관합니다.
♻️ 백업 파일(state.json.bak)에서 복구했습니다. (퀴즈 11개)
```

### 한계

백업은 **직전 1세대만** 보관합니다. 잘못된 퀴즈를 추가하고 두 번 이상 저장하면 그 이전 상태로는 돌아갈 수 없습니다. 필요하면 `state_YYYYMMDD_HHMMSS.json`처럼 날짜별로 여러 개를 남기고 오래된 것부터 지우는 방식으로 확장할 수 있습니다.

---

## 15. 유지보수 가이드 (요구 변경 시 수정 위치)

| 요구 변경 | 수정할 곳 | 함께 확인할 곳 |
|---|---|---|
| **점수 계산 방식** (예: 100점 → 정답 수, 감점제) | `QuizGame.calculate_score()` 한 곳 | `read_state()`의 점수 범위 검사(0~100) |
| **Quiz 필드 추가** (예: 카테고리, 해설) | `Quiz.__init__`, `to_dict`, `from_dict` | `quiz_data.py` 기본 문제, `add_quiz()` 입력, `display()` 출력 |
| **선택지 개수 변경** (4개 → 5개) | `Quiz.from_dict`의 개수 검사, `add_quiz()`의 `range(1, 5)` | `play()`·`add_quiz()`의 `get_number(..., 1, 4)` |
| **저장 위치·파일 이름** | `quiz_game.py` 상단의 `STATE_FILE`, `BACKUP_FILE` 등 상수 | `.gitignore` |
| **저장 형식** (JSON → SQLite 등) | `QuizGame.save()`, `load()`, `read_state()` | 나머지 메서드는 `self.quizzes`만 쓰므로 수정 불필요 |
| **기존 state.json 형식 호환** | `Quiz.from_dict` (새 필드는 `data.get("필드", 기본값)`으로 읽기) | 예전 파일이 손상으로 판정되지 않는지 테스트 |
| **메뉴 추가** (예: 퀴즈 삭제) | `show_menu()` 출력, `run()`의 분기와 `get_number(..., 1, 5)` 범위 | 데이터가 바뀌는 기능이면 `self.save()` 호출 |
| **입력 규칙** (빈 입력, 숫자 범위) | `get_number()`, `get_text()` | — |
| **기본 퀴즈 문제** | `quiz_data.py`의 `get_default_quizzes()` | — |
| **종료 처리** (Ctrl+C 등) | `main.py`의 `try`/`except` | — |

변경한 뒤에는 아래 항목을 확인합니다.

1. `python3 main.py`로 메뉴 1~5번을 모두 실행
2. 종료 후 다시 실행해서 데이터가 유지되는지 확인
3. `echo "broken" > state.json` 후 실행해서 백업 복구가 되는지 확인
4. 저장 형식을 바꿨다면 `python3 tools/benchmark.py`로 성능 재측정