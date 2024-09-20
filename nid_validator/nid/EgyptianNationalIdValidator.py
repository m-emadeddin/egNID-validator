import re
from datetime import datetime

EgNID_REGEX: str = r"^(2|3)[0-9]{2}[0-1][0-9][0-3][0-9](01|02|03|04|11|12|13|14|15|16|17|18|19|21|22|23|24|25|26|27|28|29|31|32|33|34|35|88)\d{5}$"


CENTURY_ID: dict[int, int] = {
    2: 1900,
    3: 2000
}

MONTHS: dict[str, str] = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

GOVERNORATES: dict[str, str] = {
    "01": "Cairo",
    "02": "Alexandria",
    "03": "Port Said",
    "04": "Suez",
    "11": "Damietta",
    "12": "Dakahlia",
    "13": "Sharqia",
    "14": "Qalyubia",
    "15": "Kafr El Sheikh",
    "16": "Gharbia",
    "17": "Monufia",
    "18": "Beheira",
    "19": "Ismailia",
    "21": "Giza",
    "22": "Beni Suef",
    "23": "Fayoum",
    "24": "Minya",
    "25": "Assiut",
    "26": "Sohag",
    "27": "Qena",
    "28": "Aswan",
    "29": "Luxor",
    "31": "Red Sea",
    "32": "New Valley",
    "33": "Matrouh",
    "34": "North Sinai",
    "35": "South Sinai",
    "88": "Foreign"
}


class EgyptianNationalIdValidator:
    """This class is used to validate and extract data from Egyptian National ID numbers.
    """

    def __init__(self, id: str) -> None:
        """Initialize the class with a national ID number.

        Args:
            id (str): The national ID number.

        """
        self.id: str = id
        if not self.is_valid_nid():
            raise ValueError("Invalid ID number")

        self.data = {}
        self._extract_data()
        self._get_date_of_birth()
        self._get_governorate()
        self._get_gender()


    def is_valid_nid(self) -> bool:
        """Validate the national ID using a regular expression.

        Returns:
            bool: True if the ID is valid, False otherwise.

        """
        valid = re.match(EgNID_REGEX, self.id)
        if valid: return True
        else: return False


    def _extract_data(self) -> None:
        """Parse the string and extract data from the ID number.
        """
        self.birth_century_code: int = int(self.id[0])
        self.birth_date: str = self.id[1:7]
        self.governorate_code: str = self.id[7:9]
        self.sequence_number: str = self.id[9:13]
        self.gender_code: int = int(self.id[12])
        self.legitimate_digit: int = int(self.id[13])


    def _get_date_of_birth(self) -> None:
        """Extract the birth date from the national ID and store it in the data dictionary.
        """
        self.birth_century = CENTURY_ID[self.birth_century_code]
        self.birth_year: int = self.birth_century + int(self.birth_date[:2])
        self.birth_month: int = int(self.birth_date[2:4])
        self.birth_day: int = int(self.birth_date[4:])
        self.data["birth_date"] = datetime(self.birth_year, self.birth_month, self.birth_day).date()


    def _get_governorate(self) -> None:
        """Convert the governorate code to the governorate name and store it in the data dictionary.
        """
        self.data["governorate"] = GOVERNORATES[self.governorate_code]


    def _get_gender(self) -> None:
        """Convert the gender code to male or female and store it in the data dictionary.
        """
        self.data["gender"] = "Female" if self.gender_code % 2 == 0 else "Male"


    def __str__(self) -> str:
        """Return a formatted string of the fields extracted from the ID number.
        """
        return (f"id: {self.id} \n"
                f"birth_century: {self.birth_century_code} \n"
                f'birth_date: {self.data["birth_date"]} \n'
                f'governorate: {self.data["governorate"]} \n'
                f'gender: {self.data["gender"]}')
