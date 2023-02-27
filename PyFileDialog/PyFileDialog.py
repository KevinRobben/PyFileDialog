"""
pyfiledialog.file_dialog
~~~~~~~~~~~~~~~~~~~~~~~~~

A Python package for selecting files and folders using Windows file dialogs.

Usage:
save_file_dialog("txt")
pick_folder_dialog(title="Selecteer een folder")
pick_file_dialog(extensions=["txt", "js", "xlsx", "*"])
pick_file_dialog(extensions=["*", "txt", "js", "xlsx" ], multiselect=True)

"""

import ctypes
import os
from typing import List

# load the folder_picker file
my_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./PyFileDialog.dll")
# folder_picker = ctypes.WinDLL(my_path)

# C:/Users/Kevin Robben/source/repos/PyFileDialog/x64/Debug/PyFileDialog.dll
folder_picker = ctypes.WinDLL("C:/Users/Kevin Robben/source/repos/PyFileDialog/x64/Debug/PyFileDialog.dll")


# define the function parameters and return type
folder_picker.PickFolderDialog.argtypes = [
    ctypes.c_void_p,            # hWnd
    ctypes.c_wchar_p,           # pszSelectedFolder
    ctypes.c_wchar_p,           # pszTitle
]

folder_picker.PickFolderDialog.restype = ctypes.c_bool

# define the argument types for the PickFolderDialog function
folder_picker.PickFileDialog.argtypes = [
    ctypes.c_void_p,            # hWnd
    ctypes.c_wchar_p,           # pszSelectedFolder
    ctypes.c_wchar_p,           # pszTitle
    ctypes.c_wchar_p,           # pszFileExtensions
    ctypes.c_bool               # allow_multi_select
]
# define the return type for the PickFolderDialog function
folder_picker.PickFileDialog.restype = ctypes.c_bool

# define the argument types for the SaveFileDialog function
folder_picker.SaveFileDialog.argtypes = [
    ctypes.c_void_p,            # hWnd
    ctypes.c_wchar_p,           # pszFileNameBuffer
    ctypes.c_uint32,            # fileNameBufferSize
    ctypes.c_wchar_p,           # pszTitle
    ctypes.c_wchar_p,           # pszExtensionFilter
    ctypes.c_wchar_p            # defaultExtension

]
# define the return type for the SaveFileDialog function
folder_picker.SaveFileDialog.restype = ctypes.c_bool


# "TXT Files (*.txt)\0m*.csv\0All Files (*.*)\0*.*\0"
def get_filter_string(extensions: "List[str]", useFile=False):
    filter_str = ""
    text_str =  "file" if useFile else "files"
    for ext in extensions:
        if ext == "*" and useFile:
            ext_str = "Any"
        elif ext == "*":
            ext_str = "All"
        else:
            ext_str = ext.upper()
        filter_str += f"{ext_str} {text_str} (*.{ext})\0*.{ext}\0"
    return filter_str


def save_file_dialog(default_extension:str, title=None,  extensions_filter:"List[str]"=[]):

    file_name_buffer = ctypes.create_unicode_buffer(256)
    file_name_buffer_size = ctypes.sizeof(file_name_buffer)
    hWnd = 0 # or use the handle of your parent window

    if default_extension not in extensions_filter:
        extensions_filter.insert(0, default_extension)

    # build the file extensions string if specified
    extensions_str = get_filter_string(extensions_filter, True)

    for extension in extensions_filter:
        if extension[0] == ".":
            raise AttributeError("Do not include \".\" before a file extension ")
            

    result = folder_picker.SaveFileDialog(hWnd, file_name_buffer, file_name_buffer_size, title, extensions_str, default_extension)
    if result:
         return file_name_buffer.value
    else:
        return None


def pick_folder_dialog(title=None):
    # call the function
    pszSelectedFolder = ctypes.create_unicode_buffer(1024)
    hWnd = 0 # or use the handle of your parent window
    if folder_picker.PickFolderDialog(hWnd, pszSelectedFolder, title):
        return pszSelectedFolder.value
    else:
        return None


def pick_file_dialog(title=None, extensions=None, multiselect=False):

    for extension in extensions:
        if extension[0] == ".":
            raise AttributeError("Do not include \".\" before a file extension ")

    # create a buffer to hold the selected folder path
    selected_files = ctypes.create_unicode_buffer(1024)
    hWnd = 0 # or use the handle of your parent window
    # build the file extensions string if specified
    extensions_str = None
    if extensions is not None:
        extensions_str = get_filter_string(extensions)


    # call the PickFileDialog function
    result = folder_picker.PickFileDialog(hWnd, selected_files, title, extensions_str, multiselect)

    # return the selected folder path if successful
    if result:
        if multiselect:
            # split the buffer by the null character and filter out empty strings
            paths = []
            buffer_value = ctypes.addressof(selected_files)
            while True:
                filename = ctypes.wstring_at(buffer_value)
                if not filename:
                    break
                path = os.path.join(selected_files.value, filename)
                paths.append(path)
                buffer_value += len(filename) * 2 + 2

            # if the length is 1, there is one file. 
            # If the length > 1 the first index contains the directory path. Omit this
            if len(paths) > 1:
                paths.pop(0)
            return paths
        else:
            return selected_files.value
    else:
        return None




