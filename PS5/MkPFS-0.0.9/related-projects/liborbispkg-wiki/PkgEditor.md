# PkgEditor

PkgEditor is a GUI tool. You can work with GP4 projects, PKG files, and SFO files.

Usage guide:
* [Creating PKGs with GP4 Projects](#creating-pkgs-with-gp4-projects)
* [Opening PKGs](#opening-pkgs)
* [Editing SFO Files](#editing-sfo-files)

## Creating PKGs with GP4 Projects

The contents and layout of a PKG file are defined in GP4 project files. PkgEditor allows you to create and edit GP4 files. To create a GP4 project, click `File`->`New`->`GP4 Project`, and choose a name and location for your GP4 project. You can also open an existing project with `File`->`Open`.

PKGs require a content id, which should have the format
`XXXXXX-YYYY00000_00-ZZZZZZZZZZZZZZZZ`
and be exactly 36 characters long. This uniquely identifies the PKG and should not be shared between any two PKG files.

PKGs also require a passcode, but because we are making fake PKGs this passcode doesn't do anything to prevent people from accessing the PKG's files. You can still set a custom passcode if you want.

If you're making an additional content (DLC) fake PKG, you will need to enter an entitlement key. A default one of all zeroes is provided by default.

Add folders to the PKG by right-clicking in the file view (right side) and choosing `New Folder`. You can also drag a folder or files into this view, which will add the file or folder and its subfolders and files.

You can enter a Volume Timestamp which will be used as the file timestamp in the PFS image, and the Creation Date which will be put into the PARAM.SFO at build time. Checking the `Use time of build?` checkbox will override the creation date to whatever the current time is when you build the PKG. Checking the `Include time?` checkbox will include the date and time in the creation date, while leaving it unchecked will leave just the date (day/month/year).

All PKGs need a param.sfo file in the `Image0/sce_sys` directory. You should create an SFO with `File`->`New`->`SFO File`, create the SFO, and then add it to the `Image0/sce_sys` directory by dragging and dropping into the file view.

Click `Build PKG` when you're done adding files. It will ask for an output filename, the default is the content id.

The Build PFS button is for debugging purposes, you can probably ignore that.

## Opening PKGs

Click `File`->`Open` and select your PKG file.
Double click on the PARAM_SFO entry in the Entries tab to open it in a new tab.
Browse and extract files in the Files tab. Right click files to extract.

## Editing SFO Files

Click `File`->`Open` to open an existing SFO file, or click `File`->`New`->`SFO File` to create a new one.

A user-friendly editor is currently being worked on. You can click the `Defaults`->`Load <..> defaults` buttons to get a template for an AC or GD game package. Click on a key/value pair in order to modify it. The changes are reflected in real time in the table. There is not currently an undo feature, but changes are not written to the file until you press Ctrl-S or `File`->`Save`.
