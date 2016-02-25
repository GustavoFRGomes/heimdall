/*
 * Protocol Module to check for the protocol of the packets. It will grab info
 * on the protocol and other useful features to check for the use of flagged
 * protocols (possibly unsecure ones).
 */

#include "protocol.h"

typedef struct
{
	char *name;
	char *header;
} PROTOCOL;

char checkprotocol(const char* recvd, const char *template)
{
	// This functin will check if the template is in the received data packet.
	
	if (strstr(recvd, template) == NULL)
		return 1;

	return 0;
}
