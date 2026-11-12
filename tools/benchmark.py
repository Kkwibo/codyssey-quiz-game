"""퀴즈 개수에 따른 state.json 저장/불러오기 시간, 파일 크기, 메모리 사용량을 측정한다.

실행: python3 tools/benchmark.py
실제 state.json은 건드리지 않고 임시 폴더에서만 측정한다.
"""

import json
import sys
import tempfile
import time
import tracemalloc
from pathlib import Path

# 프로젝트 루트의 quiz.py를 불러오기 위한 경로 설정
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from quiz import Quiz  # noqa: E402


def make_quizzes(count):
    """측정용 퀴즈를 count개 만든다. (문제 약 30자, 선택지 4개)"""
    return [
        Quiz(
            f"{i}번 문제: 실행 중인 web 컨테이너에 bash로 접속하는 명령은?",
            ["docker exec -it web bash", "docker bash web", "docker exec -it web", "docker run -it web bash"],
            i % 4 + 1,
        )
        for i in range(1, count + 1)
    ]


def measure(count):
    """count개 퀴즈에 대해 저장·불러오기·검색 시간과 크기를 측정해 dict로 돌려준다."""
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "state.json"

        tracemalloc.start()
        quizzes = make_quizzes(count)
        memory = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()

        start = time.perf_counter()
        data = {"quizzes": [quiz.to_dict() for quiz in quizzes], "best_score": 80}
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        save_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        with open(path, "r", encoding="utf-8") as file:
            loaded = [Quiz.from_dict(item) for item in json.load(file)["quizzes"]]
        load_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        keyword = f"{count}번 문제"
        found = [quiz for quiz in loaded if keyword in quiz.question]
        search_ms = (time.perf_counter() - start) * 1000

        return {
            "count": count,
            "size_kb": path.stat().st_size / 1024,
            "memory_kb": memory / 1024,
            "save_ms": save_ms,
            "load_ms": load_ms,
            "search_ms": search_ms,
            "found": len(found),
        }


def main():
    print(f"{'퀴즈 수':>8} | {'파일 크기':>10} | {'메모리':>10} | {'저장':>9} | {'불러오기':>9} | {'검색':>8}")
    print("-" * 72)
    for count in (10, 1_000, 10_000, 100_000):
        r = measure(count)
        print(
            f"{r['count']:>8,} | {r['size_kb']:>8.1f}KB | {r['memory_kb']:>8.1f}KB | "
            f"{r['save_ms']:>7.1f}ms | {r['load_ms']:>7.1f}ms | {r['search_ms']:>6.2f}ms"
        )


if __name__ == "__main__":
    main()