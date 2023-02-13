[6027 ] jt   ra   ,6035           ; if (ra !=0 ) goto 6035
[6030 ] add  ra   ,rb   ,1        ; ra = (rb+1)%32768
[6034 ] ret                       ; return
[6035 ] jt   rb   ,6048           ; if (rb != 0) goto 6048
[6038 ] add  ra   ,ra   ,32767    ; ra = (ra + 32767) % 32768
[6042 ] set  rb   ,rh             ; rb = rh
[6045 ] call 6027                 ; goto 6027
[6047 ] ret                       ; return
[6048 ] push ra                   ; stack <- ra
[6050 ] add  rb   ,rb   ,32767    ; rb = (rb + 32767) % 32768
[6054 ] call 6027                 ; goto 6027
[6056 ] set  rb   ,ra             ; rb = ra
[6059 ] pop  ra                   ; stack -> ra
[6061 ] add  ra   ,ra   ,32767    ; ra = (ra + 32767) % 32768   
[6065 ] call 6027                 ; goto 6027
[6067 ] ret