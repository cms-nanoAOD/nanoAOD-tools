import fileinput, string, sys, os, time

if len(sys.argv) != 2:
        print "USAGE: %s <input.txt> "%(sys.argv [0])
        sys.exit (1)

inputfile = sys.argv [1]

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    #line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            #line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
		string = line.rstrip()
		#list_of_results.append(string[18:]) #Output dataset:
                #list_of_results.append(string[25:]) #Number of events read:
		list_of_results.append(string[30:]) #root://cms-xrd-global.cern.ch/
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

listdataset = search_string_in_file(inputfile,"root://cms-xrd-global.cern.ch/")
print "size of array = ",len(listdataset)
#print listdataset
for i in range(0,len(listdataset)):
    print listdataset[i].rsplit("/",1)[0]+"/"
