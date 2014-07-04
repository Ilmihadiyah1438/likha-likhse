def brevity(file_name, home = '/sdcard/',
	        ext = '.txt'):
    fi = file_name
    if fi[0] != '/':
        fi = home + fi
        len_ext = len(ext)
        if fi[-len_ext:] != ext:
            fi = fi + ext
    return fi