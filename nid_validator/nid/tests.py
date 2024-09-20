import unittest
from nid.EgyptianNationalIdValidator import EgyptianNationalIdValidator
from datetime import date

class EgyptianNationalIdValidatorTest(unittest.TestCase):

    def test_valid_national_id(self):
        """Test a valid Egyptian National ID"""
        valid_id = "29901150101921"  # January 15, 1999, Cairo, Female
        validator = EgyptianNationalIdValidator(valid_id)
        self.assertEqual(validator.data['birth_date'], date(1999, 1, 15))
        self.assertEqual(validator.data['governorate'], 'Cairo')
        self.assertEqual(validator.data['gender'], 'Female')

    def test_invalid_century_code(self):
        """Test ID with an invalid century code"""
        invalid_id = "49901150101921"  # Invalid century code (4 instead of 2 or 3)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_invalid_id_format(self):
        """Test an ID with an invalid format (wrong length or structure)"""
        invalid_id = "2990115010192"  # Invalid length (13 digits instead of 14)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_invalid_birth_date(self):
        """Test an ID with an invalid birth date"""
        invalid_id = "29902330101921"  # Invalid date (Feb 33 is not valid)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_invalid_governorate_code(self):
        """Test ID with an invalid governorate code"""
        invalid_id = "29901159901921"  # Invalid governorate code (99 doesn't exist)
        with self.assertRaises(ValueError):
            EgyptianNationalIdValidator(invalid_id)

    def test_male_gender_extraction(self):
        """Test gender extraction when the gender code represents Male"""
        valid_id = "29901150101931"  # Male (sequence number ends in odd digit)
        validator = EgyptianNationalIdValidator(valid_id)
        self.assertEqual(validator.data['gender'], 'Male')

    def test_female_gender_extraction(self):
        """Test gender extraction when the gender code represents Female"""
        valid_id = "29901150101921"  # Female (sequence number ends in even digit)
        validator = EgyptianNationalIdValidator(valid_id)
        self.assertEqual(validator.data['gender'], 'Female')


if __name__ == '__main__':
    unittest.main()
