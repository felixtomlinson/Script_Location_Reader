# -*- coding: utf-8 -*-

import os
import textract
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from prettytable import PrettyTable
from Location_database import add_to_Scripts_DB
from Location_database import add_to_LocationsInfo_DB
import csv


def main():
    print (table_creator('celesteandjesseforever_screenplay.pdf'))
    # print(table_creator('Sherlock-A-Study-in-Pink-final-shooting-script.pdf'))
    # print(table_creator('Peaky-Blinders-S1-Ep1.pdf'))
    # print(table_creator('Brooklyn-Shooting-Script.pdf'))
    # print(table_creator('A-Long-Way-Down-Shooting-Script.pdf'))
    pass


def document_reader(file_name):
    '''Uses textract to read and return the text of files, split them into
    different lines and return the whole thing as a list object'''
    # add_to_Scripts_DB(os.path.splitext(file_name)[0])
    text = textract.process(file_name).decode('utf-8')
    text = text.splitlines()
    return text


def split_text_without_time_of_day(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out):
    '''Returns internal or external and location type from important text when
    there is no given time of day.'''
    location_type = important_text_without_inside_or_out[end_of_inside_or_out+1:]
    time_of_day = 'NA'
    return [inside_or_out, location_type, time_of_day]


def split_text_returner(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out):
    '''When there are standard times of the day contained in the Time of Day
    column this function searches for them and then returns the type of
    location and the time of day using the location of the times of day
    as a reference point. If there is no time of day this returns time of day
    as NA and the location type'''
    times_in_the_day = ['DAY', 'NIGHT', 'EVENING','DUSK', 'PRE-DAWN', 'BEFORE DAWN',
    'DAWN', 'MORNING', 'SUNSET', 'SUNRISE', 'Sundown', 'LATE AFTERNOON',
    'AFTERNOON', 'MINUTES LATER', 'MOMENTS LATER', 'LATER', 'SAME']
    #There is a potential bug here.
    #If for example morning were before day and you had the string
    # 'INT. DAY. MORNING ROOM.' you'd get a truely weird result.
    #Should it rather be if it contains one of these things then do this stuff
    # rather that for these things do all these tests and see if it contains them
    for times in times_in_the_day:
        start_of_time_of_day = important_text_without_inside_or_out.find(times)
        if start_of_time_of_day != -1:
            end_of_location_type = start_of_time_of_day
            if important_text_without_inside_or_out[start_of_time_of_day-1] == ' ':
                end_of_location_type = start_of_time_of_day - 1
            if important_text_without_inside_or_out[start_of_time_of_day-2] == '-':
                end_of_location_type = start_of_time_of_day - 3
            location_type = important_text_without_inside_or_out[end_of_inside_or_out+1:end_of_location_type]
            if location_type != '':
                if location_type[-1] == '.':
                    location_type = location_type[:-1]
            time_of_day = important_text_without_inside_or_out[start_of_time_of_day:]
            return [inside_or_out, location_type, time_of_day]
    return split_text_without_time_of_day(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out)


def split_text_returner_in_reverse(important_text_without_inside_or_out, inside_or_out):
    '''Carries out the same function as split_text_returner but when the order
    of the important text goes internal or external, time of day, location
    type.'''
    end_of_inside_or_out = len(inside_or_out) + 1
    times_in_the_day = ['DAY', 'NIGHT', 'EVENING','DUSK', 'PRE-DAWN', 'BEFORE DAWN',
    'DAWN', 'MORNING', 'SUNSET', 'SUNRISE', 'Sundown', 'LATE AFTERNOON',
    'AFTERNOON', 'MINUTES LATER', 'MOMENTS LATER', 'LATER', 'SAME']
    for times in times_in_the_day:
        start_of_time_of_day = important_text_without_inside_or_out.find(times)
        if important_text_without_inside_or_out.find('- ') != -1:
            end_of_time_of_day = important_text_without_inside_or_out.find('- ')
        if important_text_without_inside_or_out.rfind('.') != -1:
            important_text_without_inside_or_out = important_text_without_inside_or_out[end_of_inside_or_out:]
            end_of_time_of_day = important_text_without_inside_or_out.find('.') + 1
        if start_of_time_of_day != -1:
            location_type = important_text_without_inside_or_out[end_of_time_of_day + 1:]
            if location_type[-1] == '.':
                location_type = location_type[:-1]
            time_of_day = times
            return [inside_or_out, location_type, time_of_day]
    return split_text_without_time_of_day(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out)

def text_splitter (important_text):
    '''Splits the various important parts of the text out into a list.
    The important parts for this tool are: if the location is inside or
    outside, the location details and what time of day the actions
    is happening at'''
    inside_or_out_or_both = ['INT./EXT.', 'INT.', 'EXT.', 'C/U.']
    for category in inside_or_out_or_both:
        start_of_inside_or_out = important_text.find(category)
        if start_of_inside_or_out != -1:
            if important_text[-1] == '.':
                important_text = important_text[:-1]
            important_text = important_text[start_of_inside_or_out:]
            end_of_inside_or_out = len(category)
            split_text = split_text_returner(important_text, end_of_inside_or_out, category)
            if split_text == None:
                return split_text
            if split_text[1] == '':
                split_text = split_text_returner_in_reverse(important_text, category)
            return split_text


def deleted_scene_detector(important_text):
    #Make the over black issue it's own function
    '''If a scene is labelled as omitted or scene delted this will produce a
    list to be inputted into the table which shows the user that the scene is
    no longer being used.'''
    omitted = ['OMITTED', 'SCENE DELETED']
    over_black = 'OVER BLACK'
    for name in omitted:
        omitted_or_not = important_text.find(name)
        over_black_or_not = important_text.find(over_black)
        if omitted_or_not != -1:
            return ['***NA***', '***OMITTED***','***NA***']
        if over_black_or_not != -1:
            return ['***NA***', 'OVER BLACK','***NA***']


def important_text_compiler(list_of_strings, string, index):
    '''If the important text is split up by split lines due to how the
    PDF is formatted this function recompiles it into a single string so that
    it can be read and the text split into useful categories'''
    inside_or_out_or_both = ['INT./EXT.', 'INT.', 'EXT.']
    for category in inside_or_out_or_both:
        if category == string:
            next_string = index + 2
            new_string = string + " " + list_of_strings[next_string]
            return new_string
    return string


def rough_scene_checker(script_as_list, index, which_side):
    '''Checks to see if there are any short strings in close proximity to
    the important text'''
    if len(script_as_list[index + 2 * which_side]) <= 5:
        if len (script_as_list[index + 2 * which_side]) > 0:
            if not '.' in script_as_list[index + 2 * which_side]:
                scene_number = script_as_list[index + 2 * which_side]
                if count_letters(scene_number) < 2:
                    return scene_number


def count_letters(potential_scene_number):
    '''Counts the number of letters in a potential scene number, if the
    potential scene number is just a single letter or if it returns a
    UnicodeEncodeError then the function returns 3.'''
    try:
        potential_scene_number = str(potential_scene_number)
        potential_scene_number = potential_scene_number.upper()
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ*!'
        count = 0
        for letter in letters:
            if letter in potential_scene_number:
                count += potential_scene_number.count(letter)
            if potential_scene_number == letter:
                count = 3
        return count
    except UnicodeEncodeError as e:
        count = 3
        return count


def potential_scene_number_returner(potential_scene_number):
    '''If count letters retuns less than two this returns the potential scene
    number. If it returns two or more then it returns nothing.'''
    count = count_letters(potential_scene_number)
    if count < 2:
        return potential_scene_number

def potential_scene_number_compiler(script_as_list):
    '''Iterates through the script as a list and checks each string in the list
    to see if it is a potential scene number. It firsts checks that they are
    relatively short and then if they have more than two letters in them. If
    they are both short and contain few letters then it adds them to a list of
    probable scene numbers.'''
    potential_strings_within_range = []
    for potential_scene_number in script_as_list:
        if len(potential_scene_number) <= 9:
            if len (potential_scene_number) > 0:
                potential_scene_number = potential_scene_number_returner(potential_scene_number)
                if potential_scene_number != None:
                    potential_strings_within_range.append(potential_scene_number)
    return potential_strings_within_range


def scene_number_one_on_each_side(script_as_list):
    '''Finds potential scene numbers in the text, split by lines,
    before and the text after the important text. It returns a number
    if it appears both before and after the text.'''
    upper_range_number = potential_scene_number_compiler(script_as_list[1])
    lower_range_number = potential_scene_number_compiler(script_as_list[0])
    if bool(set(upper_range_number) & set(lower_range_number)):
        #Simplify this to remove for loops. Just printing the set will return the right number nearly all the time
        for numbers in upper_range_number:
            upper_number = numbers
            for scene_numbers in lower_range_number:
                if scene_numbers == upper_number:
                    return scene_numbers


def scene_number_two_anywhere(script_as_list):
    '''Finds potential scene numbers in the text, split by lines, around
    the important text.It returns a number if it appears twice in the text,
    split by lines.'''
    potential_number = potential_scene_number_compiler(script_as_list)
    for number in potential_number:
        number_of_occurences = potential_number.count(number)
        if number_of_occurences == 2:
            return number


def list_splitter(list_inputted):
    '''Splits a list of strings into a list of strings split by spaces'''
    list_of_long_strings = []
    for string in list_inputted:
        string = string.split()
        list_of_long_strings.extend(string)
    return list_of_long_strings


def scene_number_two_anywhere_with_split_lists(script_as_list):
    '''Finds potential scene numbers in the text, split by lines, around the
    important text. It returns a number if it appears twice in the text,
    split by spaces.'''
    potential_number = potential_scene_number_compiler(script_as_list)
    script_as_list = list_splitter(script_as_list)
    for number in potential_number:
        number_of_occurences = script_as_list.count(number)
        if number_of_occurences == 2:
            return number


def script_trimmer(script_as_list, index, search_range, search_type):
    '''Returns a list of the strings around the string that contain important
    information the length of the list can be determined by inputting a search
    range. If the list is returned in two halves or as one list is determined
    by search_type'''
    script_length = len(script_as_list)
    lower_index = index - search_range
    upper_index = index + search_range
    if lower_index < 0:
        lower_index = 0
    if upper_index > script_length:
        upper_index = script_length
    lower_half = script_as_list[lower_index:index]
    upper_half = script_as_list[index:upper_index]
    both_halves = script_as_list[lower_index:upper_index]
    if search_type == 'one_on_each_side':
        return [lower_half, upper_half]
    else:
        return both_halves


def pattern_finder (a_list):
    '''Iterates through script as a list and looks for patterns that might
    mean that a string is a scene number, it then checks to see if there are
    too many letters in the string and if not it retuns the string.'''
    for i, something in enumerate(a_list):
        try:
            if a_list[i + 1] == '':
                if a_list[i - 1] == '':
                    if len(something) <= 5:
                        if something.find('.') == -1:
                            if count_letters(something) < 2:
                                return something
        except IndexError as e:
            pass


def best_guesser(script_as_list, index, start, end, search_type):
    '''Given a range and a selected search type, this function selects a
    function to carry out a search and returns the number that it returns.'''
    for number in range(start, end):
        trimmed_script = script_trimmer(script_as_list, index, number, search_type)
        if search_type == 'one_on_each_side':
            scene_number = scene_number_one_on_each_side(trimmed_script)
        elif search_type == 'two_anywhere':
            scene_number = scene_number_two_anywhere(trimmed_script)
        elif search_type == 'split_script':
            scene_number = scene_number_two_anywhere_with_split_lists(trimmed_script)
        elif search_type == 'pattern_finder':
            scene_number = pattern_finder(trimmed_script)
        if scene_number != None:
            return scene_number


def scene_numbers_checker(script_as_list, index, a):
    '''This function holds the established hierarchy of the search types that
    work out what the scene number might be, it then provides the best guesser
    numbers at three regular intervals to search between.'''
    lowers = [a, a+6, a+10]
    uppers = [a+5, a+9, a+13]
    combined = zip(lowers,uppers)
    for i, j in combined:
        scene_number = best_guesser(script_as_list, index, i, j, 'one_on_each_side')
        if scene_number != None:
            return scene_number
        scene_number = best_guesser(script_as_list, index, i, j, 'two_anywhere')
        if scene_number != None:
            return scene_number
    for i, j in combined:
        scene_number = best_guesser(script_as_list, index, i, j, 'split_script')
        if scene_number != None:
            return scene_number
    for i, j in combined:
        scene_number = best_guesser(script_as_list, index, i, j, 'pattern_finder')
        if scene_number != None:
            return scene_number


def best_scene_number_checker(script_as_list, script_length, index):
    '''Checks to see if the scene number is in the position that they should
    be in, a single gap to the left and right on either side.'''
    if (index-2) > 0:
        if (index+2) < script_length:
            if script_as_list[index-2] == script_as_list[index+2]:
                if count_letters(script_as_list[index+2]) < 2:
                    return script_as_list[index+2]


def scene_numberer(script_as_list, index):
    '''Searches the area surrounding the key text to see if there are places
    where scene numbers that might be it then checks to see if they are
    anywhere else and returns those numbers if they are'''
    script_length = len(script_as_list)
    scene_number = best_scene_number_checker(script_as_list, script_length, index)
    if scene_number != None:
        return scene_number
    scene_number = scene_numbers_checker(script_as_list, index, 3)
    if scene_number != None:
        return scene_number
    scene_number = scene_numbers_checker(script_as_list, index, 14)
    if scene_number != None:
        return scene_number
    if index-1 > 0 and index+1 < script_length:
        if (script_as_list[index+1]) == '' or (script_as_list[index-1]) == '':
            scene_number = rough_scene_checker(script_as_list, index, 1)
            if scene_number == None:
                scene_number = rough_scene_checker(script_as_list, index, -1)
            if scene_number != None:
                return scene_number
    return ''


def add_normal_scene_info(script, lines, index, scriptname):
    '''This function checks to see if the line has important text in it,
    formats it, checks the scene number and then adds the formatted lines and
    the scene numbers together.'''
    formatted_lines = text_splitter(lines)
    if formatted_lines != None:
        if formatted_lines[1]=='':
            compiled_line = important_text_compiler(script, lines, index)
            formatted_lines = text_splitter(compiled_line)
        scene_number = [scene_numberer(script, index)]
        complete_line = scene_number + formatted_lines
        # add_to_LocationsInfo_DB(complete_line, os.path.splitext(scriptname)[0])
        return complete_line

def add_deleted_scene_info(script, lines, index, scriptname):
    '''This function checks to see if the line has text indicating a deleted
    scene in it, formats it, checks the scene number and then adds the
    formatted lines and the scene numbers together.'''
    deleted_lines = deleted_scene_detector(lines)
    if deleted_lines != None:
        lines = lines.split()
        script = script[:index-1] + lines + script[index+1:]
        scene_number = [scene_numberer(script, index)]
        complete_line = scene_number + deleted_lines
        # add_to_LocationsInfo_DB(complete_line, os.path.splitext(scriptname)[0])
        return complete_line


def table_creator(script):
    # Could use a list of script numbers, plus the index to work out the missing
    # ones (as long as we assume sequentialness, there are only gaps of size 1
    # and we have an if loops that adds As and Bs)
    '''This function takes the script as an input and uses the formatted_lines
    function to add all the locations together and turns it in into a table.'''
    scriptname = script
    script = document_reader(script)
    table = PrettyTable(['Scene Number', 'Internal or external',
    'Type of Location', 'Time of Day'])
    index = 0
    for lines in script:
        formatted_lines = add_normal_scene_info(script, lines, index, scriptname)
        if formatted_lines != None:
            table.add_row(formatted_lines)
        deleted_lines = add_deleted_scene_info(script, lines, index, scriptname)
        if deleted_lines != None:
            table.add_row(deleted_lines)
        index += 1
    return str(table)


def file_namer(file_name):
    '''Names the file as a CSV document with a useful description'''
    # return ('Location Information for '+ os.path.splitext(file_name)[0] + '.csv')
    return 'script_locs.csv'

def csv_creator(script):
    '''This function takes the script as an input and uses the formatted_lines
    function to add all the locations together and creates a CSV file.'''
    scriptname = script
    file_name = file_namer(script)
    csv_file = open(file_name, "w")
    script_csv = csv.writer(csv_file)
    script_csv.writerow(['Scene Number', 'Internal or external',
    'Type of Location', 'Time of Day'])
    script = document_reader(script)
    index = 0
    for lines in script:
        formatted_lines = add_normal_scene_info(script, lines, index, scriptname)
        if formatted_lines != None:
            formatted_lines[2] = formatted_lines[2].encode('utf-8')
            script_csv.writerow(formatted_lines)
        deleted_lines = add_deleted_scene_info(script, lines, index, scriptname)
        if deleted_lines != None:
            script_csv.writerow(deleted_lines)
        index += 1
    csv_file.close


def csv_remover(script):
    '''Removes the file created by csv_creator'''
    file_name = file_namer(script)
    os.remove(file_name)


def locations_emailer(script, email_address):
    '''Sends the user an email with a CSV file with their location information
    attached'''
    file_name = file_namer(script)
    fromaddr = "script.location.reader@gmail.com"
    password = open('emailpasswordsetting.txt',"r")
    password = password.read()
    msg = MIMEMultipart()
    msg['From'] = 'Script Location Reader'
    msg['To'] = email_address
    msg['Subject'] = os.path.splitext(file_name)[0]
    body = "Thank you very much for using our Script Location Reader \
    service.\n\n The location information for " + os.path.splitext(script)[0] + " is attached to this email."
    csv_creator(script)
    new_file = open(file_name, "w+")
    csv = MIMEText(new_file.read())
    csv.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(csv)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, email_address, text)
    csv_remover(script)
    server.quit()


# def option_selector():
#     '''Allows user selection to choose the file of the script that needs to be
#     read and determine the output type of the file.'''
#     script = input('\n\nPlease input the script that you want the \
#     locations for (the full path):')
#     choice = input('\n\nPlease pick the method that you would prefer to \
#     recieve your location information: "onscreen", by "email", or as a \
#     "download":\n\n')
#     choice = choice.upper()
#     if choice == 'ONSCREEN':
#         return ('\n' + table_creator(script) + '\n\nThanks very much for using our Script Location Reader.')
#     if choice == 'EMAIL':
#         locations_emailer(script)
#         return ('\n\nThanks very much for using our Script Location Reader.')
#     if choice == 'DOWNLOAD':
#         csv_creator(script)
#         return ('\n\nThanks very much for using our Script Location Reader.')
#     else:
#         choice = raw_input('Please select one of "onscreen", "email", or \
#         "download".')
#         option_selector()
#         return ('\n\nThanks very much for using our Script Location Reader.')


#option_selector()


if __name__ == '__main__':
    main()
