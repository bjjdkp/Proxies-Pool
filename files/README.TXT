___________________________________________________________________
  
APNIC ALLOCATION AND ASSIGNMENT REPORTS
 (version 2.0 5 January 2004)
___________________________________________________________________


Contents:

 1. About these reports
 2. Conditions of use
 3. Statistics format




1.	ABOUT THESE REPORTS
____________________________________________________________________

The directory ftp://ftp.apnic.net/pub/stats/apnic/ contains 
daily summary reports of the allocations and assignments of numeric 
Internet address resources within ranges originally delegated to 
APNIC and historical ranges transferred to APNIC by other 
registries.

The resources reported are:

	- IPv4 address ranges (IPv4)
	- IPv6 address ranges (IPv6)
	- Autonomous System Numbers (ASNs)

These reports are produced as part of a joint Regional Internet 
Registry (RIR) project to provide consistent and accessible 
Internet resource statistics to the global community. It is hoped
these reports will lead to increased research and analysis of the 
global use of address resources. 

For detailed information on the RIR statistics exchange format, 
see:

    http://www.apnic.net/db/rir-stats-format.html



2.	CONDITIONS OF USE
____________________________________________________________________


The files are freely available for download and use on the condition 
that APNIC will not be held responsible for any loss or damage 
arising from the use of the information contained in these reports.

APNIC endeavours to the best of its ability to ensure the accuracy 
of these reports; however, APNIC makes no guarantee in this regard.

In particular, it should be noted that these reports seek to 
indicate where resources were first allocated or assigned. It is not
intended that these reports be considered as an authoritative 
statement of the location in which any specific resource may 
currently be in use.

		

3.	STATISTICS FORMAT
____________________________________________________________________
		


3.1 	File names
------------------


Each file is named using the format:

	delegated-apnic-<yyyymmdd>

The most recent file will also be available under the name:

	delegated-apnic-latest
    


3.2	File format
-------------------

The file consists of: 

	- comments
	- file header lines
	- records

Header and record lines are structured as 'comma separated fields'
(CSV). Leading and trailing blank text in fields not meaningful.

The vertical line character '|' (ASCII code 0x7c) is used as the
CSV field separator.

After the header lines, records are not sorted.



3.2.1	Comments
----------------


Comments are denoted by # at the beginning of a line. No
line-embedded comments are permitted. Comments may occur at
any place in the file.

Example:

	#optional comments.
	#   any number of lines.

	#another optional comment.

Blank lines are permitted, and may occur at any place in the file.



3.2.2 	File header
-------------------


The file header consists of the version line and the summary
lines for each type of record. 


Version line
------------

Format:

	version|registry|serial|records|startdate|enddate|UTCoffset

Where:

	version  	format version number of this file, 
			currently 2;

	registry   	as for records and filename (see below);

	serial     	serial number of this file (within the
			creating RIR series);

	records    	number of records in file, excluding blank
			lines, summary lines, the version line and 
			comments;

	startdate  	start date of time period, in yyyymmdd 
			format;

	enddate    	end date of period in yyyymmdd format;
	
	UTCoffset  	offset from UTC (+/- hours) of local RIR
			producing file.



Summary line
------------

The summary lines count the number of record lines of each type in 
the file.

Format:

	registry|*|type|*|count|summary

Where:

	registry   	as for records (see below);
	
	*          	an ASCII '*' (unused field, retained for
			spreadsheet purposes);
			
	type       	as for records (defined below);
	
	count      	sum of the number of record lines of this 
			type in	the file.
			
	summary    	the ASCII string 'summary' (to distinguish 
			the record line);


Note that the count does not equate to the total amount of resources
for each class of record. This is to be computed from the records
themselves.



3.2.3 	Records
---------------

After the defined file header, and excluding any space or comments,
each line in the file represents a single allocation (or assignment)
of a specific range of Internet number resources (IPv4, IPv6 or
ASN), made by the RIR identified in the record.

IPv4  records may represent non-CIDR ranges or CIDR blocks, and 
therefore the record format represents the beginning of range, and a
count. This can be converted to prefix/length using simple algorithms.

IPv6 records represent the prefix and the count of /128 instances 
under that prefix.

Format:

	registry|cc|type|start|value|date|status[|extensions...]

Where:

	registry  	The registry from which the data is taken.
			For APNIC resources, this will be:

			    apnic

	cc        	ISO 3166 2-letter code of the organisation to
	                which the allocation or assignment was made. 

	type      	Type of Internet number resource represented
			in this record. One value from the set of 
			defined strings:

			    {asn,ipv4,ipv6}

	start     	In the case of records of type 'ipv4' or
			'ipv6' this is the IPv4 or IPv6 'first
			address' of the	range.

			In the case of an 16 bit AS number, the
			format is the integer value in the range:
			
			    0 - 65535
			
			In the case of a 32 bit ASN,  the value is
			in the range:
			
			    0 - 4294967296
			    
		    	No distinction is drawn between 16 and 32
		    	bit ASN values in the range 0 to 65535.

	value     	In the case of IPv4 address the count of
			hosts for this range. This count does not 
			have to represent a CIDR range.

			In the case of an IPv6 address the value 
			will be the CIDR prefix length from the 
			'first address'	value of <start>.
			
			In the case of records of type 'asn' the 
			number is the count of AS from this start 
			value.

	date      	Date on this allocation/assignment was made
			by the RIR in the format:
			
			    YYYYMMDD

			Where the allocation or assignment has been
			transferred from another registry, this date
			represents the date of first assignment or
			allocation as received in from the original
			RIR.

			It is noted that where records do not show a 
			date of	first assignment, this can take the 
			0000/00/00 value.

    	status    	Type of allocation from the set:

                            {allocated, assigned}

                	This is the allocation or assignment made by 
                	the registry producing the file and not any
                	sub-assignment by other agencies.

   	extensions 	In future, this may include extra data that 
   			is yet to be defined.



3.3 	Historical resources
----------------------------


Early Registration Transfers (ERX) and AUNIC legacy records do not
have any special tagging in the statistics reports. 



____________________________________________________________________


If you any questions or comments about these reports, please contact
<technical@apnic.net>

____________________________________________________________________
