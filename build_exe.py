import PyInstaller.__main__

PyInstaller.__main__.run([
    'card3.py',
    '--onefile',
    '--windowed',
    '--name=CardCatalog',
    '--clean',
])
