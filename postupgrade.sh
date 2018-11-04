#!/bin/sh

echo "<INFO> Copy back existing config files"
cp -v -r /tmp/REPLACELBPPLUGINDIR/* REPLACELBPCONFIGDIR/

echo "<INFO> Remove temporary folders"
rm -rf /tmp/REPLACELBPPLUGINDIR

exit 0
