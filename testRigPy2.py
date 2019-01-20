#!/usr/bin/python2.7
#
'''
    Program:    hcpcli...
    Author:     liam collins

    Version:    alpha-0.2.0

    Edits:
    2018-10-14  lc      Created from scratch as Proof of Concept
    2018-10-20  lc      Convert all HCP logic to the hcp module. This
                        is now a wrapper script showing how the hcp
                        module can be called.

    Copyright (c) 2018 NOVA Industries Limited

    No warenty, all rights reserved.

    This program was written using the public available HCP document
    "MK-HCPAW012-04: HCP Anywhere File Sync and Share API Reference Guide"
    published by Hitachi Vantara. This document can be found at:

    "https://knowledge.hitachivantara.com/Documents/Storage/Content_Platform_Anywhere/4.0.0/File_Sync_and_Share_API_Reference"
'''
import urllib2
import json
import os
import sys
from optparse import OptionParser
'''
    http        Simple module to return the string of a HTTP return code
    hcp         The module that actually talks to HCP Anywhere
'''
import http
import hcp

HTTP_OK = 200
HTTP_CREATED = 201

parser = OptionParser('usage: %prog -u <user> -p <password> -x <hcp URL>' )
parser.add_option( '-u', '--user',      dest='username',    default=None, help='Username' )
parser.add_option( '-p', '--password',  dest='password',    default=None, help='Password' )
parser.add_option( '-s', '--url',       dest='url',         default=None, help='URL server name' )
parser.add_option( '-c', '--command',   dest='command',     default=None, help='Command (ls/upload/download/delete)')
parser.add_option( '-f', '--filename',  dest='filename',    default=None, help='Source filename (upload/download)' )
parser.add_option( '-d', '--dir',       dest='directory',   default=None, help='Driectory')
parser.add_option( '-t', '--to',        dest='to',          default=None, help='Destination filename')
(options,args) = parser.parse_args()

if ( options.username is None or
        options.password is None or
        options.url is None or
        options.command is None ) :
    parser.error( 'Missing options' )


def hcpLs( options ) :

    (rc,content) = hcp.ls( options )

    if rc == HTTP_OK :
        dirList = content[ 'entries' ]
        for item in dirList:
            if 'size' not in item :
                item['size'] = 0
            print( '{0}\t{1}\t{2:d}\t{3}'.format( item['type'].lower(),
                                                    item['access'].lower(),
                                                    item['size'],
                                                    item['name']))
    else :
        print( 'Cannot find directory "{0}"'.format(options.directory))

    return (rc, content)

def hcpUpload( options ) :

    (rc, content) = hcp.upload( options )

    print( 'Content:{0}'.format( content ))
    return (rc, content)
'''
    # BUG: This doesn't work at all...
'''
def hcpDownload( options ) :
    (rc, content) = hcp.download( options )
    print( 'RC={0}, content={1}'.format(rc, content))
    return (rc, content)

def hcpMkdir( options ) :

    (rc,content) = hcp.mkdir( options )

    if rc == HTTP_CREATED :
        print( '{0}\n{1}'.format( rc, content ))
    else :
        print( 'Create failed ')

    return (rc, content)
'''
    Yet to be implemented
'''
def hcpRm( options ) :
    print( 'Yet to be implemented' )
    return( 1,'YTBI')

def hcpRmDir( options ):
    print( 'Yet to be implemented' )
    return( 1,'YTBI')
'''

                    M A I N   B O D Y   C O D E
                    =======   =======   =======

    List of all of the supported commands:
'''
hcpCommand = {
    'upload'    : hcpUpload,
    'download'  : hcpDownload,
    'rm'        : hcpRm,
    'rmdir'     : hcpRmDir,
    'mkdir'     : hcpMkdir,
    'ls'        : hcpLs
}

def main() :

    if options.command in hcpCommand :
        (rc, content) = hcp.login( options )
        if rc == HTTP_OK :
            (rc, content) = hcpCommand[ options.command ]( options )
            sys.exit( rc )
        else:
            print( 'Error: login failed...')
            sys.exit(1)
    else :
        parser.error('Unknown command')

if __name__ == '__main__':
    main()
