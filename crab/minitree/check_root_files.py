import argparse as arg
import glob
import os
import sys

import ROOT

if __name__ == '__main__':
	parser = arg.ArgumentParser(description='Recursively check that every .root file under a directory opens and its tree can be read')
	parser.add_argument('-d', '--dir', dest='Dir', type=str, required=True, help="directory to scan for .root files")
	parser.add_argument('-t', '--tree', dest='TreeName', type=str, default='Events', help="tree name to read from each file (default: Events)")
	parser.add_argument('-delete', '--delete', dest='Delete', action='store_true', help="delete files that fail the check")


	args = parser.parse_args()

	if not os.path.isdir(args.Dir):
		print("Dir '" + args.Dir + "' does not exist")
		sys.exit(1)

	ROOT.gErrorIgnoreLevel = ROOT.kFatal

	root_files = sorted(glob.glob(args.Dir.rstrip('/') + '/**/*.root', recursive=True))
	print("Total .root files found : ", len(root_files))

	good_files = []
	bad_files = []
	nonzero_entry_files = []
	total_entries = 0

	for fname in root_files:
		try:
			f = ROOT.TFile.Open(fname)
			if (not f) or f.IsZombie():
				bad_files.append((fname, "could not open file / zombie"))
				continue
			tree = f.Get(args.TreeName)
			if not tree:
				bad_files.append((fname, f"tree '{args.TreeName}' not found in file"))
				f.Close()
				continue
			nentries = tree.GetEntries()
			f.Close()
			print(f"OK   {fname}  ({nentries} entries)")
			good_files.append(fname)
			total_entries += nentries
			if nentries > 0:
				nonzero_entry_files.append(fname)
			else:
				if args.Delete:
					print(f"Deleting file {fname} due to zero entries")
					os.remove(fname)
		except Exception as e:
			bad_files.append((fname, str(e)))

	print()
	print("-----------------------------------------    summary     --------------------------------")
	print("Good files : ", len(good_files))
	print("Bad files  : ", len(bad_files))
	if bad_files:
		print("\nBad file details:")
		for fname, reason in bad_files:
			print(f"  {fname}  --  {reason}")
	print()
	print(f"Total entries in '{args.TreeName}' across good files : ", total_entries)
	print()
	print(f"Files with non-zero '{args.TreeName}' entries ({len(nonzero_entry_files)}), space-separated:")
	print(' '.join(nonzero_entry_files))
