# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hiddenimports = collect_submodules('fastapi') + collect_submodules('starlette') + collect_submodules('pydantic') + [
'ai_services.chat_service',
'ai_services.scan_service',
]
BASE_DIR = os.path.abspath('.')

a = Analysis(
['launcher.py'],
pathex=[BASE_DIR],
binaries=[],
datas=[
# backend и его routers
('backend', 'backend'),
('backend/routers', 'backend/routers'),
# frontend с картинками
('frontend', 'frontend'),
('frontend/img/dark.png', 'frontend/img'),
('frontend/img/white.png', 'frontend/img'),
('frontend/img/logo.png', 'frontend/img'),
# ai_services
('ai_services', 'ai_services'),
# веса и база знаний
('best.pt', '.'),
('best.tar', '.'),
('knowledge_base.json', '.')
],
hiddenimports=hiddenimports,
hookspath=[],
runtime_hooks=[],
excludes=[
    "pkg_resources",
    "pkg_resources._vendor",
    "pkg_resources._vendor.jaraco",
    "pkg_resources._vendor.jaraco.text",
    "setuptools",
    "setuptools._vendor",
    "setuptools._vendor.jaraco",
    "setuptools._vendor.jaraco.text",
],
noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
pyz,
a.scripts,
a.binaries,
a.datas,
[],
name='BloomBuddy',
debug=False,
strip=False,
upx=False,
console=True,
onefile=True
)