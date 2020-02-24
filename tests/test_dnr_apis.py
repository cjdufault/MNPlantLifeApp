import dnr_apis as dnr

sna_search = dnr.search("hastings")

for i in range(len(sna_search)):
    dnr.sna_details_request(sna_search[i])

    print(i)
    print(sna_search[i].get_id())
    print(sna_search[i].get_name())
    print(sna_search[i].get_county())
    print(sna_search[i].get_coordinates_box())
    print(sna_search[i].get_notes())
    print(sna_search[i].get_tags())
    print(sna_search[i].get_desc())
    print(sna_search[i].get_directions())

    for item in sna_search[i].get_trees_shrubs():
        print(item)
    for item in sna_search[i].get_grasses():
        print(item)
    for item in sna_search[i].get_wildflowers():
        print(item)
    print()

all_snas = dnr.search("")

for i in range(len(all_snas)):
    print(str(i) + " " + all_snas[i].get_id() + " " + all_snas[i].get_name())
