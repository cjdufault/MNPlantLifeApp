import dnr_apis as dnr

sna_search = dnr.search("hastings")

for sna in sna_search.keys():
    sna_id = sna_search[sna]
    sna_object = dnr.sna_details_request(sna_id)

    print(sna_object.id)
    print(sna_object.name)
    print(sna_object.county)
    print(sna_object.coordinates_box)
    print(sna_object.notes)
    print(sna_object.tags)
    print(sna_object.desc)
    print(sna_object.directions)

    for item in sna_object.trees_shrubs:
        print(item)
    for item in sna_object.grasses:
        print(item)
    for item in sna_object.wildflowers:
        print(item)
    print()
