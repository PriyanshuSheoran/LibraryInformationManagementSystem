from django.test import TestCase

# Create your tests here.
from django.urls import reverse

class URLTests(TestCase):

    def test_home_root_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_alias_url(self):
        response = self.client.get("/home")
        self.assertEqual(response.status_code, 200)

    def test_readers_page(self):
        response = self.client.get("/readers")
        self.assertEqual(response.status_code, 200)

    def test_save_student_post(self):
        response = self.client.post("/save", data={})
        self.assertIn(response.status_code, [200, 302])

    def test_add_reader_post(self):
        response = self.client.post("/readers/add", data={
            "reader_ref_id": "REF001",
            "reader_name": "John Doe",
            "reader_contact": "1234567890",
            "reader_address": "123 Main St"
       })
        self.assertEqual(response.status_code, 302)  # Assuming redirect after save


    def test_edit_reader_url(self):
        # Since it expects an actual reader_id, use a dummy for now (may 404 or 200 based on logic)
        response = self.client.get("/readers/edit/1/")
        self.assertIn(response.status_code, [200, 404])

    def test_delete_reader_url(self):
        response = self.client.get("/readers/delete/1/")
        self.assertIn(response.status_code, [200, 302, 404])

    def test_export_readers(self):
        response = self.client.get("/readers/export/")
        self.assertIn(response.status_code, [200, 302])

