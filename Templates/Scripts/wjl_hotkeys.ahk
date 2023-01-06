; ===============================
; HOTSTRINGS - Math, etc
; ===============================


::]tf::{U+2234} ; therefore
::]1/2::{ASC 171} ; 1/2
::]1/4::{ASC 172} ; 1/4
::]3/4::{U+00BE}
::]1/3::{U+2153}
::]2/3::{U+2154}
::]1/8::{U+215B}
::]3/8::{U+215C}
::]5/8::{U+215D}
::]7/8::{U+215E}
::]1/16::{U+00B9}{U+2044}{U+2081}{U+2086}
::]3/16::{U+00B3}{U+2044}{U+2081}{U+2086}
::]5/16::{U+2075}{U+2044}{U+2081}{U+2086}
::]7/16::{U+2077}{U+2044}{U+2081}{U+2086}
::]9/16::{U+2079}{U+2044}{U+2081}{U+2086}
::]11/16::{U+00B9}{U+00B9}{U+2044}{U+2081}{U+2086}
::]13/16::{U+00B9}{U+00B3}{U+2044}{U+2081}{U+2086}
::]15/16::{U+00B9}{U+2075}{U+2044}{U+2081}{U+2086}
::]inf::{ASC 236} ; infinity
::]+-::{ASC 241} ; plus/minus
::]>=::{ASC 242}
::]<=::{ASC 243}
::]~::{ASC 247}
::]deg::{ASC 248}
::]<>::{U+2260}

; You should be PROUD to be GREEK!
::]ag::{U+03B1}
::]bg::{U+03B2}
::]gg::{U+03B3}
::]dg::{U+03B4}
::]udg::{U+0394}
::]eg::{U+03B5}
::]fg::{U+1D719}
::]pg::{U+1D713}
::]wg::{U+1D6DA}
::]uwg::{U+03A9}
::]zg::{U+03B6}
::]hg::{U+03B7}
::]tg::{U+03B8}
::]kg::{U+03BA}
::]lg::{U+03BB}
::]ulg::{U+039B}
::]mg::{U+03BC}
::]ng::{U+03BD}
::]pi::{U+1D745}
::[rg::{U+03C1}
::]sg::{U+03C3}
::]usg::{U+03A3}
::]tg::{U+1D70F}

; Engineering
::]dia::{U+2300}
::]ib::{U+2336}
::]cl::{U+2104}
::]pl::{U+214A}


; Arrows
::]up::{ASC 24}
::]dn::{ASC 25}
::]rt::{ASC 26}
::]lt::{ASC 27}
::]ccw::{U+21BA}
::]cw::{U+21BB}

; Punctuation/Markup
::]par::{ASC 20}
::]sec::{ASC 21}
::]bul::{ASC 7}
::]chk::{U+2714}
::]rev1::{U+2673}
::]rev2::{U+2674}
::]rev3::{U+2675}
::]rev4::{U+2676}
::]rev5::{U+2677}
::]rev6::{U+2678}
::]rev7::{U+2679}

; Math
::]sqrt::{U+221A}



::]wjl::{U+1D500}{U+1D4F3}{U+1D4F5}

; Symbols
::]info::{U+1F6C8}
::]flag::{U+1F6A9}
::]warn::{U+26A0}
::]poo::{U+1F4A9}
::]wflag::{U+2690}
::]blag::{U+2691}
::]eyes::{U+1F440}
::]tu::{U+4F44D}
::]td::{U+1F44E}



; SHAPES
::]wtri::{U+2583}
::]btri::{U+2582}


; ===============================
; HOTSTRINGS - Date & Time
; ===============================

:*:]dd::
FormatTime, CurrentDate,, yyyy-MM-dd
SendInput %CurrentDate%
return

:*:]d1::
FormatTime, CurrentDate,, yyyyMMdd
SendInput %CurrentDate%
return

::]d2::
FormatTime, CurrentDate,, M/dd/yyyy
SendInput %CurrentDate%
return

::]d3::
FormatTime, CurrentDate,, MM/dd/yy
SendInput %CurrentDate%
return

::]d4::
FormatTime, CurrentDate,, MMMM d, yyyy
SendInput %CurrentDate%
return

::]dt1::
FormatTime, CurrentDate,, yyyyMMdd_HHmm
SendInput %CurrentDate%
return


; ===============================
; Coding
; ===============================
:*:]cdpython::cd c:\users\wlynes\documents\python\


; ===============================
; Progress Bars
; ===============================

:*:]10p::{U+2588}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}
:*:]20p::{U+2588}{U+2588}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}
:*:]30p::{U+2588}{U+2588}{U+2588}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}
:*:]40p::{U+2588}{U+2588}{U+2588}{U+2588}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}
:*:]50p::{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2591}{U+2591}{U+2591}{U+2591}{U+2591}
:*:]60p::{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2591}{U+2591}{U+2591}{U+2591}
:*:]70p::{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2591}{U+2591}{U+2591}
:*:]80p::{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2591}{U+2591}
:*:]90p::{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2591}
:*:]100p::{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}{U+2588}