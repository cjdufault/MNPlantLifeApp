import dnr_apis as dnr

sna_search = dnr.search("hastings")

for i in range(len(sna_search)):
    dnr.sna_details_request(sna_search[i])

    print(i)
    print(sna_search[i].id)
    print(sna_search[i].name)
    print(sna_search[i].county)
    print(sna_search[i].coordinates_box)
    print(sna_search[i].notes)
    print(sna_search[i].tags)
    print(sna_search[i].desc)
    print(sna_search[i].directions)

    for item in sna_search[i].trees_shrubs:
        print(item)
    for item in sna_search[i].grasses:
        print(item)
    for item in sna_search[i].wildflowers:
        print(item)
    print()

all_snas = dnr.search("")

for i in range(len(all_snas)):
    print(str(i) + " " + all_snas[i].id + " " + all_snas[i].name)
