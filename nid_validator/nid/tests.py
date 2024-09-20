import unittest
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from nid.EgyptianNationalIdValidator import EgyptianNationalIdValidator


class EgyptianNationalIdValidatorTest(unittest.TestCase):

    def test_valid_national_id(self):
        """Test that a valid national ID returns the correct data."""
        valid_id = "29901150101921"  # January 15, 1999, Cairo, Female
        validator = EgyptianNationalIdValidator(valid_id)
        self.assertEqual(validator.data["birth_date"], datetime(1999, 1, 15).date())
        self.assertEqual(validator.data["governorate"], "Cairo")
        self.assertEqual(validator.data["gender"], "Female")

    def test_invalid_century_code(self):
        """Test ID with an invalid century code."""
        invalid_id = "49901150101921"  # Invalid century code (4 instead of 2 or 3)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_invalid_id_format(self):
        """Test an ID with an invalid format (wrong length or structure)."""
        invalid_id = "2990115010192"  # Invalid length (13 digits instead of 14)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_invalid_birth_date(self):
        """Test an ID with an invalid birth date."""
        invalid_id = "29902330101921"  # Invalid date (Feb 33 is not valid)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_invalid_governorate_code(self):
        """Test ID with an invalid governorate code."""
        invalid_id = "29901159901921"  # Invalid governorate code (99 doesn't exist)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_male_gender_extraction(self):
        """Test gender extraction when the gender code represents Male."""
        valid_id = "29901150101931"  # Male (sequence number ends in odd digit)
        validator = EgyptianNationalIdValidator(valid_id)
        self.assertEqual(validator.data["gender"], "Male")

    def test_female_gender_extraction(self):
        """Test gender extraction when the gender code represents Female."""
        valid_id = "29901150101921"  # Female (sequence number ends in even digit)
        validator = EgyptianNationalIdValidator(valid_id)
        self.assertEqual(validator.data["gender"], "Female")


class NationalIdValidatorAPITest(APITestCase):

    def test_valid_national_id(self):
        """Test that a valid national ID returns the correct data.
        """
        # Valid ID (January 15, 1999, Cairo, Female)
        url = reverse("nid-validator", args=["29901150101921"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("birth_date", response.data)
        self.assertIn("governorate", response.data)
        self.assertIn("gender", response.data)
        self.assertEqual(response.data["birth_date"], datetime(1999, 1, 15).date())
        self.assertEqual(response.data["governorate"], "Cairo")
        self.assertEqual(response.data["gender"], "Female")

    def test_invalid_national_id(self):
        """Test that an invalid national ID returns a 400 Bad Request.
        """
        # Invalid ID (wrong century code)
        url = reverse("nid-validator", args=["49901150101921"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid National Id")

    def test_invalid_governorate_code(self):
        """Test that an invalid governorate code in the national ID returns a 400 Bad Request.
        """
        # Invalid governorate code (99 doesn't exist)
        url = reverse("nid-validator", args=["29901159901921"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


if __name__ == "__main__":
    unittest.main()
