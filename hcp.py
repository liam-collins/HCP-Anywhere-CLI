#
import urllib2
import json
import os
'''
'''
headers = {
    'Accept-Type': 'application/json',
    'Content-Type': 'application/json',
    'Accept-Language': 'utf-8',
    'X-HCPAW-FSS-API-VERSION': '4.0.0'
}

commandDictionary = {
    'login' :   '/fss/public/login/oauth',
    'ls'    :   '/fss/public/folder/entries/list',
    'upload':   '/fss/public/file/stream/create?',
    'download': '/fss/public/file/stream/read',
    'mkdir' :   '/fss/public/folder/create',
    'rm'    :   '/fss/public/path/delete',
    'rmstar':   '/fss/public/path/multiDelete'
}

HTTP_OK = 200
HTTP_CREATED = 201

'''
    hcpIO:  The function that talks to HCP Anywhere and returns results

    Parameters:
    ~~~~~~~~~~~
    baseURL     : The is the URL of the HCP server
    command     : This is looked up in the "command dictionary" to find
                    out what needs to be added to create a full URL
    data        : Any payload
    bin         : Any binary payload
    additionalHeaders : Any extra headers above those in the "headers" dictionary
                        This is a dictionary.
    postItems   : Some of the URLs require post item information (like the
                    file name in "upload". This allows functions to "paste"
                    strings onto the end of the URL. This is a string

    Returns (tuple):
    ~~~~~~~~~~~~~~~~
    rc          : HTTP return code
    content     : A dictionay containing the returned information. This is
                    converted from the JSON returned by HCP.
'''
def hcpIO( baseURL, command, data=None, bin=None, aditionalHeaders=None, postItems=None ) :
    '''
        Using the "command", find out what needs to be added to the
        baseURL to give the actual URL HCP Anywhere will understand
    '''
    if command in commandDictionary :
        commandPath = commandDictionary[ command ]
    else:
        print( 'error:unknown command {0}'.format( command ))
        sys.exit( 1 )

    if postItems is None :
        url = '{0}{1}'.format( baseURL, commandPath )
    else :
        url = '{0}{1}{2}'.format( baseURL, commandPath, postItems )

    if data is not None :
        request = urllib2.Request( url, data=json.dumps( data ))
    elif bin is not None :
        request = urllib2.Request( url, bin )
    else :
        request = urllib2.Request( url )

    for item in headers :
        request.add_header( item, headers[ item ] )

    if aditionalHeaders is not None :
        for item in aditionalHeaders:
            request.add_header( item, aditionalHeaders[ item ] )
    try :
        response = urllib2.urlopen( request )
    except urllib2.HTTPError :
        return (1, None )

    rc = response.code
    content = json.loads( response.read() )

    return (rc, content)
'''
    The core functions have the same struct and returns:

    (rc, content) = <function>( options )

    rc          : The HTTP Return Code (200-500)
    contents    : The returning JSON structure from HCPAnyWhere

    options     : Dictionary containing the following:
                    'username'  : The username to login in with
                    'password'  :
                    'url'       : The URL of the HCPAnyWhere server
                                    e.g.: https://hcpanywhere.hds.com
                    'filename'  : The name of the source file
                    'to'        : The name of the destination file
                    'dir'       : The name of a directory

    Workflow:
    ~~~~~~~~~
    Obviously you must run the "login" function. This function will update
    the headers with a token ID given by HCPAnyWhere. The token is embedded
    into the headers that every other function uses, allowing you to run
    multiple commands without having to relogin in

'''
'''
    requires: 'username', 'password', 'url'
'''
def login( options ) :
    data = {
        'grant_type': 'urn:hds:oauth:negotiate-client'
    }

    data[ 'username' ] = options.username
    data[ 'password' ] = options.password

    (rc, content) = hcpIO( options.url, 'login', data=data )

    if rc == 200 :
        tokenID = content[ 'access_token' ]
        tokenType = content[ 'token_type' ]
        expiresIn = content[ 'expires_in' ]
        headers[ 'Authorization' ] = '{0} {1}'.format( tokenType, tokenID )

    return (rc, content)
'''
    requires: 'url'
    optional: 'directory'
'''
def ls( options ) :

    if options.directory is None :
        data = { 'path' : '/' }
    else :
        data = { 'path' : options.directory }

    (rc,content) = hcpIO(options.url, 'ls', data=data )

    return(rc, content)
'''
    requires:   'url', 'filename'
    optional:   'to'
'''
def upload( options ) :

    additionalHeaders = {
        'Content-Type' : 'application/octet-stream',
        'Content-Length' : os.stat(options.filename).st_size
    }

    if options.to is None :
        postItem = 'path={0}'.format( options.filename )
    else :
        postItem = 'path={0}'.format( options.to )

    try :
        fh = open( options.filename, 'rb')
    except :
        return (1, '{ "Error":"file {0} is cannot be opened}"'.format( filename ))

    (rc, content) = hcpIO( options.url, 'upload', bin=fh, aditionalHeaders=additionalHeaders, postItems=postItem)

    return (rc, content)
'''
    # BUG: This doesn't work at all...
'''
def download( options ) :
    additionalHeaders = {
        'Content-Type' : 'application/octet-stream',
        'Content-Length' : os.stat(options.filename).st_size
    }

    data = {
        'path' : options.filename
    }
    (rc, content) = hcpIO( options.url, 'download', data=data, aditionalHeaders=additionalHeaders )
    with open( options.destination, 'rb' ) as fh:
        fh.write( content )
    print( '{0}'.format(rc))

    return (rc, content)
'''
    requires:   'url', 'directory'
'''
def mkdir( options ) :
    data = {
        'path' : options.directory,
        'createParents' : True
    }

    (rc,content) = hcpIO( options.url, 'mkdir', data=data )
    if rc <> HTTP_CREATED :
        content( '{ "Error" : "Directory creation failed" }')

    return rc, content
'''
    requires:   'url', 'filename'
'''
def rm( options ) :
    return( 0, '{"Error" : "Not yet implemented" }')
'''
    requires:   'url', 'directory'
'''
def rmdir( options ) :
    return( 0, '{"Error" : "Not yet implemented" }')
