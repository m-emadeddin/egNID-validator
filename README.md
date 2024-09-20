# egNID-validator
A simple and effective API for validating Egyptian National IDs and extracting valuable information such as the date of birth, gender, and governorate of birth based on the ID format.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Setup](#project-setup)
- [API Endpoints](#api-endpoints)
  - [Validation Example](#validation-example)
  - [API Documentation](#api-documentation)
- [Testing](#testing)
- [National ID Format](#national-id-format)
- [Project Decisions](#project-decisions)


## Project Overview

The **egNID-validator** API is designed to validate Egyptian national ID numbers and extract essential details such as:
- Date of Birth
- Gender
- Governorate where the ID owner was born

This project implements regular expressions to validate the ID format and extract this information in a structured and reliable way. It also provides a RESTful API that responds with JSON data.

## Project Setup

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone git@github.com:m-emadeddin/egNID-validator.git
   ```
2. Navigate to the project directory:

    ```bash
    cd egNID-validator/
    ```
3. Install required dependencies:
    ```bash
    sudo pip3 install -r requirements.txt
    ```
4. Navigate to the Django project directory:
    ```bash
    cd nid_validator/
    ```
5. Run the Django development server (default port: 8000):
    ```bash
    python manage.py runserver
    ```
6. The server is now running and the API is available on:
    ```bash
    http://127.0.0.1/id/{id}
    ```

## API Endpoints

### National ID Validation Endpoint:
- **URL**: `/id/<str:id>/`
- **Method**: `GET`
- **Description**: Takes a National ID as input and validates its format, then extracts and returns the birth date, gender, and governorate information.

### Validation Example:

```bash
curl http://127.0.0.1:8000/id/29901150101921/
```

**Response**:
```json 
{
    "birth_date": "2001-03-21",
    "gender": "Male",
    "governorate": "Dakahlia"
}
```


### API Documentation

The **egNID-validator** project includes interactive API documentation generated using **drf-yasg** with Swagger UI and ReDoc.

- **Swagger UI** provides an interactive interface to test and explore API endpoints in real-time.
- **ReDoc** is another UI option that offers clean and concise API documentation.

#### Accessing the Documentation:

1. **Swagger UI**:
   - **URL**: `/swagger/`
   - **Description**: Allows you to explore the available API endpoints, see their request/response formats, and test them with example data directly from the browser.

   Example:
   ```bash
   http://127.0.0.1:8000/swagger/
   ```

2. **ReDoc**:
   - **URL**: `/redoc/`
   - **Description**: ReDoc provides a clean and structured layout for API documentation. It organizes the API endpoints, models, and response types into a detailed, user-friendly interface.

   Example:
   ```bash
   http://127.0.0.1:8000/redoc/
   ```



## Testing

The **egNID-validator** project includes unit tests to ensure the correct functionality of the ID validation process. The tests cover various scenarios, such as valid IDs, invalid IDs, invalid birth dates, governorate codes, and gender extraction.

### Running Tests

You can run the tests using Django's built-in test runner:

1. Navigate to the project directory:
    ```bash
    cd nid_validator/
    ```

2. Run the tests:
    ```bash
    python manage.py test
    ```

### Test Coverage

The tests focus on the following scenarios:

- **Valid National ID**: Ensures that a properly formatted ID returns the correct birth date, gender, and governorate.
    - Example: `29901150101921` should return `1999-01-15`, `Female`, `Cairo`.

- **Invalid National ID**: Ensures that malformed or incorrect IDs are properly rejected with an error.
    - Example: `12388947` should return an error.

- **Century Code Validation**: Ensures the century code (2 for 1900–1999, 3 for 2000–2099) is correctly parsed.

- **Invalid Birth Date**: Checks for impossible birth dates like `29902330101921` (Feb 33).

- **Governorate Code Validation**: Ensures that only valid governorate codes are accepted, and incorrect ones return an error.
    - Example: `29901159901921` should return an error since the code `99` is invalid.

- **Gender Extraction**: Ensures that gender is correctly extracted based on the ID’s sequence number (odd for males, even for females).

### Test Command

```bash
python manage.py test
```

## National ID Format

The Egyptian National ID format consists of 14 digits and can be broken down as follows:


**ID Fromat:** 
```bash
C-YYMMDD-VV-IIIG-X
```

| Section          | Description                                                                                                                                 |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `C` (1 digit)    | Century code (2 for 1900–1999, 3 for 2000–2099, etc.).                                                                                       |
| `YYMMDD` (6 digits) | Date of birth (YY = year, MM = month, DD = day).                                                                                             |
| `VV` (2 digits)  | Governorate code (01 for Cairo, 02 for Alexandria, 88 for those born abroad, etc.).                                                          |
| `IIIG` (4 digits) | Unique sequence of birth registrations on that day, with the last digit indicating gender (odd for males, even for females).                 |
| `X` (1 digit)    | Checksum digit added by the Ministry of Interior to verify the validity of the ID.                                                           |

### ID Format Example:
- **ID**: `29901150101921`
  - **2**: 1900–1999 century
  - **990115**: Date of birth: 1999-01-15
  - **01**: Born in Cairo
  - **0192**: Unique sequence of births on that date, female (even number)
  - **1**: Checksum digit for validation


## Project Decisions

1. **Validation Using Regex**: 
   - A regular expression (`EgNID_REGEX`) is used to ensure that the National ID follows the official Egyptian format before extracting any data. The regex ensures that the century, birth date, governorate, and other components conform to the expected patterns.
   - IDs with an incorrect length or structure are immediately rejected.

2. **Century and Year Handling**:
   - The validator assumes valid IDs belong to individuals born between 1900 and 2099. If the century code is 2 (for 1900–1999) or 3 (for 2000–2099), the ID is considered valid.
   - IDs outside this range will return an error. If the century exceeds 2099, the code will need updating for future generations.
   - **Future Year Handling**: IDs with birth years in the future are not flagged as invalid, but this can easily be adjusted by adding a date check against the current year in the validator.

3. **Governorate Code Handling**:
   - The governorate code is extracted from the ID, and only valid codes are accepted. These codes correspond to specific governorates, and IDs with invalid codes (e.g., `99`) return an error.
   - If the ID’s governorate code does not exist in the predefined list of governorates, it returns an error message.

4. **Gender Identification**:
   - The gender is determined by the last digit of the sequence (`IIIG`) in the ID. Odd numbers (1, 3, 5, 7, 9) represent males, while even numbers (2, 4, 6, 8) represent females.

5. **Checksum Handling (optional for future updates)**:
   - Currently, the code does not check the final checksum digit (`X`) in the ID, which is used by the Ministry of Interior to ensure authenticity. This could be added as a future improvement.

6. **Error Handling and Robustness**:
   - Invalid IDs, whether due to incorrect length, invalid date formats, or governorate codes, trigger appropriate error responses.
   - A simple `try-except` block ensures that invalid IDs are handled gracefully and return a clear error message (`Invalid National ID`) without crashing the server.

7. **Testing Approach**:
   - Unit tests are implemented to validate various edge cases such as:
     - **Valid IDs**: Tests whether valid IDs return the correct birth date, gender, and governorate.
     - **Invalid IDs**: Tests cases with malformed IDs, future birth dates, or incorrect governorate codes.
     - **Invalid Date Formats**: Ensures IDs with non-existent dates (e.g., February 30th) return errors.
     - **Gender Extraction**: Ensures that gender is correctly identified based on the sequence number.
     - **Empty ID Handling**: Tests for cases where no ID is provided, ensuring an appropriate error is returned.

8. **API Documentation with Swagger**:
   - The project uses `drf-yasg` to auto-generate and display Swagger API documentation. This provides a user-friendly interface to test the API and view schema details.
   - Future updates could involve improving the schema and adding more detailed descriptions for each API field.

9. **Linter and Code Formatting**:
   - `Ruff` is used to ensure the code adheres to Python best practices, enforcing strict rules for line length, docstring formatting, and overall code cleanliness.
   - Future improvements could involve adding more detailed documentation and comments for better code maintainability.
    - Certain non-critical formatting issues were intentionally left unresolved to focus on functionality, but can be easily addressed in future iterations.


