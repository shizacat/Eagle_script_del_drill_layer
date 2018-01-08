#!/usr/bin/env python3

import sys
import os
import shutil
import xml.etree.ElementTree as ET

work_layers = ['144', '145', '146']

def backup(name):
	new_name = os.path.join(
		os.path.split(name)[0],
		os.path.split(name)[1] + '.bak'
	)

	shutil.copyfile(name, new_name)

def del_layer(name):
	try:
		tree = ET.parse(name)
		root = tree.getroot()

		layers = root.find('./drawing/layers')
		for child in root.findall('./drawing/layers/'):
			if child.attrib['number'] in work_layers:
				layers.remove(child)

		libraries = root.find('./drawing/board/libraries')
		for item in root.findall('./drawing/board/libraries/'):
			if item.attrib['name'] == 'drilegend':
				libraries.remove(item)

		plain = root.find('./drawing/board/plain')
		for item in root.findall('./drawing/board/plain/'):
			if item.attrib.get('layer', '') in work_layers:
				plain.remove(item)

		elements = root.find('./drawing/board/elements')
		for item in root.findall('./drawing/board/elements/'):
			if item.attrib.get('library', '') == 'drilegend':
				elements.remove(item)

		new_name = os.path.splitext(os.path.split(name)[1])[0] + '_new' + os.path.splitext(os.path.split(name)[1])[1]
		tree.write(name)
	except ET.ParseError:
		print('Error in the xml file format.')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Enter the file name!')
		sys.exit(-1)

	file_name = sys.argv[1]

	if not os.path.exists(file_name):
		print('"{}" file not found!'.format(file_name))
		sys.exit(-1)

	backup(file_name)
	del_layer(file_name)