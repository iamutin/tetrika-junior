from task3.solution import appearance


def test_appearance(test_case):
    intervals = test_case["intervals"]
    expected_answer = test_case["answer"]
    result = appearance(intervals)
    assert (
        result == expected_answer
    ), f"Ожидаемый ответ: {expected_answer}, полученный ответ: {result}"
