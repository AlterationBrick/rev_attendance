#!/usr/bin/python

import json
import sys

def membership_achieved(m):
    return m['type'] == 'new' and m['meetings'] >= 8 and m['teamevents'] >= 1

def update_regular(idfilename, datafilename):
    with open(idfilename, 'r') as idfile:
        ids = [line.strip() for line in idfile]
    with open(datafilename, 'r+') as datafile:
        memdict = json.load(datafile)
        for rcsid in ids:
            if rcsid in memdict:
                memdict[rcsid]['meetings'] += 1
                if membership_achieved(memdict[rcsid]):
                    memdict[rcsid]['type'] = 'member'
                    print("{} has achieved membership!".format(rcsid))
            else:
                print("Member {} was not recognized.".format(rcsid))
        datafile.seek(0)
        datafile.truncate(0)
        json.dump(memdict, datafile)

def add_members(infilename, datafilename):
    with open(infilename, 'r') as infile:
        memdict = {}
        for line in infile:
            line_l = [item.strip() for item in line.split(',')]
            memdict[line_l[1]]={'name': line_l[0], 'gmail': line_l[2], 'meetings': 1, 'teamevents': 0, 'type': 'new'}
    with open(datafilename, 'r+') as datafile:
        try:
            old_dict = json.load(datafile)
        except json.JSONDecodeError:
            old_dict = {}
        old_dict.update(memdict)
        datafile.seek(0)
        datafile.truncate(0)
        json.dump(memdict, datafile)
        
def add_member(name, rcsid, gmail, member_type, datafilename):
    with open(datafilename, 'r+') as datafile:
        memdict = json.load(datafile)
        memdict[rcsid] = {'name': name, 'gmail': gmail, 'meetings': 1, 'teamevents': 0, 'type': member_type}
        datafile.seek(0)
        datafile.truncate(0)
        json.dump(memdict, datafile)
            
def check_membership(datafilename):
    with open(datafilename, 'r') as datafile:
        memdict = json.load(datafile)
        members = [m for m in memdict if memdict[m]['type'] == 'member']
        noobs = [m for m in memdict if memdict[m]['type'] == 'new']
        leads = [m for m in memdict if memdict[m]['type'] == 'leader']
        print("Leads:\n{}\nMembers:\n{}\n".format("\n".join(leads), "\n".join(members)))
        for n in noobs:
            print("{} needs {} meetings and {} team events to achieve membership".format(n, 8 - memdict[n]['meetings'], 1 - memdict[n]['teamevents']))

if __name__ == "__main__":
    action = sys.argv[1]
    # mem.py attend idfile datafile
    if action == "meeting":
        update_regular(sys.argv[2], sys.argv[3])
    # new member format: [First Last] rcsid gmail
    # member storage format: rcsid: {First Last gmail meetings teamevents type}
    # type: new, member, leader
    if action == "new":
        add_members(sys.argv[2], sys.argv[3])
    if action == "new_single":
        add_member(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    if action == "check":
        check_membership(sys.argv[2])
