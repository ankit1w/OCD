# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=[r'.'],
             binaries=[],
             datas=[(r'.\pdfCropMargins_mod\pdftoppm_windows_local', r'pdfCropMargins_mod\pdftoppm_windows_local'),
                    (r'.\wkhtmltopdf.exe', '.'),
                    (r'.\phantomjs.exe', '.'),
                    (r'.\disable_quick_edit.bat', '.'),
                    (r'.\dino.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

Key = ['mkl','libopenblas','numpy','tcl', 'tkinter','mfc140u']

def remove_from_list(input, keys):
    outlist = []
    for item in input:
        name, _, _ = item
        flag = 0
        for key_word in keys:
            if name.find(key_word) > -1:
                flag = 1
        if flag != 1:
            outlist.append(item)
    return outlist

a.binaries = remove_from_list(a.binaries, Key)


exe = EXE(pyz,
          a.scripts,
          [('W ignore', None, 'OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon=r'./ocd.ico')
