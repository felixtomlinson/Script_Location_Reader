import pytest
import re


@pytest.fixture
def test_script():
    import models
    return models.Script('A-Long-Way-Down-Shooting-Script.pdf')


def test_given_longWayDown_returns_author_as_9th_item_in_list(test_script):
    assert test_script.text[8] == 'Written by Jack Thorne'


def test_scene_number_in_regex(test_script):
    r = re.compile('\d')
    text_as_string = ''.join(test_script.text)
    nums = r.findall(text_as_string)
    assert '1' in nums