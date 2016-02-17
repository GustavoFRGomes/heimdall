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
