# Proof-Of-Concept for PostScript Remote Code Execution

Idea is simple: some fairly obvious Code injection problem. However the twiser
comes with the fact that you (a) need to inject code in postscript (b) need to
write postscript that does the dirty trick for you stealing the flags and
(c) properly escape PostScript to fix the problem

Status: Playing Around  
Also: Adoptable (I might not be having services this CTF so feel free to adopt)

## Setup

Ideally PostCGI, simple rust wrapper in source that does nothing fishy. Twitter
clone. We'll need to see how to write to persistent storage from postscript.

Stretch Goal: ActivityPub and federation

## Resources

https://www-cdf.fnal.gov/offline/PostScript/BLUEBOOK.PDF  
https://www.whoishostingthis.com/resources/postscript/  
http://paulbourke.net/dataformats/postscript/  
https://stackoverflow.com/questions/4663409/creating-a-pdf-hyperlink-with-postscript  