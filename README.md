# Unifize BE Dev Assignment

## How to run the project

#### Prerequisites
- Python 3.10 installed on your system
- pip package manager

#### Step 1: Create a Virtual Environment
1. Open your terminal or command prompt.
2. Navigate to the directory where you want to create your virtual environment.
3. Run the following command to create a virtual environment named `venv`:
   ```bash
   python3.10 -m venv venv
   ```
#### Step 2: Activate the Virtual Environment
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
    source venv/bin/activate
    ```
#### Step 3: Install Dependencies
1. Ensure you are in the directory where `requirements.txt` is located.
2. Run the following command to install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
#### Step 4: Run the Application
Run main.py using the following command:
```bash
python main.py
```

#### Step 5: Run Test Cases
To run the test cases, use the following command:
```bash
pytest tests/
```

### Assumptions
1. Discounts other than voucher codes will be automatically applied
2. When applying discounts only 1 discount per category will be applied, in cases of multiple discounts exists per category one which expires sooner will be applied

### Core Entities
- Discount: Base class for all discounts. They are composed of DiscountRules to apply specific discount logic.
- DiscountRules: DiscountRule exposes a common interface to implement specific discount logic.
- DiscountProcessor: Responsible for applying discounts to cart and calculating the final price.
- DiscountProcessingStrategy: Defines the strategy for processing discounts, including stacking order etc

