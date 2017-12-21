import Script_reader
import pytest

'''def test_return_page_numbers_and_distance():
    ls = ["", "1", "",'A STUDY IN PINK', '', 'SHOOTING SCRIPT - GREEN AMENDED', '', '18/04/10', '', 'Screen snows and -A blizzard of cuts round various news reports, fast, just', 'snatched words and phrases -NEWSEADER', '-- Afghanistan -ITN NEWSREADER', '-- British troops involved in a -SKY NEWSREADER', '-- four dead, two injured -Video phone: chaotic, accidental footage, just the camera', 'still running - a dirt road, a crashed jeep belching smoke,', 'gunfire, soldiers running. We hear a voice yelling -Watson!!', '', 'MAN', '', 'News reports -BBC NEWSREADER', '-- increased hostilities over the', 'last few weeks -SKY NEWSREADER', '-- until relatives have been', 'informed -Video phone -Watson!!', '', 'MAN', '', 'News reports -ITN NEWSREADER', '-- two more have died in the worst', 'outbreak of violence -SKY NEWSREADER', '-- said his thoughts were with the', 'victims families -Video phone -Watson!!', '', 'MAN', '', 'And on that we cut to:', '1', '', 'INT. JOHN\xe2\x80\x99S BEDSIT - NIGHT', '', '1', '', 'Close on a pair of eyes snapping open.', 'Wider:', '', '1.', '', '\x0cA STUDY IN PINK', '', 'SHOOTING SCRIPT - GREEN AMENDED', '', '18/04/10', '', 'A man, startling awake, sweating in his bed. A single bed in', 'the dullest, plainest room. He sits up, calming himself,', 'letting his breathing return to normal.', 'Dr. John Watson. Early thirties, thickset, weathered.', 'Something slightly dazed and pained in his eyes. He\xe2\x80\x99s been', 'through hard times, seen bad things.', 'Looks around the room. A bare minimum of personal', 'possessions, neatly folded clothes.', 'The opposite wall.', '', 'Leaning by the door, a walking cane.', '', 'Close on John, looking at it - frowns.', '2', '', 'Fierce, resentful.', '', 'INT. JOHN\xe2\x80\x99S BEDSIT - DAY', '', '2', '', 'Later - first light. Close on a coffee cup as it is set down', 'on the desk. Panning down the desk drawer as John pulls it', 'open, removes a laptop computer --- revealing something else in the drawer. A hand gun', '(whatever gun John would\xe2\x80\x99ve had in Afghanistan.)', 'John\xe2\x80\x99s look holds on the gun for a moment, like it\xe2\x80\x99s a', 'curious temptation to him --- then he firmly closes the drawer.', 'The lap top computer open at:', 'A blog page.', '', 'Closer on the Page Title:', '', 'The Personal Blog Of Dr. John H. Watson --- panning down the screen to an empty page.', 'winking away, expectant.', '', 'The cursor', '', 'We roll focus to see John\xe2\x80\x99s face, reflected.', 'effort of concentration.', '', 'Frowning.', '', 'An', '', 'ELLA', '(V.O.)', 'How\xe2\x80\x99s your blog going?', '3', '', 'INT. THERAPIST\xe2\x80\x99S CONSULTING ROOM - DAY (11.00 AM)', '', '3', '', 'Ella - a therapist - sitting opposite John Watson, her', 'notepad out.', 'John sits stiffly in his chair.', 'embarrassed.', 'Oh, fine.', '', 'JOHN', 'Good.', '', 'Out of place.', '', 'A little', '', 'Very good.', '', 'Ella looks at him, knowingly.', '', '2.', '', '\x0cA STUDY IN PINK', '', 'SHOOTING SCRIPT - GREEN AMENDED', '', '18/04/10', '', 'ELLA']
    assert Script_reader.return_page_numbers_and_distance(ls) == ["1.", 45]

def test_distance_calculator():
    ls = ["", "1", "",'A STUDY IN PINK', '', 'SHOOTING SCRIPT - GREEN AMENDED', '', '18/04/10', '', 'Screen snows and -A blizzard of cuts round various news reports, fast, just', 'snatched words and phrases -NEWSEADER', '-- Afghanistan -ITN NEWSREADER', '-- British troops involved in a -SKY NEWSREADER', '-- four dead, two injured -Video phone: chaotic, accidental footage, just the camera', 'still running - a dirt road, a crashed jeep belching smoke,', 'gunfire, soldiers running. We hear a voice yelling -Watson!!', '', 'MAN', '', 'News reports -BBC NEWSREADER', '-- increased hostilities over the', 'last few weeks -SKY NEWSREADER', '-- until relatives have been', 'informed -Video phone -Watson!!', '', 'MAN', '', 'News reports -ITN NEWSREADER', '-- two more have died in the worst', 'outbreak of violence -SKY NEWSREADER', '-- said his thoughts were with the', 'victims families -Video phone -Watson!!', '', 'MAN', '', 'And on that we cut to:', '1', '', 'INT. JOHN\xe2\x80\x99S BEDSIT - NIGHT', '', '1', '', 'Close on a pair of eyes snapping open.', 'Wider:', '', '1.', '', '\x0cA STUDY IN PINK', '', 'SHOOTING SCRIPT - GREEN AMENDED', '', '18/04/10', '', 'A man, startling awake, sweating in his bed. A single bed in', 'the dullest, plainest room. He sits up, calming himself,', 'letting his breathing return to normal.', 'Dr. John Watson. Early thirties, thickset, weathered.', 'Something slightly dazed and pained in his eyes. He\xe2\x80\x99s been', 'through hard times, seen bad things.', 'Looks around the room. A bare minimum of personal', 'possessions, neatly folded clothes.', 'The opposite wall.', '', 'Leaning by the door, a walking cane.', '', 'Close on John, looking at it - frowns.', '2', '', 'Fierce, resentful.', '', 'INT. JOHN\xe2\x80\x99S BEDSIT - DAY', '', '2', '', 'Later - first light. Close on a coffee cup as it is set down', 'on the desk. Panning down the desk drawer as John pulls it', 'open, removes a laptop computer --- revealing something else in the drawer. A hand gun', '(whatever gun John would\xe2\x80\x99ve had in Afghanistan.)', 'John\xe2\x80\x99s look holds on the gun for a moment, like it\xe2\x80\x99s a', 'curious temptation to him --- then he firmly closes the drawer.', 'The lap top computer open at:', 'A blog page.', '', 'Closer on the Page Title:', '', 'The Personal Blog Of Dr. John H. Watson --- panning down the screen to an empty page.', 'winking away, expectant.', '', 'The cursor', '', 'We roll focus to see John\xe2\x80\x99s face, reflected.', 'effort of concentration.', '', 'Frowning.', '', 'An', '', 'ELLA', '(V.O.)', 'How\xe2\x80\x99s your blog going?', '3', '', 'INT. THERAPIST\xe2\x80\x99S CONSULTING ROOM - DAY (11.00 AM)', '', '3', '', 'Ella - a therapist - sitting opposite John Watson, her', 'notepad out.', 'John sits stiffly in his chair.', 'embarrassed.', 'Oh, fine.', '', 'JOHN', 'Good.', '', 'Out of place.', '', 'A little', '', 'Very good.', '', 'Ella looks at him, knowingly.', '', '2.', '', '\x0cA STUDY IN PINK', '', 'SHOOTING SCRIPT - GREEN AMENDED', '', '18/04/10', '', 'ELLA']
    assert Script_reader.distance_calculator(ls) == [45, 77]'''

def test_scene_number_two_anywhere_with_split_lists():
    ls1 = ['Alans sdfasdf,', "34", 'dongalsdafd fasdf asdf asdf dogo', ' asdfasd fasd fasdf asdf asdf','xx', 'sfdasdfa 34', 'zxcvbzxcvzxcvxzcb  cvzxcvzxcv', 'zxcvzxcbzxcb']
    ls2 = ['Alans sdfasdf, 34', 'dongalsdafd fasdf asdf asdf dogo', ' asdfasd fasd fasdf asdf asdf','xx', 'sfdasdfa', '34', 'zxcvbzxcvzxcvxzcb  cvzxcvzxcv', 'zxcvzxcbzxcb']
    assert Script_reader.scene_number_two_anywhere_with_split_lists(ls1) == '34'
    assert Script_reader.scene_number_two_anywhere_with_split_lists(ls2) == '34'

def test_deleted_scene_detector():
    str1 = 'OMITTED'
    str2 = '***SCENE DELETED ***'
    assert Script_reader.deleted_scene_detector(str1) == ['***NA***', '***OMITTED***','***NA***']
    assert Script_reader.deleted_scene_detector(str2) == ['***NA***', '***OMITTED***','***NA***']

def test_split_text_returner_in_reverse():
    str1 = 'EXT. DAY. BY THE MOUNDS.'
    assert Script_reader.split_text_returner_in_reverse(str1, 'EXT.') == ['EXT.', 'BY THE MOUNDS', 'DAY']

def test_text_splitter():
    str1 = 'EXT. DAY. BY THE MOUNDS.'
    str2 = 'INT. KITCHEN, EILISS HOUSE. NIGHT'
    str3 = 'A sort of ethereal - glowing INT. FUNCTION ROOM. DAY'
    str4 = 'INT. THERAPISTS CONSULTING ROOM - DAY (11.00 AM)'
    str5 = 'EXT. GARRISON PUB, GARRISON LANE - DAY 1 - 18:45'
    str6 = 'FLASHBACK - EXT. CHARLIES YARD - NIGHT X - 22:00'
    str7 = 'INT. DINING ROOM, MRS. KEHOES HOUSE. EVENING.'
    assert Script_reader.text_splitter(str1) == ['EXT.', 'BY THE MOUNDS', 'DAY']
    assert Script_reader.text_splitter(str2) == ['INT.', "KITCHEN, EILISS HOUSE", 'NIGHT']
    assert Script_reader.text_splitter(str3) == ['INT.', 'FUNCTION ROOM', 'DAY']
    assert Script_reader.text_splitter(str4) == ['INT.', 'THERAPISTS CONSULTING ROOM', 'DAY (11.00 AM)']
    assert Script_reader.text_splitter(str5) == ['EXT.', 'GARRISON PUB, GARRISON LANE', 'DAY 1 - 18:45']
    assert Script_reader.text_splitter(str6) == ['EXT.', "CHARLIES YARD", 'NIGHT X - 22:00']
    assert Script_reader.text_splitter(str7) == ['INT.', 'DINING ROOM, MRS. KEHOES HOUSE', 'EVENING']

def test_text_stripper():
    str1 = 'Hello'
    str2 = '17'
    str3 = 17
    str4 = 'JESS'
    str5 = '27JHA'
    str6 = '35JA'
    str7 = '29A'
    assert Script_reader.text_stripper(str1) == None
    assert Script_reader.text_stripper(str2) == '17'
    assert Script_reader.text_stripper(str3) == '17'
    assert Script_reader.text_stripper(str4) == None
    assert Script_reader.text_stripper(str5) == None
    assert Script_reader.text_stripper(str6) == None
    assert Script_reader.text_stripper(str7) == '29A'

def test_pattern_finder():
    ls1 = ['', '2', '', 'Basil Brown rides up to a large country house on his bicycle.', 'He is in his early fifties; workingman\xe2\x80\x99s suit, cloth cap,', 'gold watch chain; a Suffolk man through and through. An air', 'of solidity and containment.', 'He parks the bike on its stand and knocks on the imposing', 'door. John Grateley, the butler opens it. He clocks Basil\xe2\x80\x99s', 'suit, boots and bike.', 'BROWN']
    ls2 = ['It is pronounced Praetty.', '', 'BROWN', 'Mrs Praetty. If you\xe2\x80\x99d be so kind.', '', 'Grateley closes the door without inviting Brown in.', 'gardens. She\xe2\x80\x99s in her forties; lace, tweed and cashmere. A', 'delicacy that belies an inner strength.', 'BROWN', 'Did you have many replies to your', 'advertisement?', '', 'Sc', 're', '', '3', '', 'EDITH']
    ls3 = ['EXT. DAY. THE GARDENS.', '', 'en', '', 'Edith Pretty is walking with Brown through her well-tended']
    assert Script_reader.pattern_finder(ls1) == '2'
    assert Script_reader.pattern_finder(ls2) == '3'
    assert Script_reader.pattern_finder(ls3) == 'en'
