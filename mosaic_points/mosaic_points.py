#! /usr/bin/python3
"""
A script for parsing .chk_im files for NanoSIMS stage position data,
and returning a tab-separated CSV file presenting [source, tile number, x, y, z]
and titled according to the chk_im file name or as given.\n\n

Can be passed files explicitly, via a directory, or via an expression.
"""
import os
import argparse


def get_title(path):
	"""
	Strip a path of surrounding details (i.e. extension and tile number) such that what remains
	is a string to use as a title.

	:param path: <String> Pathname to edit

	:return title: <String> Clean title to use
	"""
	no_ext = os.path.splitext(path)[0]
	no_tile = no_ext.rsplit('_', maxsplit=1)[0]
	title = os.path.basename(no_tile)

	return title + "_tileXY.csv"


def main(files, title):
	"""
	Given a file name pattern or directory, will create an output csv file containing
	the (x,y,z) coordinates of the NanoSIMS 50L for each tile (i.e. in the center of the tile).

	:param files: <List> chk_im file names (strings)
	:param title: <String> Name of output file (default based on the name of the first file)
	"""	
	if not title:
		title = get_title(files[0])

	column_info = "Source\tTile Number\tx (um)\ty (um)\tz (um)\n"
	row_data = []

	for file in files:
		if not os.path.exists(file):
			print("Skipped a file that wasn't found.")
			continue

		file_name, file_ext = os.path.splitext(file)
		if file_ext != '.chk_im':
			print("Skipped a file that wasn't .chk_im.")
			continue

		tile_number = file_name.rsplit('_', maxsplit=1)[1]  # Split once on underscore from the right

		# Get the (x, y, z) values
		# It's possible that different machines write their .chk_im's differently, in which case this 
		# would need to be altered. This is for the 50L. This information is also in .im files, which
		# can be shown with `unu head` in the command line
		with open(file, 'r') as chk_im:
			for line in chk_im:
				if line.startswith("Stage Position"):
					stage_data = line.split()

					for value in stage_data:
						if value.startswith('x'):
							x = value.split('=')[1]
						elif value.startswith('y'):
							y = value.split('=')[1]
						elif value.startswith('z'):
							z = value.split('=')[1]

		# Append each tab-separated cell (don't forget the newline!)
		row_data.append(f"{os.path.basename(file)}\t{tile_number}\t{x}\t{y}\t{z}\n")

	# Sort the row_data by tile number (the second column)
	row_data.sort(key=lambda row: int(row.split('\t')[1]))

	# Write the data (if any) to a csv file, title gathered above.
	if len(row_data) == 0:
		print("There wasn't any data gathered. Check that the files passed are correct.")
		raise SystemExit

	with open(title, 'w') as output:
		output.write(column_info)
		for row in row_data:
			output.write(row)

	# Print a confirmation
	print(f"Wrote tile coordinates to {title}")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)

	parser.add_argument('files', nargs='*',
		help="Files that will be used.")
	parser.add_argument('-t', '--title', type=str, default=None,
		help="Title for the output csv file. Default is based on the given chk_im's")

	args = parser.parse_args()

	if not args.files:
		parser.print_help()
		raise SystemExit

	print(f"Going through the {len(args.files)} given chk_im files....\n")
	main(args.files, args.title)
