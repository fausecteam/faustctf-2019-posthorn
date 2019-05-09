SERVICE := posthorn
DESTDIR ?= dist_root
SERVICEDIR ?= /srv/$(SERVICE)

.PHONY: build install

build:
	$(MAKE) -C src
	m4 -DSERVICEDIR=$(SERVICEDIR) uwsgi/posthorn.ini.m4 > uwsgi/posthorn.ini

install: build
	install -d -m 755 $(DESTDIR)/etc/uwsgi/apps-enabled/
	install -d -m 755 $(DESTDIR)/etc/nginx/sites-enabled/
	install -d -m 755 $(DESTDIR)/etc/systemd/system/
	install -d -m 755 $(DESTDIR)$(SERVICEDIR)/bin/
	install -d -m 755 $(DESTDIR)$(SERVICEDIR)/cgi/
	install -m 755 src/postweb $(DESTDIR)$(SERVICEDIR)/bin/postweb
	install -m 444 uwsgi/posthorn.ini $(DESTDIR)/etc/uwsgi/apps-enabled/
	install -m 444 nginx/posthorn     $(DESTDIR)/etc/nginx/sites-enabled/
	install -m 444 systemd/posthorn-database-setup.service $(DESTDIR)/etc/systemd/system/
	install -m 555 setup.sh   $(DESTDIR)$(SERVICEDIR)
	install -m 444 schema.sql $(DESTDIR)$(SERVICEDIR)
	install -m 444 cgi/*.cgi $(DESTDIR)$(SERVICEDIR)/cgi/
	install -m 444 cgi/*.ps  $(DESTDIR)$(SERVICEDIR)/cgi/
	install -m 644 BUGS.md   $(DESTDIR)$(SERVICEDIR)
