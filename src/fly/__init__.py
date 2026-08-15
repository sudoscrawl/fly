from importlib.metadata import version

__version__ = version("flyt")

# It's this way so that I don't need to manually change the version
# at every place where it gets used
