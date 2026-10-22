# Parser field notes

A bug report from @nightshift_404 on X (https://x.com/nightshift_404)
showed that `user=batch_worker` loses its user field when imported from the
queue service. The same record with `user=batch-worker` works. Reproduce
with the sample service log before changing the username expression.

The timestamp and severity fields still parse correctly. Keep the raw
message intact so existing exports remain usable while this is fixed.
