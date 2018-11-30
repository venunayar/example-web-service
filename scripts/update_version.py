import json
import os
import sys

def update_version(cfg_dict):
    ov = cfg_dict['version']
    subversions = cfg_dict['version'].split('.')
    subversions[-1] = str(int(subversions[-1]) + 1)
    nv = cfg_dict['version'] = '.'.join(subversions)
    print 'Updated version from {} to {}'.format(ov, nv)
    return

def main(args):
    try:
        cfg_dict = {}
        if len(args) <= 1:
            print 'No version file specified.'
            sys.exit(-1)
            
        version_file = args[1]    
        with open(version_file, 'r') as f:
            cfg_dict = json.load(f)
        update_version(cfg_dict)
        with open(version_file, 'w') as f:
            json.dump(cfg_dict, f)
    except Exception as e:
        print 'Error updating version: {}'.format(e.message)
        sys.exit(-1)

if __name__ == '__main__':
    main(sys.argv)
