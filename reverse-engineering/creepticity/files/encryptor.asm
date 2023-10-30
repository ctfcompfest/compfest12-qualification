; ----------------------------------------------------------------------------
; 
; To assamble and run:
;
;   nasm -f elf -F dwarf -g encryptor.asm && ld -m elf_i386 -s -o encryptor encryptor.o
;   ./encryptor [text file]
; ----------------------------------------------------------------------------

global  _start

section .bss
    text        resb 128

section .data
    key_num     db 42
    bufsize     db  128

section .text

_start:
    xor eax, eax
	xor ebx, ebx
	xor ecx, ecx
	xor edx, edx
    pop   ebx           ; argc
    pop   ebx           ; argv[0]
    pop   ebx           ; the first real arg, a filename
    mov   eax,  5
    mov   ecx,  0
    int   80h
    mov eax, 3
    mov ebx, eax
    mov ecx, text
    mov edx, bufsize
    int 80h
    mov ecx, eax
    mov eax, 6
    int 80h
    mov ebx, text   

enc_loop:
    xor eax, eax
    mov al, [ebx]
    mov ah, [key_num]
    xor al, ah
    cmp al, 97
    jb storestring
    sub al, 97
storestring:
    add al, 30
    mov BYTE [ebx], al
    ;sub al, ah
    xor al, ah
    cmp al, 128
    jb storekey
    sub al, 128
storekey:
    mov BYTE [key_num], al
    inc ebx
    loop enc_loop

    mov al, 0x20
    mov BYTE [ebx], al
    inc ebx
    push ebx

    mov ebx, text
    xor eax, eax
    mov al, [ebx]
    mov ah, [key_num]
    xor al, ah
    cmp al, 97
    jb storestring2
    sub al, 97
storestring2:
    add al, 30
    mov BYTE [ebx], al
    ;sub al, ah
    xor al, ah
    cmp al, 128
    jb storekey2
    sub al, 128
storekey2:
    mov BYTE [key_num], al

    pop ebx
    mov BYTE [ebx], al
    mov BYTE [ebx+1], 0xA

    mov ebx, 1
    mov eax,  4
    mov ecx,  text
    mov edx, bufsize
    int 80h

    mov eax, 1
    mov ebx, 0
    int 80h
