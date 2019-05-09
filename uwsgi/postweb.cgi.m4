[uwsgi]
plugins = cgi
processes = 1
threads = 4
cgi = SERVICEDIR/cgi/
cgi-helper = .cgi=SERVICEDIR/bin/postweb
http-socket = localhost:5001
master = true
http-socket-modifier1 = 9
