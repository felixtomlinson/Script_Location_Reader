import os
import textract
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from prettytable import PrettyTable

def main():
   print(table_creator('Sherlock-A-Study-in-Pink-final-shooting-script.pdf'))
   print(table_creator('A-Long-Way-Down-Shooting-Script.pdf'))
   print(table_creator('Peaky-Blinders-S1-Ep1.pdf'))
   print(table_creator('Brooklyn-Shooting-Script.pdf'))
   pass

def document_reader(file):
    '''Uses textract to read and return the text of files, split them into different lines and make them uppercase'''
    text = textract.process(file)
    text = text.splitlines()
    return text

def split_text_by_given_times_of_day(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out):
    times_in_the_day = ['DAY', 'NIGHT', 'EVENING','DUSK', 'DAWN', 'MORNING', 'SUNSET', 'LATE AFTERNOON']
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

def split_text_by_hyphens(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out):
    hyphen_number = important_text_without_inside_or_out.rfind('- ')
    if important_text_without_inside_or_out[hyphen_number-1] == ' ':
        stop_number = hyphen_number-1
    location_type = important_text_without_inside_or_out[end_of_inside_or_out+1:hyphen_number-1]
    time_of_day = important_text_without_inside_or_out[hyphen_number+2:]
    return [inside_or_out, location_type, time_of_day]

def split_text_by_stops(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out):
    stop_number = important_text_without_inside_or_out.rfind('.')
    if important_text_without_inside_or_out[stop_number-1] == ' ':
        stop_number = stop_number-1
    location_type = important_text_without_inside_or_out[end_of_inside_or_out+1:stop_number]
    if location_type[-1] == '.':
        location_type = location_type[:-1]
    time_of_day = important_text_without_inside_or_out[stop_number+2:]
    return [inside_or_out, location_type, time_of_day]

def split_text_without_time_of_day(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out):
    location_type = important_text_without_inside_or_out[end_of_inside_or_out+1:]
    time_of_day = 'NA'
    return [inside_or_out, location_type, time_of_day]

def split_text_returner(important_text_without_inside_or_out, inside_or_out):
    end_of_inside_or_out = len(inside_or_out)
    if split_text_by_given_times_of_day(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out) != -1:
        return split_text_by_given_times_of_day(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out)
    if important_text_without_inside_or_out.find('- ') != -1:
        return split_text_by_hyphens(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out)
    if important_text_without_inside_or_out.rfind('.') != -1:
        return split_text_by_stops(important_text_without_inside_or_out, end_of_inside_or_out, inside_or_out)
    else:
        return split_text_without_time_of_day

def split_text_returner_in_reverse(important_text_without_inside_or_out, inside_or_out):
    end_of_inside_or_out = len(inside_or_out)+1
    times_in_the_day = ['DAY', 'NIGHT', 'EVENING','DUSK', 'DAWN', 'MORNING', 'SUNSET', 'LATE AFTERNOON']
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

def text_splitter (important_text):
    '''Splits the various important parts of the text out into a list. The important parts for this tool are: \
if the location is inside or outside, the location details and what time of day the actions is happening at'''
    inside_or_out_or_both = ['INT./EXT.', 'INT.', 'EXT.']
    for category in inside_or_out_or_both:
        start_of_inside_or_out = important_text.find(category)
        if start_of_inside_or_out != -1:
            if important_text[-1] == '.':
                important_text = important_text[:-1]
            important_text = important_text[start_of_inside_or_out:]
            split_text = split_text_returner(important_text, category)
            if split_text == None:
                return split_text
            if split_text[1] == '':
                split_text = split_text_returner_in_reverse(important_text, category)
            return split_text

def deleted_scene_detector(important_text):
    '''If a scene is labelled as omitted or scene delted this will produce a list for the table\
which reflects that the scene is no longer being used.'''
    omitted = ['OMITTED', 'SCENE DELETED']
    for name in omitted:
        omitted_or_not = important_text.find(name)
        if omitted_or_not != -1:
            return ['***NA***', '***OMITTED***','***NA***']

def heading_decider(output_type):
    '''Depending on what type of output has been selected by the user this function creates the headings in the correct format'''
    if output_type == 'CSV':
        return ('Scene Number,Internal or external,Type of Location,Time of Day\n')
    else:
        return (['Scene Number','Internal or external','Type of Location','Time of Day'])

def important_text_compiler(list_of_strings, string, index):
    '''If the important text is split up by split lines due to how the PDF is formatted\
this function recompiles it into a single string so that it can be read and the text split\
into useful categories'''
    inside_or_out_or_both = ['INT./EXT.', 'INT.', 'EXT.']
    for category in inside_or_out_or_both:
        if category == string:
            next_string = index+2
            new_string = string + " " + list_of_strings[next_string]
            return new_string
    return string

def rough_scene_checker(script_as_list, index, which_side):
    '''Checks to see if there are any short strings in close proximity to the important text'''
    #Needs to be improved to strip out non-numbers
    if len(script_as_list[index + 2 * which_side]) <= 5:
        if len (script_as_list[index + 2 * which_side]) > 0:
            if not '.' in script_as_list[index + 2 * which_side]:
                scene_number = script_as_list[index + 2 * which_side]
                return scene_number

def potential_scene_number_compiler(script_as_list):
    '''Returns a list of strings which are shorter than 6 characters'''
    #Needs to be improved to strip out non-numbers
    potential_strings_within_range = []
    for strings in script_as_list:
        if len(strings) <= 5:
            if len (strings) > 0:
                potential_strings_within_range.append(strings)
    return potential_strings_within_range

def scene_number_one_on_each_side(script_as_list):
    '''Finds potential scene numbers in the text, split by lines, before and the text after the important text.\
It returns a number if it appears both before and after the text.'''
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
    '''Finds potential scene numbers in the text, split by lines, around the important text.\
It returns a number if it appears twice in the text, split by lines.'''
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
    '''Finds potential scene numbers in the text, split by lines, around the important text.\
It returns a number if it appears twice in the text, split by spaces.'''
    potential_number = potential_scene_number_compiler(script_as_list)
    script_as_list = list_splitter(script_as_list)
    for number in potential_number:
        number_of_occurences = script_as_list.count(number)
        if number_of_occurences == 2:
            return number

def script_trimmer(script_as_list, script_length, index, search_range, search_type):
    '''Returns a list of the strings around the string that contain important information\
the length of the list can be determined by inputting a search range. If the list is returned\
in two halves or as one list is determined by search_type'''
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

def best_guesser(script_as_list, script_length, index, start, end, search_type):
    '''Given a range and a selected search type, this function selects a function to carry\
out a search and returns the number that it returns.'''
    for number in range(start, end):
        trimmed_script = script_trimmer(script_as_list, script_length, index, number, search_type)
        if search_type == 'one_on_each_side':
            scene_number = scene_number_one_on_each_side(trimmed_script)
        elif search_type == 'two_anywhere':
            scene_number = scene_number_two_anywhere(trimmed_script)
        elif search_type == 'split_script':
            scene_number = scene_number_two_anywhere_with_split_lists(trimmed_script)
        if scene_number != None:
            return scene_number

def scene_numberer(script_as_list, index):
    '''Searches the area surrounding the key text to see if there are places where scene numbers that might be\
it then checks to see if they are anywhere else and returns those numbers if they are'''
    script_length = len(script_as_list)
    if script_as_list[index-2] == script_as_list[index+2]:
        if (index-2) > 0:
            if (index+2) < script_length:
                return script_as_list[index+2]
    lowers = [3, 9, 13]
    uppers = [8, 12, 16]
    combined = zip(lowers,uppers)
    for i, j in combined:
        scene_number = best_guesser(script_as_list, script_length, index, i, j, 'one_on_each_side')
        if scene_number != None:
            return scene_number
        scene_number = best_guesser(script_as_list, script_length, index, i, j, 'two_anywhere')
        if scene_number != None:
            return scene_number
    for i, j in combined:
        scene_number = best_guesser(script_as_list, script_length, index, i, j, 'split_script')
        if scene_number != None:
            return scene_number
    if (script_as_list[index+1]) == '' or (script_as_list[index-1]) == '':
        scene_number = rough_scene_checker(script_as_list, index, 1)
        if scene_number == None:
            scene_number = rough_scene_checker(script_as_list, index, -1)
        if scene_number != None:
            return scene_number
    print script_as_list[index-10:index+10]
    return ''

def line_generator(list, output_type):
    '''Turns a list with three objects in it either into CSV or a table depending on the ouput type selected'''
    if output_type == 'CSV':
        return list[0] + ',' + list[1] + ',' + list[2] + ',' + list[3] + '\n'
    else:
        return list

def table_creator(script):
    '''This function takes the script as an input and uses the formatted_lines function to add all the locations together and\
 turns it in into a table.'''
    script = document_reader(script)
    table = PrettyTable(heading_decider('text'))
    index = 0
    for lines in script:
        formatted_lines = text_splitter(lines)
        if formatted_lines != None:
            if formatted_lines[1]=='':
                compiled_line = important_text_compiler(script, lines, index)
                formatted_lines = text_splitter(compiled_line)
            scene_number = scene_numberer(script, index)
            formatted_lines.insert(0, scene_number)
            table.add_row(line_generator(formatted_lines, 'text'))
        deleted_lines = deleted_scene_detector(lines)
        if deleted_lines != None:
            scene_number = scene_numberer(script, index)
            deleted_lines.insert(0, scene_number)
            table.add_row(line_generator(deleted_lines, 'text'))
        index += 1
    return str(table)

def file_namer(file):
    '''Names the file as a CSV document with a useful description'''
    return ('Location Information for '+ os.path.splitext(file)[0] + '.csv')

def csv_creator(script):
    '''This function takes the script as an input and uses the formatted_lines function to add all the locations together and\
    creates a CSV file.'''
    file_name = file_namer(script)
    csv = open(file_name, "w")
    script = document_reader(script)
    table = heading_decider("CSV")
    index = 0
    for lines in script:
        formatted_lines = text_splitter(lines)
        if formatted_lines != None:
            if formatted_lines[1]=='':
                compiled_line = important_text_compiler(script, lines, index)
                formatted_lines = text_splitter(compiled_line)
            scene_number = scene_numberer(script, index)
            formatted_lines.insert(0, scene_number)
            table += line_generator(formatted_lines, "CSV")
        deleted_lines = deleted_scene_detector(lines)
        if deleted_lines != None:
            scene_number = scene_numberer(script, index)
            deleted_lines.insert(0, scene_number)
            table += line_generator(deleted_lines, "CSV")
        index += 1
    csv.write(table)
    csv.close

def locations_emailer(script):
    '''Sends the user a CSV file with their location information in it'''
    file_name = file_namer(script)
    fromaddr = "script.location.reader@gmail.com"
    password = open('emailpasswordsetting.txt',"r")
    password = password.read()
    toaddr = raw_input('\nPlease type the email you want the document to be sent to:\n')
    msg = MIMEMultipart()
    msg['From'] = 'Script Location Reader'
    msg['To'] = toaddr
    msg['Subject'] = os.path.splitext(file_name)[0]
    body = "Thank you very much for using our Script Location Reader service. \n\n\
The location information for " + os.path.splitext(script)[0] +  " is attached to this email."
    csv_creator(script)
    new_file = open(file_name, "rw")
    csv = MIMEText(new_file.read())
    csv.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(csv)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    csv_remover(script)
    server.quit()

def csv_remover(script):
    '''Removes the file created by csv_creator'''
    file_name = file_namer(script)
    os.remove(file_name)

def option_selector():
    '''Allows user selection to choose the file of the script that needs to be read and \
determine the output type of the file.'''
    script = raw_input('\n\nPlease input the script that you want the locations for (the full path):')
    choice = raw_input('\n\nPlease pick the method that you would prefer to recieve your location information: "onscreen", by "email", or as a "download":\n\n')
    choice = choice.upper()
    if choice == 'ONSCREEN':
        print ('\n'+table_creator(script))
        return ('\n\nThanks very much for using our Script Location Reader.')
    if choice == 'EMAIL':
        locations_emailer(script)
        return ('\n\nThanks very much for using our Script Location Reader.')
    if choice == 'DOWNLOAD':
        csv_creator(script)
        return ('\n\nThanks very much for using our Script Location Reader.')
    else:
        choice = raw_input('Please select one of "onscreen", "email", or "download".')
        option_selector()
        return ('\n\nThanks very much for using our Script Location Reader.')

#option_selector()

if __name__ == '__main__':
    main()
