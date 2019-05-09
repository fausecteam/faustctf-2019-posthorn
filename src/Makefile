CFLAGS ?= -Wall -Werror -fstack-protector-strong

all: postweb postweb.gnu postweb.diet

postweb: postweb.diet
	cp $^ $@

postweb.gnu: postweb.c
	$(CC) -o $@ $^ $(CFLAGS)

postweb.diet: postweb.c
	diet $(CC) -s -o $@ $^ $(CFLAGS)
