#!/bin/sh
pyinstaller  --icon="start_here_ubuntu.ico" \
--add-data 'web/templates/*:web/templates' \
--add-data 'web/css/*:web/css' \
--add-data 'web/js/*:web/js' \
--add-data 'web/images/*:web/images' \
--noconsole --onefile \
app.py
# echo "hello"