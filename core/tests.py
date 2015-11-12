import httplib
from core.models import Location
from django.test import TestCase


class ViewsTestCase(TestCase):
    def test_list_view(self):

        another_locations = []
        right_locations = []
        wrong_locations = []

        for i in range(0, 10):
            another_locations.append(Location.objects.create(title="Another_%s" % i, area=Location.AREA_BOTLEY))
        for i in range(0, 10):
            right_locations.append(Location.objects.create(title="Item_%s" % i, area=Location.AREA_BOTLEY))
        for i in range(10, 20):
            wrong_locations.append(Location.objects.create(title="Item_%s" % i, area=Location.AREA_CENTRAL))

        self.assertEqual(len(another_locations), 10)
        self.assertEqual(len(right_locations), 10)
        self.assertEqual(len(wrong_locations), 10)

        response = self.client.get('/location/')
        self.assertEqual(response.status_code, httplib.OK)

        paginator = response.context['paginator']

        object_count = 0
        for k in range(0, paginator.num_pages):
            page = paginator.page(k + 1)
            object_count += len(page.object_list)
        self.assertEqual(object_count, 30)

        response = self.client.get('/location/?query=Item')
        self.assertEqual(response.status_code, httplib.OK)

        paginator = response.context['paginator']

        object_count = 0
        for k in range(0, paginator.num_pages):
            page = paginator.page(k + 1)
            object_count += len(page.object_list)
        self.assertEqual(object_count, 20)

        response = self.client.get('/location/?query=Item&area=%s' % Location.AREA_BOTLEY)
        self.assertEqual(response.status_code, httplib.OK)

        paginator = response.context['paginator']

        object_count = 0
        for k in range(0, paginator.num_pages):
            page = paginator.page(k + 1)
            object_count += len(page.object_list)
        self.assertEqual(object_count, 10)
