
import argparse
import collections
import json
import sys

def read(passwd_path, group_path):

    passwd_file_path = passwd_path
    group_file_path = group_path

    group_dict = build_group_dict(group_file_path)
    user_dict = build_users(passwd_file_path, group_dict)
    json_users = json.dumps(user_dict)
    print(json_users)
    return json_users


def build_group_dict(group_file_path):

    try:
        f = open(group_file_path, 'r')
    except IOError:
        print "Could not read file:", group_file_path
        sys.exit()

    dict = {}

    while True:
        line = f.readline()
        if not line:
            f.close()
            break
        if line[0] != '#':
            fields = line.split(":")
            if len(fields) != 4:
                print('Group missing necessary components. Skip.')
                continue
            if fields[2] == '\\n' or fields[2] == '':
                continue
            else:
                gid = int(fields[2])
                name = fields[0]
                dict[gid] = name
    return dict


def build_users(passwd_file_path, group_dict):

    try:
        f = open(passwd_file_path, 'r')
    except IOError:
        print "Could not read file:", passwd_file_path
        sys.exit()

    users_dict = {}

    while True:
        line = f.readline()
        if not line:
            f.close()
            break
        if line[0] != '#':
            fields = line.split(":")
            if len(fields) != 7:
                print('User missing necessary components. Skip.')
                continue
            if fields[0] != '':
                fields_dict = collections.OrderedDict()

                user_name = fields[0]
                uid = fields[2]
                full_name = fields[4]

                groups = []
                if fields[3] != '':
                    group_fields = fields[3].split(',')
                    for group in group_fields:
                        group_name = group_dict.get(int(group), None)
                        if group_name is not None:
                            groups.append(group_name)

                fields_dict['uid'] = int(uid)
                fields_dict['full_name'] = full_name
                fields_dict['groups'] = groups
                users_dict[user_name] = fields_dict

    return users_dict


def main():

    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-p", help="Path to passwd directory", type=str, required=True)
    required.add_argument("-g", help="Path to group directory", type=str, required=True)

    try:
        args = parser.parse_args()
        passwd_path = args.p
        group_path = args.g
        read(passwd_path, group_path)
    except argparse.ArgumentError:
        sys.exit()


if __name__ == "__main__":
    main()
