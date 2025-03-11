# A Template for End-to-End Testing with Selenium Python and Behave

# One-time setup

## Selenium

Selenium is a framework for automating browser interactions. More information can be found [here](https://www.seleniumhq.org/).

### Context

Settings and driver instantiation. This project uses a singleton pattern to represent a webdriver.

`settings.json` handles the URL and the browser.

A sample `settings.json` file is provided for reference. Change the relevant username, password, and URL for test execution.

### .Env File

Set the below details to the .Env file

`AZURE_CLIENT_ID="Your Azure AD Application Client ID"`

`AZURE_TENANT_ID="Your Azure AD Tenant ID"`

`AZURE_CLIENT_SECRET="Your Azure AD Application Client Secret"`

`AZURE_KEYVAULT_URL="Your Key Vault URL"`

`secret_name="Your Key Vault Username Variable"`

`secret_pass="Your Key Vault Password Variable"`

## Behave

Behave is a framework for Behavior-Driven Development (BDD). It's a shared language syntax that allows you to specify steps for end-to-end tests. You can find its documentation [here](https://behave.readthedocs.io/).

### Installation

#### Install Python

Download and install the latest version of Python.

#### Download Latest Visual Studio Code IDE

Download Visual Studio Code from [here](https://code.visualstudio.com/download).

#### Installing Java

Download Java from [here](https://www.oracle.com/java/technologies/javase/jdk19-archive-downloads.html) and install it..

#### Downloading Allure Folder

Download the Allure report folder containing screenshots and JSON files from the [Allure website](https://github.com/allure-framework/allure2/releases).

Move the downloaded Allure folder to the root directory.

## Getting Started

To get started, you'll need to fork the repository. Then, clone the repository and navigate to it. Next, run the below command to install the required dependencies.

```
pip3 install -r requirements.txt
```

Once you've completed these steps, simply run the command `behave` to execute a basic test case. This test case performs a Google search using the Chrome browser.

## General Architecture

This template is constructed using the Page-Object-Model (POM). The POM is a straightforward architectural pattern in which each web page is represented by an object.

`environment.py` contains [environmental controls](https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls) for the Behave framework.

There are ten directories contained in this project:

### Allure-results

Generates the screenshots and JSON file for the Allure Report.

### Data

`admin_data.json` - Deals with the data change for admin pages, Opportunity ID (Refer to the below script-wise requirements).
`sales_rep_data.json` - Deals with the data change for sales_rep pages, Opportunity ID (Refer to the below script-wise requirements).

### Features

Contains `.feature` files. These are text files conforming to [Gherkin syntax](https://behave.readthedocs.io/en/latest/philosophy.html#the-gherkin-language).

### Steps

Includes files that contain test methods linked to steps in the `.feature` files.

### Logs

Contains log files after each execution.

### Pages

Encompasses all page objects along with locators for locating elements on the webpages.

### Selector

Encompasses all page locators used in various pages.

### Upload-Files

Encompasses the test files needed to upload in various upload buttons.

### Utils

Encompasses all utilities that are used in various pages.

## Set Allure

Download the latest Allure folder to the C drive from the following link: [Allure](https://github.com/allure-framework/allure2/releases).

## Set the Environment Variables

Add the path of the Python folder and Python/Scripts folder under System variables -> Path.

Add the path of the Allure/bin folder under System variables -> Path.

Add the path of the Java folder under System variables -> Create New Variable and add the installed path of java.

# Commands for Code Execution

To execute a single feature file, use the following command:

```
behave --no-capture --format=allure_behave.formatter:AllureFormatter -o allure-results features/'FEATURE FILE NAME'.feature
```

To perform parallel execution with 5 feature files, please follow these steps:

```
python runner.py
```

## To Get Allure Report

Run the following command:

```
allure serve
```

## Run the Following Commands After Successful Installation of Python in case of any error when installing with requirements.txt

```bash
pip install behave
pip install webdriver-manager
pip install selenium
pip install numpy
pip install Pillow
pip install Allure-behave
pip install Allure-Combine
pip install pyautoit
pip install pytest
pip install pytest-ordering
pip install pytest-xdist
pip install python-dateutil
pip install python-dotenv
pip install azure-keyvault-secrets azure-identity
```
