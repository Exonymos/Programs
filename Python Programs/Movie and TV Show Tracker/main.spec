# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import sys
from PyInstaller.utils.hooks import collect_submodules


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=collect_submodules('requests') + collect_submodules('bs4') + collect_submodules('sqlite3'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

# specify product name, file description, internal name, and company name
product_name = 'Episode Tracker'
file_description = 'A simple python application for tracking movies and TV shows.'
internal_name = 'Episode Tracker'
company_name = 'Exonymos'

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=internal_name,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon=['icon.ico'],         
          file_description=file_description,
          internal_name=internal_name,
          product_name=product_name,
          company_name=company_name)
