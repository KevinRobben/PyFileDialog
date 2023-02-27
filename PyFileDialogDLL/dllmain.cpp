// dllmain.cpp : Defines the entry point for the DLL application.
#include <wchar.h>
#include "pch.h"
#include <windows.h>
#include <commdlg.h>
#include <Shobjidl.h>



#define DLL_EXPORT __declspec(dllexport)


extern "C" {

    DLL_EXPORT BOOL SaveFileDialog(HWND hWnd, LPWSTR pszFileNameBuffer, DWORD fileNameBufferSize, LPCWSTR pszTitle, LPCWSTR pszExtensionFilter, LPCTSTR defaultExtension);
                                    // (LPCTSTR filter, LPCTSTR defaultExtension, LPTSTR fileNameBuffer, DWORD fileNameBufferSize)

    BOOL SaveFileDialog(HWND hWnd, LPWSTR pszFileNameBuffer, DWORD fileNameBufferSize, LPCWSTR pszTitle, LPCWSTR pszExtensionFilter, LPCTSTR defaultExtension)
    {
        BOOL bResult = FALSE;

        // Initialize OPENFILENAME
        OPENFILENAME ofn = { 0 };
        ofn.lStructSize = sizeof(ofn);
        ofn.hwndOwner = hWnd;
        ofn.lpstrTitle = pszTitle ? pszTitle : nullptr;
        ofn.lpstrFile = pszFileNameBuffer;
        ofn.nMaxFile = fileNameBufferSize;
        ofn.lpstrFilter = pszExtensionFilter;
        ofn.lpstrDefExt = defaultExtension;
        ofn.Flags = OFN_EXPLORER | OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT;

        // Display the Open dialog box.
        if (GetSaveFileName(&ofn) == TRUE)
        {
            bResult = TRUE;
        }

        return bResult;
    }
    

    DLL_EXPORT BOOL PickFileDialog(HWND hWnd, LPWSTR pszSelectedFile, LPCWSTR lpstrTitle, LPCWSTR pszFileExtensions, BOOL allowMultiSelect);

    BOOL PickFileDialog(HWND hWnd, LPWSTR pszSelectedFile, LPCWSTR pszTitle, LPCWSTR pszFileExtensions, BOOL allowMultiSelect)
    {
        BOOL bResult = FALSE;

        // initialize the OPENFILENAME structure
        OPENFILENAME ofn = { 0 };
        ofn.lStructSize = sizeof(ofn);
        ofn.hwndOwner = hWnd;
        ofn.lpstrTitle = pszTitle ? pszTitle : nullptr;
        ofn.lpstrFile = pszSelectedFile;
        ofn.nMaxFile = MAX_PATH;
        ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR | OFN_CREATEPROMPT;
        if (allowMultiSelect) {
            ofn.Flags |= OFN_ALLOWMULTISELECT;
        }
        ofn.lpstrDefExt = L"";
        if (pszFileExtensions != nullptr) {
            ofn.lpstrFilter = pszFileExtensions;
        }

        // display the folder picker dialog
        if (GetOpenFileName(&ofn)) {
            bResult = TRUE;
        }

        return bResult;
    }




    DLL_EXPORT BOOL PickFolderDialog(HWND hWnd, LPWSTR pszSelectedFolder, LPCWSTR pszTitle);

    BOOL PickFolderDialog(HWND hWnd, LPWSTR pszSelectedFolder, LPCWSTR pszTitle)
    {
        BOOL bResult = FALSE;

        // initialize the COM library
        HRESULT hr = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
        if (SUCCEEDED(hr)) {
            // create the folder picker dialog object
            IFileOpenDialog* pFileOpenDialog;
            hr = CoCreateInstance(CLSID_FileOpenDialog, NULL, CLSCTX_ALL, IID_IFileOpenDialog, reinterpret_cast<void**>(&pFileOpenDialog));
            if (SUCCEEDED(hr)) {
                // set the options for the folder picker dialog
                FILEOPENDIALOGOPTIONS options;
                hr = pFileOpenDialog->GetOptions(&options);
                if (SUCCEEDED(hr)) {
                    options |= FOS_PICKFOLDERS;
                    hr = pFileOpenDialog->SetOptions(options);
                }

                // set the title of the folder picker dialog
                pFileOpenDialog->SetTitle(pszTitle ? pszTitle : nullptr);

                // display the folder picker dialog
                hr = pFileOpenDialog->Show(hWnd);
                if (SUCCEEDED(hr)) {
                    // get the selected folder path
                    IShellItem* pItem;
                    hr = pFileOpenDialog->GetResult(&pItem);
                    if (SUCCEEDED(hr)) {
                        PWSTR pszFilePath;
                        hr = pItem->GetDisplayName(SIGDN_FILESYSPATH, &pszFilePath);
                        if (SUCCEEDED(hr)) {
                            wcscpy_s(pszSelectedFolder, MAX_PATH, pszFilePath);
                            CoTaskMemFree(pszFilePath);
                            bResult = TRUE;
                        }
                        pItem->Release();
                    }
                }

                pFileOpenDialog->Release();
            }
            CoUninitialize();
        }

        return bResult;
    }

}

