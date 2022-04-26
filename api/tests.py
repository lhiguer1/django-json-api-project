from django.test import SimpleTestCase
from . import views

# Create your tests here.
class APITestCase(SimpleTestCase):
    def testPing(self):
        response = self.client.get('/api/ping', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'success': True})

    def testCharactersMissingParameter(self):
        response = self.client.get('/api/characters', follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'error': 'names parameter is required'})

    def testCharactersDuplicates(self):
        '''Test if search results are filtering duplicates'''
        data1 = {'names': 'walt,tod'}
        data2 = {'names': 'walt,tod,walt'}

        response1 = self.client.get('/api/characters', data=data1, follow=True)
        response2 = self.client.get('/api/characters', data=data2, follow=True)


        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1.status_code, response2.status_code)
        self.assertListEqual(response1.json(), response2.json())
        
    def testCharacters(self):
        data = {'names': 'walt,tod,henry'}
        expected_response = [{"char_id": 1, "name": "Walter White", "birthday": "09-07-1958", "occupation": ["Lab Assistant", "Enforcer", "Meth Cook"], "img": "https://images.amcnetworks.com/amc.com/wp-content/uploads/2015/04/cast_bb_700x1000_walter-white-lg.jpg", "status": "Presumed dead", "nickname": "Heisenberg", "appearance": [5], "portrayed": "Bryan Cranston", "category": "Breaking Bad", "better_call_saul_appearance": []}, {"char_id": 4, "name": "Walter White Jr.", "birthday": "07-08-1993", "occupation": ["High School Chemistry Teacher", "Meth King Pin"], "img": "https://media1.popsugar-assets.com/files/thumbor/WeLUSvbAMS_GL4iELYAUzu7Bpv0/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2018/01/12/910/n/1922283/fb758e62b5daf3c9_TCDBRBA_EC011/i/RJ-Mitte-Walter-White-Jr.jpg", "status": "Alive", "nickname": "Flynn", "appearance": [1, 2, 3, 4, 5], "portrayed": "RJ Mitte", "category": "Breaking Bad", "better_call_saul_appearance": []}, {"char_id": 5, "name": "Henry Schrader", "birthday": "Unknown", "occupation": ["DEA Agent"], "img": "https://vignette.wikia.nocookie.net/breakingbad/images/b/b7/HankS5.jpg/revision/latest/scale-to-width-down/700?cb=20120620014136", "status": "Deceased", "nickname": "Hank", "appearance": [1, 2, 3, 4, 5], "portrayed": "Dean Norris", "category": "Breaking Bad", "better_call_saul_appearance": []}, {"char_id": 15, "name": "Todd Alquist", "birthday": "Unknown", "occupation": ["Lab Assistant", "Enforcer", "Meth Cook"], "img": "https://vignette.wikia.nocookie.net/breakingbad/images/9/95/Todd_brba5b.png/revision/latest?cb=20130717134303", "status": "Deceased", "nickname": "Ricky Hitler", "appearance": [5], "portrayed": "Jesse Plemons", "category": "Breaking Bad", "better_call_saul_appearance": []}]
        response = self.client.get('/api/characters', data=data, follow=True)

        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(expected_response), len(response_json))
        
        for i in range(len(expected_response)):
            self.assertDictEqual(response_json[i], expected_response[i])

class MiscTests(SimpleTestCase):
    def testParseNamesUnique(self):
        names = 'walt,tod,walt,henry schrader,walt'
        expected_names = ['walt', 'tod', 'henry schrader']
        parsed_names = views.parse_names(names)
        self.assertCountEqual(expected_names, parsed_names)

    def testParseNamesWhitespacesRemoved(self):
        names = '    walt ,tod,,,walt,  henry,walt   '
        expected_names = ['walt', 'tod', 'henry']

        parsed_names = views.parse_names(names)
        self.assertCountEqual(expected_names, parsed_names)

    def testParseNamesLowercase(self):
        names = 'WaLt,TOD,Henry Schrader'
        expected_names = ['walt', 'tod', 'henry schrader']

        parsed_names = views.parse_names(names)
        self.assertCountEqual(expected_names, parsed_names)
