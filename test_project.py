from project import human_parser, Minerals, human, food_plan_for_a_day     
import requests

def test_human_parser():
    """Test command line arguments"""

    assert human_parser(9, "f", None) == ("female", 9)
    assert human_parser(8.5, "m", "k") == ("child", 8)
    assert human_parser(85.35, "m", "j") == ("male", 85)
    assert human_parser(0.356, "f", None) == ("baby", 0.4)
    assert human_parser(35.6, "f", "p") == ("femalep", 35)
    assert human_parser(35.6, "f", "n") == ("female", 35)
    assert human_parser(25.3, "f", "l") == ("femalel", 25)
    assert human_parser(55.6, "f", None) == ("female", 55)
    assert human_parser(55.6, "f", "khv") == ("female", 55)
    assert human_parser(5, None, None) == ("child", 5)

    # Wrong command line arguments
    assert human_parser(-9, "f", None) == None
    assert human_parser(35.6, "f", "d") == None
    assert human_parser(35.6, "f", None) == None


def test_count_mineral_norm_for_person():
    """Test for determining the daily requirement of minerals for a person from a csv file"""

    assert Minerals.count_mineral_norm_for_person(("female", 9), "Chromium, Cr (µg)") == 21
    assert Minerals.count_mineral_norm_for_person(("child", 8), "Copper, Cu (mg)") == 0.440
    assert Minerals.count_mineral_norm_for_person(("male", 85), "Fluoride, F (µg)") == 4000
    assert Minerals.count_mineral_norm_for_person(("baby", 0.4), "Iodine, I (µg)") == 110
    assert Minerals.count_mineral_norm_for_person(("femalep", 35), "Iron, Fe (mg)") == 27
    assert Minerals.count_mineral_norm_for_person(("female", 35), "Manganese, Mn (mg)") == 1.8
    assert Minerals.count_mineral_norm_for_person(("femalel", 25), "Molybdenum, Mo (µg)") ==50
    assert Minerals.count_mineral_norm_for_person(("female", 55), "Selenium, Se (µg)") == 55
    assert Minerals.count_mineral_norm_for_person(("child", 5), "Zinc, Zn (mg)") == 5


def test_human(monkeypatch):
    """Test user inputs checking"""
    responses = iter(["5"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("child", 5)

    responses = iter(["10", "m"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("male", 10)

    # Wrong age input test
    responses = iter(["-9", "g", "0", "80.56", "m"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("male", 80)

    # Wrong gender input test
    responses = iter(["10", "l", "", "22", "f"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("female", 10)

    # Wrong additional inf-n about female
    responses = iter(["14", "f", "ghhj", "5", "", "n"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("female", 14)

    responses = iter(["60", "f"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("female", 60)

    responses = iter(["0.36"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("baby", 0.4)

    responses = iter(["20.6", "f", "l"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    assert human() == ("femalel", 20)


def test_food_plan_for_a_day(monkeypatch):
    """Test user inputs checking and yielding results"""
    # Class for mocking request responses
    class MockResponse(object):
        def __init__(self):
            self.status_code = 200

        def json(self):
            return {'foods': [{"description": "Red apple", "foodCategory": "apple"}, 
                               {"description": "Green apple", "foodCategory": "apple"}, 
                               {"description": "Green apple", "foodCategory": "apple"}
                               ]}
    # Creates mocking object
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    # User inputs
    responses = iter(["apple", "", "-88", "hfj", "111.5", "gzj", "", "55", "3", "hg", "85", "n", "lemon", 96, "1", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    # List to append yields
    list_of_yields = []
    for food in food_plan_for_a_day():
        list_of_yields.append(food)

    assert list_of_yields == [({"description": "Green apple", "foodCategory": "apple"}, 111.5), 
                                     ({"description": "Red apple", "foodCategory": "apple"}, 96)]
