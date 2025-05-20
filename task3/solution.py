def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals["lesson"]

    def process_intervals(raw_intervals: list[int]) -> list[tuple[int, int]]:
        # Разбиваем на пары начало-конец
        it = iter(raw_intervals)
        intervals_list = list(zip(it, it))

        if not intervals_list:
            return []

        intervals_list.sort()

        # Объединяем интервалы
        merged = [intervals_list[0]]
        for current in intervals_list[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                merged[-1] = last[0], max(last[1], current[1])
            else:
                merged.append(current)

        # Обрезаем интервалы по границам урока
        result = []
        for start, end in merged:
            start = max(start, lesson_start)
            end = min(end, lesson_end)
            if start < end:
                result.append((start, end))
        return result

    pupil_intervals = process_intervals(intervals["pupil"])
    tutor_intervals = process_intervals(intervals["tutor"])

    # Находим пересечения интервалов pupil и tutor
    total_time = 0
    i = j = 0
    while i < len(pupil_intervals) and j < len(tutor_intervals):
        pupil_start, pupil_end = pupil_intervals[i]
        tutor_start, tutor_end = tutor_intervals[j]

        # Находим пересечение текущих интервалов
        start = max(pupil_start, tutor_start)
        end = min(pupil_end, tutor_end)
        if start < end:
            total_time += end - start

        # Переходим к следующему интервалу
        if pupil_end < tutor_end:
            i += 1
        else:
            j += 1

    return total_time
