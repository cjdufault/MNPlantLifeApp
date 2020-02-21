import dnr_apis as dnr

results = dnr.sna_search("hastings")
for sna in results:
    dnr.sna_details(sna)

for i in range(len(results)):
    print(i)
    print(results[i].get_id())
    print(results[i].get_name())
    print(results[i].get_county())
    print(results[i].get_coordinates_box())
    print(results[i].get_notes())
    print(results[i].get_tags())
    print(results[i].get_desc())
    print(results[i].get_directions())

    for item in results[i].get_trees_shrubs():
        print(item)
    for item in results[i].get_grasses():
        print(item)
    for item in results[i].get_wildflowers():
        print(item)
    print()
