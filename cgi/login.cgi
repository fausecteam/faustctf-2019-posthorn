(uuid.ps) run
(psql.ps) run
(faustlib.ps) run
(fdf.ps) run


(HTTP_COOKIE) getenv {
	(=) search pop pop pop
}{
	genuuid
} ifelse /session exch def


newpath 0 0 moveto
(Set-Cookie: SessionId=) session (
Content-Type: application/vnd.fdf

%FDF-1.2
1 0 obj
<<
  /FDF
  <<
    /F
    \() (/index.cgi) completeurl (\)
  >>
>>
endobj

trailer
<</Root 1 0 R>>
%%EOF
) 4 {concatstrings} repeat show

0 -30 rmoveto

/formdata parsefdf def
%formdata /username get show
0 -20 rmoveto
%formdata /password get show
0 -20 rmoveto

/checkpassword
{
	sqlescapestring (SELECT password FROM user_table WHERE username = ) exch (;) 2 {concatstrings} repeat sqlgetrow eq
} bind def

formdata /password get formdata /username get checkpassword
{
	(UPDATE user_table SET session = ) session sqlescapestring ( WHERE username = ) formdata /username get sqlescapestring (;) 4 {concatstrings} repeat sqlgetrow
} if

showpage
quit
