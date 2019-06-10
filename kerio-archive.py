
import os, sys
import email
import pyzmail

from shutil import copyfile, move
import datetime as datetime


def get_date_of_email(filename):
    """
    Return the date parsed from 'Date:' in the message header

    Args:
        filename: the name of the email file, typically .eml extension

    Returns:
        datetime object from the message header, or "NONE" if
        there is not one found, or the date is an un-standard format

    """
    input_file = open(filename)
    msg = pyzmail.parse.message_from_file(input_file)
    input_file.close()
    date_string = msg.get_decoded_header('Date')
    if date_string == '':
        return "NONE"
    else:
        date_tuple = email.utils.parsedate(date_string)
    # handle dates like 11/16/2016 3:29:16PM
    if date_tuple is None:
        print "Date was not in RFC2822 format: ", date_string
        return "NONE"
    else:
        # handle yy dates, ie '16' instead of '2016'
        if date_tuple[0] < 100:
            # convert tuple to list so we can modify, then convert back
            l = list(date_tuple)
            l[0] += 2000
            date_tuple = tuple(l)
        return datetime.date(*date_tuple[:3])

def archive_folder(folder_name):
    """
    Crawls the mailbox folder and moves all items to a new folder,
    by the date of the message headers, for each calendar year

    Args:
        folder_name: name of the folder/directory to crawl

    Returns:
        none

    """
    # these must be created in each folder so that Kerio will re-index
    status_file_slug_name = 'status.fld'
    index_file_slug_name = 'index.fld'
    
    print "Archiving ", folder_name
    if not os.path.isdir(folder_name):
        print "Directory for folder doesn't seem to exist: ", folder_name
        return
    today = datetime.date.today()
    days_to_keep = 365 # emails have to be this old to archive
	# ignore folders with this text in name. these will be compared case-insensitive
	no_archive_directives = ("noarchive", "no archive")

    # recursively walk email directory
    for dirpath, dirnames, filenames in os.walk(folder_name):
        for f in filenames:
            # combine the full directory path with the file name
            full_filename = os.path.join(dirpath, f)
            print "* Processing ", full_filename

            # is this an .eml file?
            if os.path.splitext(f)[1].lower() != ".eml":
                print "Not an .eml file. Skipping ", full_filename
            else:
                # is 'noarchive' in the name?
                if any(s in full_filename.lower() for s in no_archive_directives):
                    print "'NO ARCHIVE' is set for ", full_filename
                else:
                    msg_date = get_date_of_email(full_filename)
                    if msg_date == "NONE":
                        print "DATE ERROR with ", full_filename
                    else:
                        # is this message over 1 year old? archive it.
                        diff = today - msg_date
                        if diff.days > days_to_keep:
                            # build the new directory starting with the message year
                            # create if it doesn't exist
                            target_dir_name = os.path.join(cwd, str(msg_date.year), dirpath)
                            if not os.path.exists(target_dir_name):
                                print "Need to create the directory ", target_dir_name
                                os.makedirs(target_dir_name)
                                
                            slug_file = os.path.join(target_dir_name, status_file_slug_name)
                            if not os.path.isfile(slug_file):
                                print "Creating status file slug"
                                open(slug_file, 'w+').close()
                                
                            slug_file = os.path.join(target_dir_name, index_file_slug_name)
                            if not os.path.isfile(slug_file):
                                print "Creating status file slug"
                                open(slug_file, 'w+').close()

                                print "moved to ", target_dir_name
                            move(full_filename, os.path.join(target_dir_name, f))


# main script begins

# folders to archive
folders_to_archive = ("INBOX", "Sent Items", "Deleted Items")

cwd = os.getcwd()
print "current dir: ", cwd

for f in folders_to_archive:
    archive_folder(f)
