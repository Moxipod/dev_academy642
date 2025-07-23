;enter the variabale to print it
;prints it untill the $
printchain macro x
	mov dx,offset x
	mov ah, 9h
	int 21h	
endm	
JUMPS
IDEAL
MODEL small
STACK 100h
DATASEG
include "applepic.asm"
; --------------------------
; Your variables here
; --------------------------
CODESEG
start:
	mov ax, @data
	mov ds, ax
; --------------------------
; Your code here
; --------------------------
	;prints it from the other file
	printchain apple
	
	
	
	;get input
	mov ah, 7h
	int 21h
	cmp al, 0
	
exit:
	mov ax, 4c00h
	int 21h
END start


