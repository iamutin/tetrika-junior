from unittest.mock import AsyncMock, MagicMock

import pytest

from task2.solution import BASE_URL, REQUEST_TIMEOUT, fetch_data


@pytest.fixture
def mock_response():
    return {
        "query": {
            "categorymembers": [
                {"title": "Аист"},
                {"title": "Акула"},
                {"title": "Бабочка"},
                {"title": "Бегемот"},
                {"title": "Волк"},
            ]
        }
    }


@pytest.mark.asyncio
async def test_fetch_data_success(mock_response):
    mock_response_obj = MagicMock()
    mock_response_obj.json = AsyncMock(return_value=mock_response)
    mock_response_obj.raise_for_status = MagicMock()

    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__ = AsyncMock(return_value=mock_response_obj)
    mock_context_manager.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.get.return_value = mock_context_manager

    params = {"action": "query"}
    result = await fetch_data(mock_session, params, None)

    mock_response_obj.raise_for_status()

    assert result == mock_response
    mock_session.get.assert_called_once_with(
        BASE_URL,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )
