import os
import shutil

def check_directory(dir_name):
	if os.path.isdir(dir_name):
		return True
	else:
		return False

def create_directory(dir_name):
	if os.path.exists(dir_name):
		return False
	else:
		os.makedirs(dir_name)
		return True

def create_file(dir_name, file_name, contents):
	if os.path.isdir(dir_name):
		file_path = os.path.join(dir_name, file_name)
		if not os.path.exists(file_path):
			fileout = open(file_path, "w")
			fileout.write(contents)
			fileout.close()
			return True
		else:
			return False
	else:
		return False

def check_file(dir_name, file_name):
	if os.path.isdir(dir_name):
		file_path = os.path.join(dir_name, file_name)
		if os.path.isfile(file_path):
			return True
		else:
			return False
	else:
		return False

def delete_file(dir_name, file_name):
	if os.path.isdir(dir_name):
		file_path = os.path.join(dir_name, file_name)
		if os.path.isfile(file_path):
			os.remove(file_path)
		else:
			return False
	else:
		return False

def delete_directory(dir_name):
	if os.path.isdir(dir_name):
		files = os.listdir(dir_name)
		for file in files:
			os.remove(os.path.join(dir_name, file))
		os.rmdir(dir_name)
		return True
	else:
		return False

def reset_everything(dir_name):
	shutil.rmtree(dir_name)


