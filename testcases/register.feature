Feature: User Registration

  Scenario: User enters valid registration details
    Given I am a new user on the registration page
    When I enter a valid name, email, and password
    And I submit the registration form
    Then my account should be created
    And I should be redirected to the welcome page

  Scenario: User enters invalid email format during registration
    Given I am a new user on the registration page
    When I enter an invalid email address and valid name and password
    And I submit the registration form
    Then I should see an error message indicating invalid email format
    And my account should not be created

  Scenario: User enters weak password during registration
    Given I am a new user on the registration page
    When I enter a valid name and email and a weak password
    And I submit the registration form
    Then I should see an error message indicating password strength requirements
    And my account should not be created
