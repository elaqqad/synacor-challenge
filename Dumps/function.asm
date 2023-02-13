[6027 ] jt   ra    6035
[6030 ] add  ra    rb    1
[6034 ] ret
[6035 ] jt   rb    6048
[6038 ] add  ra    ra    32767
[6042 ] set  rb    rh
[6045 ] call 6027
[6047 ] ret
[6048 ] push ra
[6050 ] add  rb    rb    32767
[6054 ] call 6027
[6056 ] set  rb    ra
[6059 ] pop  ra
[6061 ] add  ra    ra    32767
[6065 ] call 6027
[6067 ] ret
