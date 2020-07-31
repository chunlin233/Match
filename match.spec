# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['match.py'],
             pathex=['fuzz.py', 'process.py', 'string_processing.py', 'StringMatcher.py', 'test_fuzz.py', 'ui.py', 'utils.py', 'utils1.py', 'C:\\Users\\Sakura\\Desktop\\code'],
             binaries=[],
             datas=[],
             hiddenimports=['pandas', 'numpy', 'os', 'tkinter', 'simhash', 'nltk', 'xlrd', 'openyxl'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='match',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
