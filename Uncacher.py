import sys

from shutil import copyfile
from os import listdir, mkdir
from os.path import isfile, join, exists
from distutils.dir_util import copy_tree

original_loc = "C:\\Users\\caina\\AppData\\Roaming\\discord\\Cache"

default_args = {
	"-o": "Output",
	"-i": "Cache",
	"-e": ".png",
	"-c": False,
	"-p": False
	}

def copy_to_new_dir(new_loc):
	global original_loc
	copy_tree(original_loc, new_loc)


def run(args):
	cache_loc = args["-i"]
	new_loc = args["-o"]
	ftype = args["-e"]
	populate = args["-p"]
	create_output_folder = args["-c"]
	file_names = []

	if not exists(cache_loc):
		if create_output_folder:
			mkdir(cache_loc)
		else:
			print("Input folder location don't exist. Use -c to create the folder.")
			return

	if populate:
		try:
			copy_to_new_dir(cache_loc)
		except Exception as e:
			print(f"Failed to populate the data.\nReason: {str(e)}")
			print("Proceeding to convert anything else inside the input folder.")

	if not exists(new_loc):
		if create_output_folder:
			mkdir(new_loc)
		else:
			print("Output folder location don't exist. Use -c to create the folder.")
			return

	only_files = [f for f in listdir(cache_loc + "\\") if isfile(join(cache_loc + "\\", f))]

	for file in only_files:
		copyfile(join(cache_loc + "\\", file), join(new_loc + "\\", file + ftype))

	print("Complete.")

def parse_args(args):
	global default_args
	skip_next = False
	args_list = ["-o", "-i", "-e"]

	ret = default_args

	for idx in range(len(args)):
		if skip_next:
			skip_next = False
			continue

		if args[idx] in args_list:
			skip_next = True
			ret[args[idx]] = args[idx + 1]
			# print(f"Setting {args[idx]} to {args[idx + 1]}")

	
	ret["-c"] = "-c" in args
	ret["-p"] = "-p" in args

	return ret

def help_menu():
	print("""
	Discord Uncacher.
		
		Usage: python Uncacher.py {args}

		Options:
		-i {name}\tSets the input folder as the folder with the given name. Defaults to 'Cache'.
		-o {name}\tSets the output folder as the folder where the output is stored. Defaults to 'Output'.
		-e {name}\tSets the extension of the new files. Defaults to '.png'
		-c\t\tCreates the output folder with the given name if it doesn't exist yet.
		-p\t\tCURRENTLY DOESN'T WORK. Populates the input folder.

		-h\t\tShows this menu.

		""")

if __name__ == "__main__":

	file_ext = ".gif"
	new_file_loc = "Output gif"
	out = parse_args(sys.argv)

	if '-h' in sys.argv:
		help_menu()
	else:
		run(out)