!cpu m65
!to "test.prg", cbm

* = $2001

!8 $12,$20,$0a,$00,$fe,$02,$20,$30,$3a,$9e,$20
!pet "$2014"
!8 $00,$00,$00

    ldx     #$C0
    txs    
    clv

    lda #$20
    sta $1C3
    lda #$14
    sta $1C2
    ldz #$14
    ldy #1
    lda ($02,sp),y
    asr 
    lda #$84
    asr 
halt:
    bra     halt