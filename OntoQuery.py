import sys, os, optparse
import obonet
import networkx
import pprint
import inspect
import time
from helpformat import PrettyHelpFormatter
import logfile

def lineno():
    """Returns the current line number in our program."""
    return "Line number %d: " % inspect.currentframe().f_back.f_lineno

def read_tree_file(file):
    """Reads in a .obo ontology tree file."""
    try:
        graph = obonet.read_obo(file)
        return graph
    except ValueError:
        raise ValueError('File: %s has unknown file structure for .obo file. \
        \n \t It may be the wrong file type.' % file)

def read_entries_list(file):
    """Reads in a list of values of interest. Values may be
    names of entries in the ontology, or identifiers, but
    should be just one per line."""
    entries = []
    with open(file) as f:
        for line in f:
            entries.append(line.strip())
    #print(lineno(), 'entries:', entries)
    return entries

def get_name(node):
    """Returns the name associated with node.
    Checks whether node is a key in the id_to_name library.
    If True, it and returns the associated value from id_to_name.
    If node is a key in name_to_id, node itself is returned.
    Raises a KeyError if neither case is True."""
    if node in id_to_name.keys():
        name = id_to_name[node]
    elif node in name_to_id.keys():
        name = node
    else:
        raise KeyError('Name: %s is not in the dataset' % node)
    #print(lineno(), 'name:', name)
    return name
        
def get_id(node):
    """Returns the identifier associated with node.
    Checks whether node is a key in the name_to_id library.
    If True, it and returns the associated value from name_to_id.
    If node is a key in id_to_name, node itself is returned.
    Raises a KeyError if neither case is True."""
    if node in name_to_id.keys():
        id_num = name_to_id[node]
    elif node in id_to_name.keys():
        id_num = node
    else:
        raise KeyError('Identifier: %s is not in the dataset' % node)
    #print(lineno(), 'id_num:', id_num)
    return id_num

def get_category_list(umbrella_node=None):
    """Gets the list of categories to which the selected entries should be 
    matched. A supracategory that captures all desired categories may be
    designated, or a list of categories may be supplied for more tailored
    results."""
    if umbrella_node == None:
        umbrella_node = get_id(supra_cat)
    categories = {}
    #print(lineno(), 'umbrella_node:', umbrella_node)
    for child, parent, key in graph.in_edges(umbrella_node, keys = True):
        #print(lineno(), 'child, parent, key:', child, parent, key)
        categories[get_name(child)] = child
    #print(lineno(), 'categories:', categories)
    #for cat in cat_list:
    #    categories[get_name(cat)] = get_id(cat)
    return categories

def get_paths(entry, umbrella_node=None):
    """Gets all paths from origin to destination(s).
    origin must be in the form of an ontology identifier, not a name."""
    if umbrella_node == None:
        umbrella_node = get_id(supra_cat)
        origin = get_id(entry)
    #print(lineno(), 'umbrella_node:', umbrella_node)
    destinations = get_category_list(umbrella_node).values()
    #print(lineno(), 'categories:', categories)
    paths = networkx.all_simple_paths(graph, source = origin, target = destinations)
    #print(lineno(), 'paths:', paths)
    return paths

def get_start_and_end(path):
    """Gets the origin and destination for a particular path.
    Returns a tuple."""
    entry = get_name(path[0])
    category = get_name(path[-1])
    #print(lineno(), 'entry, category:', entry, category)
    return entry, category

def match_categories(nodes=None):
    """Iterates through all of the entries in the list file and finds the categories
    in the category list that they fall under. Returns a dictionary with each entry
    as a key and the values being either a set (if duplicates == False; the default)
    or a list (if duplicates == True) of categories."""
    if nodes == None:
        nodes = entries
    results = {}
    for node in nodes:
        try:
            paths = get_paths(node)
        except KeyError:
            logfile.write_out('KeyError: %s is not a valid entry' % node, log_file)
            continue
        for path in paths:
            entry, category = get_start_and_end(path)
            if duplicates == False:
                # the dictionary values for each key will be a set (no duplicates)
                if entry in results.keys():
                    results[entry].add(category)
                else:
                    results[entry] = {category}
            elif duplicates == True:
                # the dictionary values for each key will be a list (duplicates)
                if entry in results.keys():
                    results[entry].append(category)
                else:
                    results[entry] = [category]
    #print(lineno(), 'results:', results)
    return results

# Debate: multiple output functions, or one that implements a 'switch/case'?
def write_json(results, mode='w'):
    """Writes desired entries and their categories to a json format.
    The category sets are converted to lists so as to be compatible
    with the json format."""
    import json
    with open(out_file, mode) as file:
        new_results = {key: list(value) for key, value in results.items()}
        json.dump(new_results, file, indent=4, sort_keys=True)
    logfile.write_out(results, log_file)

def write_json_plus_input(results, mode='w'):
    # print out inputs
    write_json(results, 'a')
    return

def write_csv():
    pass

def write_tsv():
    pass

def help():
    print('''
    =======================================================================================================================
    Usage:
    
    python get_efo_disease_types.py -t <tree_file> -i <list_file>
    [, -o <out_file> [, -l <log_file> [, -s <supracategory>
    [, -c <categories> [, -d <duplicates> ] ] ] ] ]
    
    A tree file and a disease list file must be provided.
    
    An output file name and a log file name may be optionally specified;
    if these are not given, default values will be used:
    
    Output file default: ontoquery_results.json
    
    Log file default: ontoquery.log

 --------------------------------------------------------------------------

    For more information, run:

    python get_efo_disease_types.py -h

    or

    python get_efo_disease_types.py --help
    =======================================================================================================================
    ''')
    sys.exit(1)

def parse_options(values):
    """p is the parser that was defined in main()"""
    usage = "usage: %prog -t tree_file -i list_file [options]"
    version = "%prog 1.0"
    description = "Retrieves information from TREE_FILE for a list of ontology tree entries found in LIST_FILE.§match_categories() will match the entries found in LIST_FILE with the immediate descendants of SUPRA_CAT, the contents of CAT_FILE, or both that are connected to each entry in LIST_FILE.".replace('§', '\n\n    ')
    globals().update({'p' : optparse.OptionParser(usage = usage,
                      version = version, description = description)}) #,
                      #formatter = PrettyHelpFormatter())})
    p.add_option("-t", "--tree", action = "store", dest = "tree_file",
                help = "a .obo file containing an ontology tree",
                metavar = "TREE_FILE")
    p.add_option("-i", "--input", action = "store", dest = "list_file",
                help = "a .txt file containing a list of entries in TREE_FILE; this is set to %default by default")
    p.add_option("-s", "--supra", action = "store", dest = "supra_cat",
                help = "parent category of categories desired in the output")
    p.add_option("-c", "--cat-file", action = "store", dest = "cat_file",
                help = "a .txt file containing a list of target categories for the output; this is set to %default by default")
    p.add_option("-d", "--duplicate", "--duplicates", action = "store",
                dest = "duplicates",
                help = "boolean value; should duplicate values be included in ouput; this is set to %default by default")
    p.add_option("-o", "--output", action = "store", dest = "out_file",
                help = "file where output should be printed; this is set to %default by default")
    p.add_option("-l", "--log", action = "store", dest = "log_file",
                help = "file where the errors and output are logged; this is set to %default by default %prog")
    p.add_option("-w", "--working-dir", action = "store", dest = "work_dir",
                help = "working directory; this is set to the current working directory by default; cwd is: %default")
    p.set_defaults(tree_file = None , list_file = 'node_list.txt',
                out_file = 'entry_categories.json', log_file = 'log.txt',
                supra_cat = None, cat_file = None, duplicates = False,
                work_dir = os.getcwd().lstrip())
    return p.parse_args()



##### main
def main():
    if len(sys.argv) == 1: help()
    opts, args = parse_options(sys.argv)
    if not opts.tree_file: help()
    if not opts.list_file: help()
    globals().update({'log_file' : opts.log_file})
    #log_header(log_file, opts, args)
    globals().update({'graph' : read_tree_file(opts.tree_file)})
    globals().update({'entries' : read_entries_list(opts.list_file)})
    globals().update({'supra_cat' : opts.supra_cat})
    #if opts.cat_file: globals().update({'cat_list' : read_entries_list(opts.cat_file)})
    globals().update({'duplicates' : opts.duplicates})
    globals().update({'out_file' : opts.out_file})
    globals().update({'work_dir' : opts.work_dir})
    globals().update({'id_to_name' : {id_: data.get('name') for id_, data in graph.nodes(data=True) if 'name' in data}})
    globals().update({'name_to_id' : {data['name']: id_ for id_, data in graph.nodes(data=True) if 'name' in data}})
    #################################
    #write_out(entries)
    logfile.log_header(log_file, opts, args, p, entries)
    logfile.new_output_section('Run-time messages:', log_file)
    results = match_categories()
    logfile.new_output_section('Results:', log_file)
    write_json(results)
    logfile.write_out('\nResults are being saved to: %s.' % out_file, log_file)
    logfile.new_output_section('End:', log_file)
    logfile.write_out('Finished at: %s' % time.ctime(), log_file)
    
if __name__ == '__main__':
    main()
    

    
    
    
    # #Enable a category list rather than just a supracategory
    # Finish styling output file.
    
    # print paths to files, not just names
    # option for an output file that includes input parameters
    # name output and log similarly