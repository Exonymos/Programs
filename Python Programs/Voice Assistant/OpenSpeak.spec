# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['gpt_va.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openai', 'speech_recognition', 'pyttsx3', 'sounddevice', 'wavio'],
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

# specify product name, file description, internal name, and company name
product_name = 'OpenSpeak'
file_description = 'A Voice Assistant powered by GPT-3'
internal_name = 'OpenSpeak'
company_name = 'Exonymos'

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OpenSpeak',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
    file_description=file_description,
    internal_name=internal_name,
    product_name=product_name,
    company_name=company_name,
)
