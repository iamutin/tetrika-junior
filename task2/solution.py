import asyncio
import csv
import logging
from collections import defaultdict
from typing import Any

from aiohttp import ClientError, ClientSession

RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SET = set(RUSSIAN_ALPHABET)

BASE_URL = "https://ru.wikipedia.org/w/api.php"
PARAMS = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": "Категория:Животные по алфавиту",
    "cmtype": "subcat|page",
    "cmlimit": "max",
    "format": "json",
}

REQUEST_TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


async def fetch_data(
    session: ClientSession,
    parameters: dict[str, str],
    continuation_params: dict[str, str] | None,
) -> dict[str, Any]:
    """
     Получаем страницу из Википедии.

    :param session: HTTP сессия
    :param parameters: Параметры запроса
    :param continuation_params: Продолжающие параметры (для пагинации)
    :return: JSON объект с результатом запроса
    """
    if continuation_params:
        parameters.update(continuation_params)

    try:
        async with session.get(
            BASE_URL,
            params=parameters,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            response.raise_for_status()
            return await response.json()
    except ClientError as e:
        logger.error("Ошибка при выполнении запроса: %s", str(e))
        raise


async def count_animals_by_first_letter(session: ClientSession) -> dict[str, int]:
    """
    Подсчет количества животных по первой букве имени.

    :param session: HTTP сессия
    :return: Словарь вида {'буква': количество животных}
    """
    letter_counters: dict[str, int] = defaultdict(int)
    continuation_params: dict = {}

    while True:
        logger.info("Получение данных...")

        try:
            response = await fetch_data(session, PARAMS.copy(), continuation_params)
        except Exception:
            break

        for animal in response["query"]["categorymembers"]:
            title = animal["title"].strip()
            first_char = title[0].upper()
            if first_char in ALPHABET_SET:
                letter_counters[first_char] += 1

            if title == "Aaaaba":
                return letter_counters

        if "continue" in response:
            continuation_params = response["continue"]
        else:
            break

    return letter_counters


def save_to_csv(filename: str, results: dict[str, int]) -> None:
    """
    Сохраняет результаты подсчета в CSV файл.

    :param filename: Имя файла
    :param results: Результаты подсчёта
    """
    sorted_rows = sorted(
        results.items(), key=lambda pair: RUSSIAN_ALPHABET.index(pair[0])
    )

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(sorted_rows)
    except IOError as e:
        logger.error("Ошибка при сохранении файла: %s", e)
        raise
    else:
        logger.info("Данные успешно сохранены в %s.", filename)


async def main() -> None:
    output_filename = "beasts.csv"

    async with ClientSession() as session:
        result = await count_animals_by_first_letter(session)
        save_to_csv(output_filename, result)

    logger.info("Работа программы завершена.")


if __name__ == "__main__":
    asyncio.run(main())
