from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[], excludes=[])

base = 'Console'

executables = [
    Executable('stat-script.py', base=base, targetName='stat-script')
]

setup(name='stat-script',
      version='0.1.6',
      description='A dirty but dep-less way to stat your targets',
      options=dict(build_exe=buildOptions),
      executables=executables)
