#! /usr/bin/python

'''
htdigest credentials file generator helper script.
`pwds' dict should filled with 'user' : 'pass' pairs,
'pass's should be copy-pasted 2 times into the `htdigest' tool
password prompt.
`pwd_file_%03d' file set (one file for each user) will be generated.
Then
$ cat pwd_file_[0-9][0-9][0-9] > passwords.secret
command should be run.
`passwords.secret' file is reeady as credentials file for usage in
digest HTTP auth.
'''

pwds = { #'user_1': 'PASS1234',
         #'user_2': '12_QWERTY_34',
         'user_3': '111_GOD',
         'user_4': 'mypass1991'
}

realm = 'domain.com'

if __name__ == '__main__':

    import os

    filename_template = 'pwd_file_%03d'
    htdigest_part = 'htdigest -c %s ' % filename_template
    realm_user = '%s %s'
    htdigest_cmd = htdigest_part + realm_user

    for i, user in enumerate(pwds):
        print 'Creationg user: %s with password: %s' % (user, pwds[user])
        os.system(htdigest_cmd % (i, realm, user))
        print 'Done!'

    print 'Generated %d htdigest files.' % (i + 1)
