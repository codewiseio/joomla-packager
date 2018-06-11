

import configparser
import os.path
import distutils.dir_util
import shutil
import zipfile
import getopt
import sys

class JoomlaPackager():

	config = configparser.ConfigParser()
	source_path = '.'

	def __init__(self, source_path='.'):
		
		self.source_path = source_path

		# read the configuration file
		distfile = os.path.join( self.source_path, 'dist.ini')

		if os.path.isfile(distfile):
			self.config.read(distfile)
		else:
			print( "Could not find a dist.ini file to read configuration information from at: " + distfile )
			exit()

	def collect(self):
		# check for existence of joomla installation
		if not os.path.isdir( self.config.get('joomla','path') ):
			die( "No Joomla! installation at " + self.config.get('joomla','path') );

		# check for existence of extension folder
		if not os.path.isdir( self.install_extension_path() ):
			die( "Could not collect files. Path does not exist: " + self.extension_path() );

		# check for existence of admin folder
		if not os.path.isdir( self.install_extension_path("admin") ):
			die( "Could not collect files. Path does not exist: " + self.extension_path('admin') );

		"""Collect the files from the demo area"""
		print ("Collecting files from Jooml! installation at: " + self.config.get('joomla','path') )

		# copy the site files from the joomla install to the source directory
		site_path =  os.path.join( self.source_path, 'site' )
		distutils.dir_util.copy_tree( self.install_extension_path('site'), site_path )

		# copy the admin files
		admin_path =  os.path.join( self.source_path, 'admin' )
		self.install_extension_path('admin')
		distutils.dir_util.copy_tree( self.install_extension_path('admin'), admin_path  )

		return True



	def install_extension_path(self,area="site"):

		return os.path.join( 
			self.config.get('joomla','path'),  
			"administrator" if area=="admin" else "",
			self.config.get('dist','type') + 's',
			self.config.get('dist','name')
		)


	def package(self):
		"""collect an archive containing the entire application"""

		# create  the package name and version number
		distname = "{}-{}".format(self.config.get('dist','name'), self.config.get('dist','version') )
		tmpdir   = os.path.join( self.source_path, distname )

		distdir  = os.path.join( self.source_path, 'dist' )
		distfile = os.path.join( distdir, distname + '.zip' )


		print ("Creating package at: " + distfile )

		# creat the dist dir if it does not exist
		if not os.path.isdir(distdir): os.mkdir(distdir)

		# copy the contents of the folder into the temporary folder
		distutils.dir_util.copy_tree(self.source_path, tmpdir)		

		# delete old versions of this distribution
		if os.path.isfile(distfile): os.remove(distfile)

		# create the distribution archive		
		zipf = zipfile.ZipFile(distfile, 'w', zipfile.ZIP_DEFLATED)

		# walk the file path
		for root, dirs, files in os.walk(tmpdir):

			# remove the path to the source directory in the zip archive
			zippath = root;
			if zippath.startswith(self.source_path + '/'):
				zippath = zippath[len(self.source_path + '/'):]
	
			for file in files:
				frompath =  os.path.join(root,file)
				topath   =  os.path.join(zippath,file)

				# ignore the dist directory
				if frompath.startswith(self.source_path + '/dist'):
					pass
				# ignore the dist.ini file
				elif frompath == os.path.join(root,'dist.ini'):
					pass
				# write the file
				else:
					zipf.write( frompath, topath  )	

		zipf.close()

		# delete the tmp directory	
		shutil.rmtree(tmpdir)

		pass

	def install():
		"""Install the files to the demo area"""

	def die(self,message):
		print(message)




if __name__ == '__main__':

	def usage():

		print ("Collect files from Joomla installation folder to source")
		print ("\tjpack.py -c\n");

		print ("Package extension for distribution")
		print ("\tjpack.py -p\n");

		print ("Collect and package files")
		print ("\tjpack.py -cp\n");

		print ("Perform operation in different directory")
		print ("\tjpack.py --source=path/to/extension/source -c\n");

	# get the command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'cps:', ['collect', 'package', 'source='])
	except getopt.GetoptError:
	    usage()
	    sys.exit(2)

	source = '.'
	collect  = False
	package = False

	# determine actions to take
	for opt, arg in opts:
	    if opt in ('-c', '--collect'):
	    	collect = True
	    elif opt in ('-p', '--package'):
	       package = True

	    elif opt in ('-s', '--source'):
	        source = arg
	    else:
	        usage()
	        sys.exit(2)

	# perform actions
	jpack = JoomlaPackager(source_path=source)

	if collect:
		jpack.collect()

	if package:
		jpack.package()

	if not collect and not package:
		print ( "No actions to take.\n")
		usage()


# read in the sys.ini file
	

# get the extension name

# deterime the extension type