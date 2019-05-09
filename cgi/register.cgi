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
(Content-Type: text/plain
Set-Cookie: SessionId=) session (
Status: 204 No Response
) 2 {concatstrings} repeat show

0 -30 rmoveto

/formdata parsefdf def
formdata /username get show
0 -20 rmoveto
formdata /password get show
0 -20 rmoveto

/checkuserexists
{
	sqlescapestring (SELECT username FROM user_table WHERE username = ) exch (;) 2 {concatstrings} repeat sqlgetrow
} bind def

formdata /username get dup checkuserexists eq not
{
	(INSERT INTO user_table \(username, password\) VALUES \() formdata /username get sqlescapestring (,) formdata /password get sqlescapestring (\);) 4 {concatstrings} repeat sqlgetrow
} if

showpage
quit
