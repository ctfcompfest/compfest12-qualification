# Boom Goes the Zip File!

by Zafirr

---

## Flag

```
COMPFEST12{2iP_f11e_Go35_kAAbo0ooOoOm_25a919}
```

## Description
Dont unpack it all! IT WILL BREAK YOUR COMPUTER!<br>
Remember, the flag matches the RegEx COMPFEST12{[A-z0-9_-]+}

## Attachment

* yang_ini_aman_diunzip
* README.txt

Ini semua dizip. Upload ke google docs dan CTFd.

## Difficulty
Hard

## Hint
This is the zip bomb I used https://www.bamsoftware.com/hacks/zipbomb/. However, I changed it a bit. I added another DEFLATE block. Since I mangled the "compressed size header" (except 1), only 1 file has the special letter (the flag letter). But thats not important, the flag letter is in that other DEFLATE block, thats all you need to know!

## Deployment
None!

## Note
None!