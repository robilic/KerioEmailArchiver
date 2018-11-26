# KerioEmailArchiver
Mail Archiver for Kerio Connect

I thought I'd share a small script I made to help with archiving Kerio mailboxes. Like the rest of you, I had users with 10, 20, 30, even 50GB of email from over the years.

This script runs on Python 2.6 (have not tested under 3, as our email server is CentOS 5 - ancient!). You can run this script from the terminal in a users mail folder and it will move the files around into folders based on year.

You can set days_to_keep as how many days old an email must be to not archive. A value of 90 will not archive any emails that are not over 90 days old.

no_archive_directives can be set to anything you don't want to archive. With the default value, if you put 'NO ARCHIVE' in the folder name, it won't be archived.

So, on my system I run the script from:

    /opt/kerio/mailserver/store/mail/mydomain.com/username

You'll end up with something like

    2016
    ├── Deleted Items
    ├── Inbox
    | ├── foo
    | └── bar
    └── Sent Items

    2017
    ├── Deleted Items
    ├── Inbox
    | ├── foo
    | └── bar
    └── Sent Items

    ...


And of course, after the script runs you will want to re-index the mailbox. And possibly move the old files to another server or backup drive, etc.
