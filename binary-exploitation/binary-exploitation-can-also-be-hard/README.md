# Tcache King

by Zafirr 

---

## Flag

```
COMPFEST12{Tcache_King_here_is_your_crown_WwW_5ef79c}
```

## Description
hahah Tcache go brrr

## Attachment

* share/
* Dockerfile
* docker-compose
* libc.so.6

Ini semua dizip. Upload ke google docs dan CTFd.

## Difficulty
Hard

## Hint
Its the house of botcake and overlapping chunks 2. With a sprinkle of leakless and PIE lol get rekt.

## Deployment
How to compile:

`gcc tcache_king.c -o tcache_king -O2 -D\_FORTIFY\_SOURCE=2 -fstack-protector-all -Wl,-z,now,-z,relro -Wall -no-pie`<br>

Workdir di /home/compfest12

Jalanin:<br>
`./tcache_king`

## Note

* Gunakan ubuntu 20.04