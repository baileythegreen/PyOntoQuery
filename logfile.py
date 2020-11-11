import time
import pprint

# Will this ever not be the logfile?
def write_out(thing, file):
    lines = {'solid': '#' * 70,
            'dashed': '-' * 70,
            'empty': ''
           }
    with open(file, 'a') as f:
        if isinstance(thing, str) and thing in lines.keys():
                print(lines[thing], file=f)
        elif isinstance(thing, str):
            #print(lineno(), file=f)
            print(thing, file=f)
        else:
            #print(lineno(), file=f)
            pprint.pprint(thing, stream=f)
        print(lines['empty'], file=f)

def log_header(file, opts, args, parser, entries):
    #global p, entries
    write_out('Started at: %s' % time.ctime(), file)
    lines = ['dashed', 'Script: %s' % parser.get_version(),
            'options', 'args:\n%s' % args, 'entries:\n%s' % entries]
    for line in lines:
        if not line == 'options':
            write_out(line, file)
        else:
            print('options:', file=open(file, 'a'))
            write_out(opts.__dict__, file)
    return

def new_output_section(string, file):
    write_out('dashed', file)
    write_out(string.title(), file)
    #write_out('empty', file)
    return