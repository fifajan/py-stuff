#! /usr/bin/python

if __name__ == '__main__':

    from sys import argv

    if len(argv) != 2:
        print '\nUSAGE: $ ./get_unique_ip_list.py /path/to/logfile.log\n'
        raise RuntimeError, 'Bad input.'

    WEB_SERVER_ACCESS_LOG_FILE = argv[1]
    OUTPUT_UNIQUE_IPS_LIST_FILE = 'IPs.log'

    f = open(WEB_SERVER_ACCESS_LOG_FILE)
    l = f.readlines()
    ips = [i.partition(' ')[0] for i in l]

    # get unique IPs
    s = set(ips)
    f.close()

    # write IPs to file
    f = open(OUTPUT_UNIQUE_IPS_LIST_FILE, 'w')
    for i in s:
        f.write(str(i) + '\n')

    f.close()
