# the-gate
The automatic gate that recognizes car numbers


The structure of the project consists of

1. controller - responsible for the business logic
2. sensor - gets data
    1. car presence
    2. license plate recognition
    3. car proximity
3. database - stores the white list of the cars
4. gate - operates the raw gate functionality (open/close)