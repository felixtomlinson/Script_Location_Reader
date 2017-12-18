import pytest
import re
import models


@pytest.fixture
def test_script():
    import models
    return models.Script('Brooklyn-Shooting-Script.pdf')


def test_scene_number_in_regex(test_script):
    r = re.compile('\d{1,5}')
    text_as_string = ''.join(test_script.text)
    nums = r.findall(text_as_string)
    for i in range(1, 153):
        assert str(i) in nums


def test_scene_number_text(test_script):
    r = re.compile('^\d{1, 4}$')
    nums = r.findall(test_script.raw_text)
    indices = re.finditer(r, test_script.raw_text)


