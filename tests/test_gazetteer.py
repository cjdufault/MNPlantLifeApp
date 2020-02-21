import dnr_apis as dnr

count = 0

results = dnr.sna_search("")
for result in results:
    print(count)
    print(result.id)
    print(result.name)
    print(result.county)
    print(result.coordinates_box)
    print()
    count += 1
