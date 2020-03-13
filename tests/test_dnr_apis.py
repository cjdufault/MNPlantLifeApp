import dnr_apis as dnr


# test that names and ids for all SNAs are being retrieved w/ sna_list_request()
all_snas = dnr.sna_list_request()
assert all_snas is not None, "sna_list_request() failed to return a dictionary"
assert len(all_snas) > 0, "Dictionary returned by sna_list_request() is empty"


for sna_name in all_snas.keys():

    # test that an ID is associated with every SNA
    assert all_snas[sna_name] is not None, f"No ID was found for {sna_name}"

    # test sna_details_request()
    sna_object = dnr.sna_details_request(all_snas[sna_name])
    assert sna_object is not None, f"sna_details_request(all_snas[{sna_name}]) failed to return an SNA object"
    assert sna_object.name is not None, f"Attributes for {sna_name} were not correctly populated"


# test that html tags are correctly removed from text
test_string = "Lorem <a href=''>ipsum</a> dolor sit amet"
expected_result = "Lorem ipsum dolor sit amet"
actual_result = dnr.remove_html_tags(test_string)
assert expected_result == actual_result, f"remove_html_tags() failed. \"{expected_result}\" was expected, " \
                                         f"but \"{actual_result}\" was the actual result"

print("All DNR API tests passed.")
