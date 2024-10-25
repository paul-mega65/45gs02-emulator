!cpu m65
!to "test.prg", cbm

* = $2001

!8 $12,$20,$0a,$00,$fe,$02,$20,$30,$3a,$9e,$20
!pet "$2014"
!8 $00,$00,$00
    
    lda #42
    jsr $FFD2
    inc $d020
    rts