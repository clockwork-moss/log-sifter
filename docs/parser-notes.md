# Parser field notes

Username fields accept ASCII letters, digits, hyphens and underscores.
Regression coverage includes queue-service usernames. Messages remain
verbatim, including unrecognized fields, for downstream analysis.

Input records start with an ISO timestamp, a supported uppercase severity,
and a message. Nonmatching lines increment the unparsed counter. Multiline
tracebacks are not joined to earlier records.
