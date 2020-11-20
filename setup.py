# -*- coding: utf-8 -*-

from distutils.core import setup 
import py2exe 
 
setup(name="Aladdin's Adventure", 
 version="1.0", 
 description="Breve descripcion", 
 author="Andrea Elias", 
 author_email="eli17048@uvg.edu.gt", 
 url="url del proyecto", 
 license="tipo de licencia", 
 scripts=["Proyecto_Andrea.py"] , 
 console=["Proyecto_Andrea.py"], 
 options={"py2exe": {"bundle_files": 2}}, 
 zipfile=None,
)