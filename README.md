Project: HCP-Anywhere-CLI

This is a proof of concept of a Hitachi Content Platform (HDS) HCP-Anywhere CLI. The code
was for a collegue that only had access to Python 2.7. The code does need a complete re-write
but will, at least, show how to do the following actions:

	1. login
	2. upload a file to HCP
	3. make a directory within HCP-Anywhere
	4. list the contents of a directory

I do plan to add the following option but that'll be done when I move this to Python 3.x and
rewrite it properly...

	1. Download a file
	2. Delete a file
	3. Delete a directory (including its contents)


How to use:
===========

The code runs from the "testRigPy2.py":

liam$ ~/Projects/HCP-CLI$ ./testRigPy2.py --help
Usage: testRigPy2.py -u <user> -p <password> -x <hcp URL>

Options:
  -h, --help            show this help message and exit
  -u USERNAME, --user=USERNAME
                        Username
  -p PASSWORD, --password=PASSWORD
                        Password
  -s URL, --url=URL     URL server name
  -c COMMAND, --command=COMMAND
                        Command (ls/upload/download/delete)
  -f FILENAME, --filename=FILENAME
                        Source filename (upload/download)
  -d DIRECTORY, --dir=DIRECTORY
                        Driectory
  -t TO, --to=TO        Destination filename


The commands are:

    'upload'    : Upload a file ("-f") to the directory "-d" or "/" position. 
    'download'  : **Doesn't work 
    'rm'        : **Doesn't work 
    'rmdir'     : **Doesn't work 
    'mkdir'     : Make a driectory from the location pointed to by "-d" or "/"
    'ls'        : List a given directory from the location pointed to by "-d" or "/" 
