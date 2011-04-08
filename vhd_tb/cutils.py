import os
import shutil
from vhd_tb import vhdlfile

def isolate_file(file, dst):
    fdic = {}
    if os.path.exists(file):
        files_in_dir = []
        abspath = os.path.abspath(file)
	dname = os.path.dirname(abspath)
	for f in os.listdir(dname):
	    if os.path.isfile(os.path.join(dname,f)):
		if f.split(".")[1] in ("vhdl","VHDL","vhd","VHD"):
		    files_in_dir.append(os.path.join(dname,f))
	ifdic = {}
	fi = open(file)
	fb = fi.read()
	fi.close()
	fvhd = vhdlfile.vhdlfile(fb)
	submodules = fvhd.get_submodules()
	shutil.copy(file,dst)
	get_related_files(file,submodules,files_in_dir,dst)
	

def get_related_files(file, submodules, files_in_dir,dst):
    for f in files_in_dir:
        fi = open(f)
	fb = fi.read()
	fi.close()
	fvhd = vhdlfile.vhdlfile(fb)
	modname = fvhd.get_name()
	if modname in submodules:
	    shutil.copy(f,dst)
	    get_related_files(f,fvhd.get_submodules(),files_in_dir,dst)

def move_file(file_, dest):
    if os.path.exists(file_):
        if os.path.exists(dest):
            shutil.copy(file_, dest)
            os.remove(file_)
