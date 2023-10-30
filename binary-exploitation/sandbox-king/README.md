# Sandbox King

by Zafirr 

---

## Flag

```
COMPFEST12{C0nGr4TTSSS_U_r_D_SssssssssAnd60X_K111ng9g99_1c7dbf}
```

## Description
You have to get a shell. The seccomp is easy to bypass right?

## Attachment

* share/files/
* Dockerfile
* docker-compose
* xinetd

Ini semua dizip. Upload ke google docs dan CTFd.

## Difficulty
Hard

## Hint
1. /proc/$pid/mem, /proc/$pid/stat, /proc/$pid/maps are your friends <br>
2. The child is a lost cause, get RCE on the PARENT process.

Hint kedua dikeluarin 4 jam setelah soal dipublish jika dan hanya jika solve kurang dari 3 (Extreme case)

## Deployment
How to compile:

`gcc king.c -o king -O2 -D\_FORTIFY\_SOURCE=2 -fpie -Wl,-pie -fstack-protector-all -Wl,-z,now,-z,relro -Wall -Wextra -Werror`<br>
`gcc sandbox.c -o sandbox -O2 -D\_FORTIFY\_SOURCE=2 -fpie -Wl,-pie -fstack-protector-all -Wl,-z,now,-z,relro -Wall -Wextra -Werror`<br>
`gcc readFlag.c -o readFlag -O2 -D\_FORTIFY\_SOURCE=2 -fpie -Wl,-pie -fstack-protector-all -Wl,-z,now,-z,relro -Wall -Wextra -Werror`

readFlag chmod 555 tambahkan setuid bit. <br>
flag.txt chmod 400

Workdir di /home/compfest12

Jalanin:<br>
`./king` untuk king tanpa debugger ("seccomp")<br>
`./sandbox king` untuk king dengan debugger

## Note

* Buat Deployment: Ntar buat instance baru (iya server total yang baru wkwkwk), set /proc/sys/kernel/yama/ptrace_scope jadi 0.