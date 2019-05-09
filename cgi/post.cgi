(uuid.ps) run
(psql.ps) run
(faustlib.ps) run
(fdf.ps) run

newpath 0 0 moveto
(Content-Type: text/plain
Status: 204 No Response
) show

/parsereceiver {
	[ exch {(,) search {exch pop exch}{exit} ifelse} loop]
} bind def

/accessqry {
	sqlescapestring
	(INSERT INTO access_table \(user_id, post_id\) VALUES \(\(SELECT user_id FROM user_table WHERE username = ) exch
	(\), ) postid (\);) 4 {concatstrings} repeat sqlgetrow
} bind def

(HTTP_COOKIE) getenv {
	(=) search pop pop pop dup
	() eq not {
		checksession dup
		() eq not {
			/username exch def
			/formdata parsefdf def

			{0 -20 rmoveto} dup exec /content /receiver {formdata exch get show} dup 3 1 roll exec 3 -1 roll exec exec

			0 -20 rmoveto
			(INSERT INTO post_table \(post, posted, user_id\) VALUES \() formdata /content get sqlescapestring
			(, now\(\), \(SELECT user_id FROM user_table WHERE username = ) username sqlescapestring
			(\)\) RETURNING post_id;) 4 {concatstrings} repeat sqlgetrow /postid exch def

			formdata /receiver get parsereceiver {accessqry} forall
			username accessqry
		} if
	} if
} if

showpage quit
