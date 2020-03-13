import trefle_api as trefle


test_species_name = "Achillea millefolium"


def main():
    print("Running tests on dnr_apis.py...")
    test_strip_sci_name_irregularities()
    result = test_species_request()
    plant_object = test_species_details_request(result[0])
    test_search(plant_object)
    print("All Trefle API tests passed!")


def test_strip_sci_name_irregularities():
    print("Testing strip_sci_name_irregularities()...")
    test_strings = ["Lorem var. ipsum", "Lorem subsp. ipsum", "Lorem sp.", "Lorem spp."]
    expected_string = "Lorem"

    # test that all of the strings, when run through strip_sci_name_irregularities(), come out as the expected string
    for string in test_strings:
        actual_string = trefle.strip_sci_name_irregularities(string)
        assert actual_string == expected_string, f"strip_sci_name_irregularities({string}) failed: " \
                                                 f"\"{expected_string}\" was expected, but {actual_string} " \
                                                 f"was the actual result"
    print("strip_sci_name_irregularities() test passed!")


def test_species_request():
    print("Testing species_request()...")

    # test getting basic data on a plant from the api
    result = trefle.species_request(test_species_name)
    assert result is not None, "species_request() failed to get data"
    assert len(result) > 0, "species_request returned data, but it was empty"
    print("species_request() tests passed!")
    return result


def test_species_details_request(result):
    print("Testing species_details_request()...")

    # test getting detailed data on a plant from the api and converting it into a Plant object
    plant_object = trefle.species_details_request(result)
    assert plant_object is not None, "species_details_request() failed to get data"
    assert plant_object.sci_name == test_species_name, "species_details_request() failed to convert data into " \
                                                       "a Plant object"
    print("species_details_request() tests passed!")
    return plant_object


def test_search(expected_plant_object):
    print("Testing search()...")

    # test that search() properly strings together the two request methods to return a Plant object
    actual_plant_object = trefle.search(test_species_name)
    assert expected_plant_object.common_name == actual_plant_object.common_name, \
        "search() failed to return the expected Plant object"
    print("search() test passed!")


if __name__ == '__main__':
    main()
