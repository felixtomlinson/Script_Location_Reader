import os
import textract
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from prettytable import PrettyTable

def document_reader(file):
    '''Uses textract to read and return the text of files, split them into different lines and make them uppercase'''
    text = textract.process(file)
    text = text.splitlines()
    return text

def scene_numberer(script_as_list, index):
    script_length = len(script_as_list)
    if (index-2) > 0:
        if (index+2) < script_length:
            if script_as_list[index-2] == script_as_list[index+2]:
                return script_as_list[index+2]
            elif (index+1) == '':
                scene_number = index+2
                for strings in script_as_list[index-10:index]:
                    there_or_not = strings.find(scene_number)
                    if there_or_not != -1:
                        return scene_number
            elif (index-1) == '':
                scene_number = index-2
                for strings in script_as_list[index:index+10]:
                    there_or_not = strings.find(scene_number)
                    if there_or_not != -1:
                        return scene_number
            else:
                for strings in script_as_list[index-10:index+10]:
                    if len(strings) <= 3:
                        if len (strings) > 0:
                            if not '.' in strings:
                                there_or_not= strings.find(strings)
                                if there_or_not != -1:
                                    return strings
                return ''

def text_splitter (important_text):
    '''Splits the various important parts of the text out into a list. The important parts for this tool are: \
if the location is inside or outside, the location details and what time of day the actions is happening at'''
    inside_or_out_or_both = ['INT./EXT.', 'INT.', 'EXT.']
    for category in inside_or_out_or_both:
        start_of_inside_or_out = important_text.find(category)
        if start_of_inside_or_out != -1:
            end_of_inside_or_out = start_of_inside_or_out + len(category)
            inside_or_out = important_text[start_of_inside_or_out:end_of_inside_or_out]
            times_in_the_day = ['DAY', 'NIGHT', 'EVENING']
            for times in times_in_the_day:
                start_of_time_of_day = important_text.find(times)
                if start_of_time_of_day != -1:
                    location_type = important_text[end_of_inside_or_out+1:start_of_time_of_day-2]
                    time_of_day = important_text[start_of_time_of_day:]
                    return [inside_or_out, location_type, time_of_day]
            if important_text.find('-') != -1:
                hyphen_number = important_text.rfind('-')
                location_type = important_text[end_of_inside_or_out+1:hyphen_number-1]
                time_of_day = important_text[hyphen_number+2:]
                return [inside_or_out, location_type, time_of_day]
            if important_text.rfind('.') > len(category):
                stop_number = important_text.rfind('.')
                location_type = important_text[end_of_inside_or_out+1:stop_number]
                time_of_day = important_text[stop_number+2:]
                return [inside_or_out, location_type, time_of_day]
            else:
                location_type = important_text[end_of_inside_or_out+1:]
                time_of_day = 'NA'
                return [inside_or_out, location_type, time_of_day]

def heading_decider(output_type):
    '''Depending on what type of output has been selected by the user this function creates the headings in the correct format'''
    if output_type == 'CSV':
        return ('Scene Number,Internal or external,Type of Location,Time of Day\n')
    else:
        return (['Scene Number','Internal or external','Type of Location','Time of Day'])

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
            scene_number = scene_numberer(script, index)
            if formatted_lines[1]=='':
                print index
            formatted_lines.insert(0, scene_number)
            table.add_row(line_generator(formatted_lines, 'text'))
        index += 1
    return str(table)

print (table_creator('Sherlock-A-Study-in-Pink-final-shooting-script.pdf'))

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
    for lines in script:
        lines = important_text_compiler(script, lines)
        formatted_lines = text_splitter(lines)
        if formatted_lines != None:
            if formatted_lines[1] != '':
                scene_number = scene_numberer(script, lines)
                formatted_lines.insert(0, scene_number)
                table += line_generator(formatted_lines, "CSV")
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

#if __name__ == '__main__':
#    main()
