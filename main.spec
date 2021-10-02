# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('pdfCropMargins_mod/pdftoppm_windows_local', 'pdfCropMargins_mod/pdftoppm_windows_local'),
                    ('wkhtmltopdf.exe', '.'),
                    ('phantomjs.exe', '.'),
                    ('disable_quick_edit.bat', '.'),
                    ('dino.txt', '.')],
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
          icon='ocd.ico')
