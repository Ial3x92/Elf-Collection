# LibOrbisPkg: The Library

The classes in the library live in the LibOrbisPkg namespace. Functionality for distinct filetypes is mostly kept to unique namespaces. The main namespaces are:

```C#
using LibOrbisPkg.GP4; // Classes for GP4 projects
using LibOrbisPkg.PKG; // Classes for PKG files
using LibOrbisPkg.PFS; // Classes for PFS files
using LibOrbisPkg.PlayGo; // Classes for PlayGo chunk.dat and manifest
using LibOrbisPkg.Rif; // Classes for license.dat and license.info
using LibOrbisPkg.SFO; // Classes for SFO files
using LibOrbisPkg.Util; // Various helper functionality (Crypto, keys, file IO helper classes, etc)
```

Note: the API is not yet stable, and is kind of clunky.