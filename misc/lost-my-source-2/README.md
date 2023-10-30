# Lost My Source 2

by prajnapras19

---

## Flag

```
COMPFEST12{my_fri3nd_s4ys_s0rry_888144}
```

## Description
This time I make a simple program (and put the flag there) with python and build it as a standalone with [PyInstaller](https://www.pyinstaller.org/), but my friend just accidentally erased the source code (again)!


## Attachment
* share/

## Difficulty
Easy

## Hint
* You don't need to reverse it. My friend said you need an archive_viewer.

## Deployment
> Intentionally left empty

## Notes
Untuk menyelesaikan soal ini, dapat menggunakan archive_viewer dari pyinstaller sendiri. Penggunaan tool decompiler yang ada di internet telah dites dan tidak bisa digunakan di ubuntu, tapi belum dites di windows.<br>
Penggunaan `grep` tidak mampu mengambil flag pada binary file ini (baru dicek menggunakan `grep -a COMPFEST` dan `grep --text COMPFEST`.
