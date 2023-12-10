# Grade Fetch Script
#### https://github.com/Rob-Payne-28/school-grades
## Description
This script automatically logs into our school's website and extracts grade information. It handles authentication and parses HTML content to extract IPR data.

## Setup Instructions
### Install Python:
Ensure Python 3 is installed on your system. This script has been tested with Python 3.9. If not already installed, you can download it from python.org or install it via Homebrew on macOS:

```shell
brew install python
```

### Install dependencies
This script uses libraries for https session management and parsing returned data. If you don't have them installed, you will need to install them.

```shell
# Used to handle session information
pip3 install requests
# Used to parse returned webpages
pip3 install beautifulsoup4
# Used to pull in environment variables
pip3 install python-dotenv
```
### Clone the Repository:
Clone the script to your local machine.

```shell
# Via https
git clone https://github.com/Rob-Payne-28/school-grades.git
```

### Environment Variables:
Create a .env file (if one doesn't already exist) in the same directory as your script to store sensitive information like URLs and login credentials. Replace the sample .env variables below with your values.

```shell
touch .env
echo "LOGIN_PAGE_URL=https://example.com/login" >> .env
echo "LOGIN_ACTION_URL=https://example.com/login-action" >> .env
echo "USERNAME=your_username" >> .env
echo "PASSWORD=your_password" >> .env
echo "I_FRAME_URL=https://example.com/iframe-base-url" >> .env
echo "USER_AGENT=YourUserAgentStringHere" >> .env
```

## Run the Script:
With everything set up, run the script:

```shell
python fetch-grades.py
```

## Troubleshooting
- If you encounter issues, check the grades_script.log file for error messages.
- Ensure that the .env file is correctly formatted and contains the necessary information.

