#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <linux/random.h>

int main(int argc, char** argv) {

	char* method = getenv("REQUEST_METHOD");
	char* device = NULL;

	if (method == NULL) return -1;

	if (strcmp(method, "GET") == 0) {
		device = "-sDEVICE=pdfwrite";
		puts("Content-Type: application/pdf\n");
	} else {
		device = "-sDEVICE=txtwrite";
	}
	fflush(stdout);

	if (0 != execlp("gs", "gs", "-q", "-sOutputFile=%stdout%", device, "-sPAPERSIZE=a4", "-dNOPAUSE", argv[1], NULL)) {
		perror("Executing GhostScript");
	}
}
