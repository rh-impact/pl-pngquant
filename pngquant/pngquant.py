#
# pngquant ds ChRIS plugin app
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from email.policy import default
from chrisapp.base import ChrisApp
import subprocess, sys, os, re


Gstr_title = r"""
                                           _   
                                          | |  
 _ __  _ __   __ _  __ _ _   _  __ _ _ __ | |_ 
| '_ \| '_ \ / _` |/ _` | | | |/ _` | '_ \| __|
| |_) | | | | (_| | (_| | |_| | (_| | | | | |_ 
| .__/|_| |_|\__, |\__, |\__,_|\__,_|_| |_|\__|
| |           __/ |   | |                      
|_|          |___/    |_|                      
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       pngquant

    SYNOPSIS

        docker run --rm fnndsc/pl-pngquant pngquant                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-pngquant pngquant                        \
                /incoming /outgoing

    DESCRIPTION

        `pngquant` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
"""


class Pngquant(ChrisApp):
    """
    Compress PNG images using pngquant.
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS plugin for pngquant'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 2000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 8000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--force', '-f', optional=True, default=False, dest='force', type=bool, help='overwrite existing output files');
        self.add_argument('--ext', '-e', optional=True, default='', dest='ext', type=str, help='set custom suffix/extension for output filenames');

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        print('Copressing PNG images here %s to %s' % (options.inputdir, options.outputdir))
        for filename in os.listdir(options.inputdir):
            inputpath = os.path.join(options.inputdir, filename)

            if not options.ext:
                outputpath = os.path.join(options.outputdir, filename)
            else:
                outputpath = os.path.join(options.outputdir, re.sub('\.\w+$', options.ext, filename))

            cmd = ['/usr/bin/pngquant']

            if options.verbosity != '0':
                cmd.append('--verbose')

            if options.force:
                cmd.append('--force')

            cmd.append('--output')
            cmd.append(outputpath)
            cmd.append('--')
            cmd.append(inputpath)

            sys.stdout.flush()

            subprocess.run(cmd, check=True)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
