import pytest
from unittest.mock import AsyncMock, patch
from app.services.github import get_pr_diff, post_pr_comment

@pytest.mark.asyncio
async def test_get_pr_diff():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.text = "diff content here"
        result = await get_pr_diff("repo/test", 1, "fake_token")
        assert result == "diff content here"

@pytest.mark.asyncio
async def test_post_pr_comment():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = AsyncMock()
        mock_response.json = lambda: {"id": 123}
        mock_post.return_value = mock_response
        result = await post_pr_comment("repo/test", 1, "comment", "fake_token")
        assert result == {"id": 123}