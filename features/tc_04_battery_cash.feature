Feature: End To End Page Tests

  @end_to_end_battery_cash
  @critical
  Scenario: TC 04, Verify End to End Work flow of Product Battery with Cash as Finance Method
    Given I load the website
    When I login the page successfully
    Then Verify End to End Work flow of Product Battery with Cash as Finance Method