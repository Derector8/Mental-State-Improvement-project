#!/usr/bin/sh

echo "Loading regions json from API...";
curl -X GET "https://covid-api.com/api/regions" -H "accept: application/json" -o regions.json;
echo "Loading regions json from API completed";
