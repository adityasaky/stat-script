from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[], excludes=[])

base = 'Console'

executables = [
    Executable('wavystats.py', base=base, targetName='wavystats')
]

setup(name='wavystats',
      version='0.1.2-1',
      description='A dirty but dep-less way to stat your targets',
      options=dict(build_exe=buildOptions),
      executables=executables)
