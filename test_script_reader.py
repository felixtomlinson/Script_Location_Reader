import pytest
import re
import models
import testing_ground


@pytest.fixture

def test_script():
    import models
    return models.Script('Sherlock-A-Study-in-Pink-final-shooting-script.pdf')


def test_find_scene_indices(test_script):
    assert testing_ground.find_scene_number_indices(test_script.text).get(1) == (832, 862)


def test_extract_between_scene_indices(test_script):
    t = testing_ground.find_scene_number_indices(test_script.text)[1]
    assert "\n\nINT. JOHN’S BEDSIT - NIGHT\n\n" == testing_ground.extract_between_scene_indices(test_script.text, t)


def test_find_useful_text(test_script):
    t = testing_ground.find_scene_number_indices(test_script.text)[1]
    assert "INT. JOHN’S BEDSIT - NIGHT" == testing_ground.find_upper_case_words(
        testing_ground.extract_between_scene_indices(test_script.text, t))

