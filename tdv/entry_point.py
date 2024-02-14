""" Run this file to run the program """
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)



from tdv.main_loop import MainLoop



main_loop = MainLoop()
main_loop.run()
