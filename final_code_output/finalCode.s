	.data
	newline: .asciz "\n"
	.text
	Lstart:
	j Lmain
L0:
	sw ra,(sp)
L1:
	lw t1, -12(sp)
	lw t0, -4(sp)
	lw t0, -4(t0)
	addi t0, t0, -20
	lw t2, (t0)
	add t1, t1, t2
	sw t1, -16(sp)
L2:
	lw t1, -8(sp)
	lw t0, -16(sp)
	sw t0, (t1)
	lw ra, (sp)
	addi sp, sp, -20
	jr ra
L3:
	lw ra,(sp)
	addi sp, sp, -20
	jr ra
L4:
	sw ra,(sp)
L5:
	lw t1, -12(sp)
	lw t0, -4(sp)
	lw t0, -4(t0)
	addi t0, t0, -20
	lw t2, (t0)
	add t1, t1, t2
	sw t1, -16(sp)
L6:
	lw t1, -8(sp)
	lw t0, -16(sp)
	sw t0, (t1)
	lw ra, (sp)
	addi sp, sp, -20
	jr ra
L7:
	lw ra,(sp)
	addi sp, sp, -20
	jr ra
L8:
	sw ra,(sp)
L9:
	addi fp, sp, 20
	lw t0, -12(sp)
	sw t0, -12(fp)
L10:
	addi t0, sp, -16
	sw t0, -8(fp)
L11:
	lw t0, -4(sp)
	sw t0, -4(fp)
	addi sp, sp, 20
	jal L0
L12:
	lw t1, -8(sp)
	lw t0, -16(sp)
	sw t0, (t1)
	lw ra, (sp)
	addi sp, sp, -20
	jr ra
L13:
	lw ra,(sp)
	addi sp, sp, -20
	jr ra
L14:
	sw ra,(sp)
L15:
	addi fp, sp, 20
	lw t0, -12(sp)
	sw t0, -12(fp)
L16:
	addi t0, sp, -16
	sw t0, -8(fp)
L17:
	sw sp, -4(fp)
	addi sp, sp, 20
	jal L8
L18:
	addi fp, sp, 20
	lw t0, -12(sp)
	sw t0, -12(fp)
L19:
	addi t0, sp, -20
	sw t0, -8(fp)
L20:
	sw sp, -4(fp)
	addi sp, sp, 20
	jal L0
L21:
	lw t1, -16(sp)
	lw t2, -20(sp)
	add t1, t1, t2
	sw t1, -24(sp)
L22:
	addi fp, sp, 20
	lw t0, -12(sp)
	sw t0, -12(fp)
L23:
	addi t0, sp, -28
	sw t0, -8(fp)
L24:
	sw sp, -4(fp)
	addi sp, sp, 20
	jal L4
L25:
	lw t1, -24(sp)
	lw t2, -28(sp)
	add t1, t1, t2
	sw t1, -32(sp)
L26:
	lw t1, -8(sp)
	lw t0, -32(sp)
	sw t0, (t1)
	lw ra, (sp)
	addi sp, sp, -36
	jr ra
L27:
	lw ra,(sp)
	addi sp, sp, -36
	jr ra
L28:
	sw ra,(sp)
L29:
	li t1, 32
	sw t1, -16(sp)
L30:
	li t1, 32
	sw t1, -20(sp)
L31:
	addi fp, sp, 36
	lw t0, -16(sp)
	sw t0, -12(fp)
L32:
	addi t0, sp, -24
	sw t0, -8(fp)
L33:
	sw sp, -4(fp)
	addi sp, sp, 36
	jal L14
L34:
	lw t1, -24(sp)
	sw t1, -12(sp)
L35:
	lw a0, -12(sp)
	li a7,1
	ecall
	la a0, newline
	li a7,4
	ecall
L36:
	lw ra,(sp)
	addi sp, sp, -28
	jr ra
	Lmain:
L37:
	addi sp, sp, 28
	jal L28
L38:
	li a0, 0
	li a7, 93
	ecall
