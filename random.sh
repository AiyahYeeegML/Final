#!/bin/bash
INPUT=./data/enrollment_test.csv
OUTPUT=./out/random_out.csv

mkdir ./out
rm -f $OUTPUT
for i in `cat $INPUT | grep "^[0-9]" | awk -F',' '{print $1}'`; do echo "$i,$(($RANDOM%2))" >> $OUTPUT; done
