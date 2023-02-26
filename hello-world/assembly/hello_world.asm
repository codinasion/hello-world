section .data
    msg db 'Hello, world!',0

section .text
    global _start

_start:
    ; write the message to standard output
    mov eax, 4      ; system call for "write"
    mov ebx, 1      ; file descriptor for standard output
    mov ecx, msg    ; address of message to write
    mov edx, 13     ; number of bytes to write
    int 0x80        ; call the kernel

    ; exit the program with a status of 0
    mov eax, 1      ; system call for "exit"
    xor ebx, ebx    ; status code of 0
    int 0x80        ; call the kernel
