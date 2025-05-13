#!/bin/bash
set -e

sam delete \
    --no-prompts \
    --region us-east-1 \
    --stack-name global-table-writer

for region in  us-east-2 us-west-{1,2};
do
    sam delete \
        --no-prompts \
        --region ${region} \
        --stack-name global-table-reader-${region}
done
