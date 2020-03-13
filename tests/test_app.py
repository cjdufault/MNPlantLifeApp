import app
import requests
import dnr_apis


base_url = "https://cdufault.pythonanywhere.com/"   # the url the site is hosted at
all_snas = dnr_apis.sna_list_request()


def main():
    print("Running tests on app.py...")
    test_search()
    test_plant_pages()
    test_sna_pages()
    print("All tests on app.py passed!")


def test_search():
    print("Running test on search()...")

    search_term = "Blaine"
    expected_matches = ["Blaine Airport Rich Fen SNA", "Blaine Preserve SNA"]
    actual_matches = app.search(search_term)
    assert actual_matches == expected_matches, f"Search test failed: expected {expected_matches}, got {actual_matches}"
    print("\tsearch() test passed!")


def test_plant_pages():
    print("Running tests on Plant pages...")
    test_sci_name = "Achillea millefolium"
    test_common_name = "common yarrow"

    # test getting a page w/ both sci_name and common_name
    response = requests.get(f"{base_url}plant?sci_name={test_sci_name}&common_name={test_common_name}")
    assert response.status_code == 200, "Loading a plant page with scientific and common names failed"

    # test getting a page w/ just a sci_name
    response = requests.get(f"{base_url}plant?sci_name={test_sci_name}")
    assert response.status_code == 200, "Loading a plant page just a scientific name failed"

    # test getting a page w/ sci and common names reversed due to a data entry error
    response = requests.get(f"{base_url}plant?sci_name={test_common_name}&common_name={test_sci_name}")
    assert response.status_code == 200, "Loading a plant page with scientific and common names reversed failed"
    print("\tPlant pages tests passed!")


def test_sna_pages():
    print("Running tests on SNA pages...")

    # to check if requested names get properly capitalized
    response = requests.get(f"{base_url}sna/cLINTON fALLS dWARF tROUT lILY sna")
    assert response.status_code == 200, "Failed to correct for improperly capitalized SNA names"

    # to check if requested names w/o "SNA" at the end get it added properly
    response = requests.get(f"{base_url}sna/Hastings")
    assert response.status_code == 200, "Failed to correct for SNA names w/o \"SNA\" at the end"

    # request every SNA page to test that none of them raise any errors
    for sna_name in all_snas.keys():
        response = requests.get(f"{base_url}sna/{sna_name}")
        assert response.status_code == 200, f"Failed to load SNA page for {sna_name}"
    print("\tSNA pages tests passed!")


if __name__ == '__main__':
    main()