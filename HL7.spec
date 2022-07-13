# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
    ('images\\ico.ico', '.'),
    ('images\\send.png', 'images'),
    ('images\\load.png', 'images'),
    ('images\\save.png', 'images'),
    ('images\\clear.png', 'images'),
    ('images\\delete.png', 'images'),
    ('images\\listen.png', 'images'),
    ('styles\\dark.qss', 'styles'),
    ('styles\\light.qss', 'styles')
    ]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HL7',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='images\\ico.ico',
    version='version.txt'
)
