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
        print(pair[0].group(0), pair[1].group(0))
        if pair[0].group(0) == pair[1].group(0):
            indexes[scene_number] = (pair[0].start()+len(pair[0].group(0)), pair[1].start())
            scene_number += 1
    return indexes


def extract_between_scene_indices(text, indices):
    """This function returns the text between two indices"""
    return text[indices[0]:indices[1]]


def find_upper_case_words(text_with_extra):
    """This function strips out line breaks and returns the upper-cased text from a given text"""
    upper_regex = re.compile('[^\n]*')
    output = set(upper_regex.findall(text_with_extra))
    output.remove('')
    return output.pop()


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
    find_scene_number_indices(script.text)
