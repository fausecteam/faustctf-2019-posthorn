[uwsgi]
plugins = cgi
processes = 1
threads = 4
cgi = SERVICEDIR/cgi/
cgi-helper = .cgi=SERVICEDIR/bin/postweb
uid = posthorn
gid = posthorn
