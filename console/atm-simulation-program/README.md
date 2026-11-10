# ATM Simulation

A console-based ATM simulation program developed using Python. It demonstrates basic banking operations through an interactive command-line interface, including balance enquiry, PIN management, cash withdrawal, and cash deposits.

## Features

- **Card Validation:** Validates the 12-digit card number and checks whether the user exists.
- **PIN Authentication:** Verifies the user's 4-digit PIN before allowing banking operations.
- **Display Balance:** Displays the account holder's name and current account balance.
- **Change PIN:** Allows users to update their existing 4-digit ATM PIN.
- **Cash Withdrawal:** Allows users to withdraw money subject to balance availability and withdrawal limits.
- **Cash Deposit:** Supports deposits using ₹500, ₹200, and ₹100 denominations.
- **Login Attempt Limit:** Restricts PIN entry to three attempts.
- **Input Validation:** Handles invalid inputs and prevents certain incorrect transactions.
- **Console Management:** Clears the terminal screen between sessions.

## Technologies Used

- Python
- OS Module
- Exception Handling
- Functions
- Dictionaries and Lists
- Conditional Statements
- Loops

## Project Structure

```text
atm-simulation/
│
├── atm.py
└── README.md
```

## How to Run

1. Make sure Python is installed on your system.
2. Clone or download this repository.
3. Navigate to the project directory.
4. Run the following command:

```bash
python atm.py
```

## Sample User Credentials

The program currently uses predefined user details stored in a Python dictionary.

| Card Number | Name | PIN |
|---|---|---|
| 123456789101 | ABC User | 1001 |
| 999999999999 | XYZ User | 1234 |

## Learning Objectives

- Practising Python functions and modular programming.
- Understanding dictionaries and lists for managing user data.
- Implementing input validation and exception handling.
- Working with conditional statements and loops.
- Understanding basic banking transaction logic.
- Developing interactive command-line applications.

## Limitations

- User information is stored in memory and is not persistent.
- Changes to PINs and account balances are lost when the program terminates.
- This is an educational simulation and does not connect to any real banking system.

## Author

**Anuj Singh**

BCA Student | Software Developer | AI/ML Learner

I enjoy building software while understanding the engineering principles behind modern systems.

## Connect With Me

- **LinkedIn:** [ianujsingh](https://linkedin.com/in/ianujsingh)
- **GitHub:** [i-am-anujsingh](https://github.com/i-am-anujsingh)

---

This project reflects my ongoing learning in Python development, console-based programming, and DSA through practical implementation.