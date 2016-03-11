/*
 * Protocol Module to check for the protocol of the packets. It will grab info
 * on the protocol and other useful features to check for the use of flagged
 * protocols (possibly unsecure ones).
 */

/* #include "protocol.h" */

typedef struct
{
	char *name;
	char *header;
} PROTOCOL;

char checkprotocol(const char* recvd, const char *template)
{
	// This functin will check if the template is in the received data packet.

	if(strstr(recvd, template) == NULL)
		return 1;

	return 0;
}

PROTOCOL unknownProtocol()
{
	// Whenever there is a unknonw protocol this is it.
	PROTOCOL *unknown = (PROTOCOL*)malloc(sizeof(PROTOCOL));
	unknown.name = (char*)malloc(sizeof(char)*7);

	unknown.name = "UNKNOWN";
	unknown.header = NULL;
	return unknown;
}

PROTOCOL protocolID(const char* packet, const PROTOCOL list[], int list_size)
{
	// check for a list of protocols.
	int i;

	for(i=0; i<list_size; i++)
	{
		if(checkprotocol(packet, list[i].header))
			return list[i];
	}
	return unknownProtocol();
}
