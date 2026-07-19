from fly.services.git import Git


def test_is_respository():
    assert Git.is_repository() is True
