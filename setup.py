from setuptools import setup
import pdbeccdutils

setup(name='pdbeccdutils',
      version=pdbeccdutils.__version__,
      description='Toolkit to deal with wwPDB chemical components definitions for small molecules.',
      project_urls={
          'Source code': 'https://gitlab.ebi.ac.uk/pdbe/ccdutils',
          'Documentation': 'https://pdbe.gitdocs.ebi.ac.uk/ccdutils/',
      },
      author='Protein Data Bank in Europe',
      author_email='pdbehelp@ebi.ac.uk',
      license='Apache License 2.0.',
      keywords='PDB CCD wwPDB small molecule',
      packages=['pdbeccdutils'],
      scripts=['bin/setup_pubchem_library',
               'bin/process_components_cif',
               'bin/murcko_scaffold_cif'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['Pillow', 'scipy', 'pdbecif'],
      tests_require=['pytest']
      )
