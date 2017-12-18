import re, models, itertools


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def find_scene_number_indices(text_to_search):
    number_regex = re.compile('\d{1,4}')
    indices = re.finditer(number_regex, text_to_search)
    indexes = {}
    pairs = pairwise(indices)
    scene_number = 1
    for pair in pairs:
        if pair[0].group(0) == pair[1].group(0):
            indexes[scene_number] = (pair[0].start()+len(pair[0].group(0)), pair[1].start())
            scene_number += 1
    return indexes


def find_upper_case_words(text_with_extra):
    upper_regex = re.compile('[A-Z][A-Z]*')
    print(upper_regex.findall(text_with_extra))


def remove_non_upper_case(text_with_extra):
    upper_regex = re.compile('([A-Z]+)')
    return upper_regex.findall(text_with_extra)


def check_if_string_starts_with_int_or_ext(string_to_check):
    int_or_ext = re.compile('^(INT|EXT)')
    return bool(re.search(int_or_ext, string_to_check))


def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r


a = models.Script('Sherlock-A-Study-in-Pink-final-shooting-script.pdf')
b = models.Script('Brooklyn-Shooting-Script.pdf')
scripts = [a, b]
for script in scripts:
    scene_info = find_scene_number_indices(a.raw_text)
    scenes = {}
    for key, value in scene_info.items():
        scenes[key] = remove_non_upper_case(a.raw_text[value[0]:value[1]])
    inside_or_out = re.compile("(EXT|INT)")
    for key, value in scenes.items():
        if not inside_or_out.match(' '.join(value)):
            scenes = remove_key(scenes, key)
    counter = 0
    for key, value in scenes.items():
        print(counter, value[0], ' '.join(value[1:-1]), value[-1])
        counter += 1
