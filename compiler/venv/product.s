.text
main:
	li.s $f10, 5.5
	li.s $f11, 4.2
	add.s $f0, $f10, $f11
	mov.s $f12, $f0
	li $v0, 2
	mov.s $f12, $f12
	syscall
	j END
END:
.data
	true: .byte 1
	false: .byte 0
	fraction5.5: .float 5.5
	fraction4.2: .float 4.2
