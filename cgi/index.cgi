/loginpage {(loginpage.ps) run} bind def
/detialpage {(detailpage.ps) run} bind def
/header {(header.ps) run} bind def
/userpage {(userpage.ps) run} bind def

(uuid.ps) run
(psql.ps) run
(faustlib.ps) run
(forms.ps) run
(getparams.ps) run

parseget /getpar exch def
pagesetup

getpar /page known not {
	getpar /page (index) put
} if

(HTTP_COOKIE) getenv
{
	(=) search pop pop pop
	dup () eq {
		(malformed cookie) loginpage
	}{
		checksession /username exch def
		username () eq {
			(not logged in) loginpage
		}{
			userpage
		} ifelse
	} ifelse
}{
	(no session cookie) loginpage
} ifelse

showpage

quit
