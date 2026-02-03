# User Stories — Personal Expense Management

## Introduction

This document contains all user stories for the **Personal Expense Management** feature. These stories are designed to deliver the core value proposition of the Expense Tracker application: helping users understand and control their personal finances through simple transaction tracking, automatic categorization, visual insights, budget management, and report export.

**Traceability to Objectives/KPIs:**
- **Engagement KPI** (60% DAU adding transactions): Stories PEM-USER-001, PEM-USER-002, PEM-USER-003
- **Budget Awareness KPI** (40% setting budgets): Stories PEM-USER-005, PEM-USER-006
- **Financial Insights KPI** (50% viewing charts): Story PEM-USER-004
- **External Reporting KPI** (25% exporting reports): Story PEM-USER-007

---

## User Stories

### PEM-USER-001: Add Expense Transaction

**As a** user  
**I want to** quickly add an expense transaction with minimal required fields  
**So that** I can track my spending without friction and maintain an accurate financial record

**Priority:** CRITICAL  
**Estimated Effort:** M  
**Dependencies:** None

#### Acceptance Criteria

##### Scenario 1: Successfully add expense with all required fields (Happy Path)
```gherkin
Given I am authenticated as a user
And I am on the expense entry form
When I enter amount "45.50"
And I select date "2026-02-03"
And I select category "Food"
And I submit the form
Then the expense is created successfully
And I see a success confirmation message
And the transaction appears in my transaction list
And an analytics event "transaction_added" is logged with user_id and category
```

##### Scenario 2: Add expense with optional description
```gherkin
Given I am authenticated as a user
And I am on the expense entry form
When I enter amount "45.50"
And I select date "2026-02-03"
And I select category "Food"
And I enter description "Lunch at restaurant"
And I submit the form
Then the expense is created with the description
And the description is visible in the transaction list
```

##### Scenario 3: Validation error for missing required fields (Edge Case)
```gherkin
Given I am authenticated as a user
And I am on the expense entry form
When I leave the amount field empty
And I submit the form
Then I see a validation error "Amount is required"
And the form is not submitted
And no transaction is created
```

##### Scenario 4: Validation error for invalid amount format (Edge Case)
```gherkin
Given I am authenticated as a user
And I am on the expense entry form
When I enter amount "abc"
And I submit the form
Then I see a validation error "Amount must be a valid number"
And the form is not submitted
```

##### Scenario 5: Validation error for negative amount (Edge Case)
```gherkin
Given I am authenticated as a user
And I am on the expense entry form
When I enter amount "-50.00"
And I submit the form
Then I see a validation error "Amount must be positive"
And the form is not submitted
```

##### Scenario 6: Validation error for future date (Edge Case)
```gherkin
Given I am authenticated as a user
And I am on the expense entry form
When I select a date in the future
And I submit the form
Then I see a validation error "Date cannot be in the future"
And the form is not submitted
```

##### Scenario 7: Authorization enforcement (Security)
```gherkin
Given I am authenticated as user "user_123"
When I submit an expense transaction
Then the transaction is created with user_id "user_123"
And the transaction is only accessible to user "user_123"
And other users cannot view or modify this transaction
```

##### Scenario 8: API response time performance (Performance)
```gherkin
Given I am authenticated as a user
When I submit a valid expense transaction
Then the API responds within 200ms (P95)
And the transaction is persisted to the database
```

##### Scenario 9: Keyboard navigation support (Accessibility)
```gherkin
Given I am authenticated as a user
And I am on the expense entry form
When I navigate using only the keyboard (Tab, Enter)
Then I can access all form fields
And I can submit the form using Enter
And all interactive elements have visible focus indicators
```

##### Scenario 10: Error handling for server failure (Error Handling)
```gherkin
Given I am authenticated as a user
And the backend API is unavailable
When I submit an expense transaction
Then I see an error message "Unable to save transaction. Please try again."
And the form data is preserved
And the transaction is retried once after 1 second
```

---

### PEM-USER-002: Add Income Transaction

**As a** user  
**I want to** record income transactions  
**So that** I can track my total cash flow and understand my financial situation holistically

**Priority:** HIGH  
**Estimated Effort:** S  
**Dependencies:** None

#### Acceptance Criteria

##### Scenario 1: Successfully add income transaction (Happy Path)
```gherkin
Given I am authenticated as a user
And I am on the income entry form
When I enter amount "2500.00"
And I select date "2026-02-01"
And I select category "Salary"
And I submit the form
Then the income transaction is created successfully
And I see a success confirmation message
And the transaction appears in my transaction list marked as "Income"
And an analytics event "transaction_added" is logged with type "income"
```

##### Scenario 2: Income transactions excluded from expense analytics (Edge Case)
```gherkin
Given I have added income transaction of "2500.00"
And I have added expense transaction of "100.00"
When I view the expense analytics chart
Then only the expense transaction is included in the chart
And the income transaction is not included in expense totals
```

##### Scenario 3: Authorization enforcement for income (Security)
```gherkin
Given I am authenticated as user "user_123"
When I submit an income transaction
Then the transaction is created with user_id "user_123"
And only user "user_123" can access this income record
```

---

### PEM-USER-003: Edit and Delete Transactions

**As a** user  
**I want to** edit or delete existing transactions  
**So that** I can correct mistakes and maintain accurate financial records

**Priority:** HIGH  
**Estimated Effort:** M  
**Dependencies:** PEM-USER-001, PEM-USER-002

#### Acceptance Criteria

##### Scenario 1: Successfully edit expense transaction (Happy Path)
```gherkin
Given I am authenticated as a user
And I have an existing expense transaction with amount "50.00"
When I select the transaction to edit
And I change the amount to "55.00"
And I change the category from "Food" to "Entertainment"
And I save the changes
Then the transaction is updated successfully
And I see a success confirmation message
And the updated values are reflected in my transaction list
And an analytics event "transaction_updated" is logged
```

##### Scenario 2: Successfully delete transaction with confirmation (Happy Path)
```gherkin
Given I am authenticated as a user
And I have an existing expense transaction
When I select the transaction to delete
Then I see a confirmation dialog "Are you sure you want to delete this transaction?"
When I confirm the deletion
Then the transaction is deleted successfully
And I see a success confirmation message
And the transaction no longer appears in my transaction list
And an analytics event "transaction_deleted" is logged
```

##### Scenario 3: Cancel deletion (Edge Case)
```gherkin
Given I am authenticated as a user
And I have an existing expense transaction
When I select the transaction to delete
And I see the confirmation dialog
When I cancel the deletion
Then the transaction is not deleted
And the transaction still appears in my transaction list
```

##### Scenario 4: Authorization enforcement for edit (Security - BOLA Prevention)
```gherkin
Given I am authenticated as user "user_123"
And user "user_456" has a transaction with id "txn_789"
When I attempt to edit transaction "txn_789" via API
Then I receive a 403 Forbidden response
And the transaction is not modified
And an audit log entry is created for the unauthorized attempt
```

##### Scenario 5: Authorization enforcement for delete (Security - BOLA Prevention)
```gherkin
Given I am authenticated as user "user_123"
And user "user_456" has a transaction with id "txn_789"
When I attempt to delete transaction "txn_789" via API
Then I receive a 403 Forbidden response
And the transaction is not deleted
And an audit log entry is created for the unauthorized attempt
```

##### Scenario 6: Keyboard navigation for edit/delete actions (Accessibility)
```gherkin
Given I am authenticated as a user
And I am viewing my transaction list
When I navigate using only the keyboard
Then I can access edit and delete buttons for each transaction
And I can activate actions using Enter or Space
```

---

### PEM-USER-004: View Expense Analytics Charts

**As a** user  
**I want to** view visual charts of my spending patterns  
**So that** I can quickly understand where my money is going and make informed financial decisions

**Priority:** CRITICAL  
**Estimated Effort:** L  
**Dependencies:** PEM-USER-001

#### Acceptance Criteria

##### Scenario 1: View pie chart by category (Happy Path)
```gherkin
Given I am authenticated as a user
And I have expenses in categories: Food (€200), Transportation (€100), Entertainment (€50)
When I navigate to the analytics dashboard
Then I see a pie chart showing expense distribution by category
And the chart displays "Food: €200 (57%)", "Transportation: €100 (29%)", "Entertainment: €50 (14%)"
And the chart updates automatically when I add new transactions
And an analytics event "chart_viewed" is logged
```

##### Scenario 2: View bar chart by month (Happy Path)
```gherkin
Given I am authenticated as a user
And I have expenses: January (€500), February (€600), March (€450)
When I navigate to the analytics dashboard
And I select the "Monthly Trend" view
Then I see a bar chart showing expenses per month
And the chart displays bars for each month with correct amounts
And the chart is limited to the last 12 months by default
```

##### Scenario 3: No data state (Edge Case)
```gherkin
Given I am authenticated as a user
And I have no expense transactions
When I navigate to the analytics dashboard
Then I see a message "No expense data available. Add your first transaction to see insights."
And no chart is displayed
```

##### Scenario 4: Authorization enforcement (Security)
```gherkin
Given I am authenticated as user "user_123"
When I request chart data via API
Then I only receive data for transactions belonging to user "user_123"
And I cannot access chart data for other users
```

##### Scenario 5: API response time performance (Performance)
```gherkin
Given I am authenticated as a user
And I have 500 transactions in the database
When I request chart data
Then the API responds within 300ms (P95)
And the data is aggregated correctly
```

##### Scenario 6: Graceful degradation on API failure (Error Handling)
```gherkin
Given I am authenticated as a user
And I have previously viewed charts (cached data exists)
And the backend API is unavailable
When I navigate to the analytics dashboard
Then I see cached chart data
And I see a warning indicator "Showing cached data. Unable to refresh."
```

##### Scenario 7: Chart accessibility with data table alternative (Accessibility)
```gherkin
Given I am authenticated as a user
And I am viewing expense charts
When I activate the "View as Table" option
Then I see the same data presented in an accessible HTML table
And the table has proper headers and ARIA labels
And screen readers can navigate the data
```

##### Scenario 8: Color contrast compliance (Accessibility)
```gherkin
Given I am authenticated as a user
When I view the expense charts
Then all chart colors have a contrast ratio of at least 3:1
And text labels have a contrast ratio of at least 4.5:1
```

---

### PEM-USER-005: Set Category Budget

**As a** user  
**I want to** define a monthly budget for each expense category  
**So that** I can control my spending and avoid overspending in specific areas

**Priority:** HIGH  
**Estimated Effort:** M  
**Dependencies:** PEM-USER-001

#### Acceptance Criteria

##### Scenario 1: Successfully set category budget (Happy Path)
```gherkin
Given I am authenticated as a user
And I am on the budget management page
When I select category "Food"
And I enter budget amount "300.00"
And I save the budget
Then the budget is created successfully
And I see a success confirmation message
And the budget appears in my budget list
And an analytics event "budget_created" is logged with category and amount
```

##### Scenario 2: Update existing budget (Happy Path)
```gherkin
Given I am authenticated as a user
And I have an existing budget for "Food" of "300.00"
When I edit the budget to "350.00"
And I save the changes
Then the budget is updated successfully
And the new amount is reflected in my budget list
And an analytics event "budget_updated" is logged
```

##### Scenario 3: Validation error for invalid budget amount (Edge Case)
```gherkin
Given I am authenticated as a user
When I enter budget amount "0"
And I save the budget
Then I see a validation error "Budget must be greater than zero"
And the budget is not created
```

##### Scenario 4: Validation error for negative budget (Edge Case)
```gherkin
Given I am authenticated as a user
When I enter budget amount "-100"
And I save the budget
Then I see a validation error "Budget must be positive"
And the budget is not created
```

##### Scenario 5: Authorization enforcement (Security - BOLA Prevention)
```gherkin
Given I am authenticated as user "user_123"
When I create a budget
Then the budget is associated with user_id "user_123"
And only user "user_123" can view or modify this budget
And other users cannot access this budget
```

##### Scenario 6: Keyboard navigation support (Accessibility)
```gherkin
Given I am authenticated as a user
And I am on the budget management page
When I navigate using only the keyboard
Then I can access all budget input fields
And I can save budgets using Enter
And all interactive elements have visible focus indicators
```

---

### PEM-USER-006: Receive Budget Alerts

**As a** user  
**I want to** receive visual warnings when I approach or exceed my category budgets  
**So that** I can adjust my spending behavior before overspending

**Priority:** HIGH  
**Estimated Effort:** M  
**Dependencies:** PEM-USER-001, PEM-USER-005

#### Acceptance Criteria

##### Scenario 1: Warning at 80% budget threshold (Happy Path)
```gherkin
Given I am authenticated as a user
And I have a budget of "300.00" for category "Food"
And I have spent "240.00" in "Food" this month (80%)
When I view the budget dashboard
Then I see a warning indicator "⚠️ 80% of Food budget used"
And the budget bar is displayed in warning color (yellow/amber)
And an analytics event "budget_threshold_warning" is logged
```

##### Scenario 2: Alert at 100% budget exceeded (Happy Path)
```gherkin
Given I am authenticated as a user
And I have a budget of "300.00" for category "Food"
And I have spent "310.00" in "Food" this month (103%)
When I view the budget dashboard
Then I see an alert indicator "❌ Food budget exceeded by €10.00"
And the budget bar is displayed in alert color (red)
And an analytics event "budget_threshold_exceeded" is logged with overage amount
```

##### Scenario 3: No alert when under 80% threshold (Edge Case)
```gherkin
Given I am authenticated as a user
And I have a budget of "300.00" for category "Food"
And I have spent "200.00" in "Food" this month (67%)
When I view the budget dashboard
Then I see no warning or alert indicators
And the budget bar is displayed in normal color (green)
```

##### Scenario 4: Real-time budget update after transaction (Happy Path)
```gherkin
Given I am authenticated as a user
And I have a budget of "300.00" for category "Food"
And I have spent "230.00" in "Food" this month
When I add a new expense of "20.00" in "Food"
Then the budget dashboard updates automatically
And I see the warning indicator "⚠️ 83% of Food budget used"
```

##### Scenario 5: Color contrast compliance for alerts (Accessibility)
```gherkin
Given I am authenticated as a user
When I view budget warning or alert indicators
Then all warning colors have a contrast ratio of at least 3:1
And alert text has a contrast ratio of at least 4.5:1
And alerts are not conveyed by color alone (icons + text)
```

##### Scenario 6: Screen reader support for alerts (Accessibility)
```gherkin
Given I am authenticated as a user using a screen reader
When a budget warning or alert is displayed
Then the screen reader announces the alert with appropriate ARIA labels
And the alert severity is communicated (warning vs. critical)
```

---

### PEM-USER-007: Export Financial Reports

**As a** user  
**I want to** export my transaction data in CSV or PDF format  
**So that** I can use the data for external analysis, tax preparation, or record-keeping

**Priority:** MEDIUM  
**Estimated Effort:** L  
**Dependencies:** PEM-USER-001, PEM-USER-002

#### Acceptance Criteria

##### Scenario 1: Export transactions as CSV (Happy Path)
```gherkin
Given I am authenticated as a user
And I have transactions from January 1 to March 31, 2026
When I navigate to the export page
And I select date range "2026-01-01" to "2026-03-31"
And I select format "CSV"
And I click "Export"
Then a CSV file is downloaded
And the file contains all transactions in the selected date range
And the CSV includes columns: Date, Type, Category, Amount, Description
And the file is named "expense_report_2026-01-01_to_2026-03-31.csv"
And an analytics event "report_exported" is logged with format "CSV"
```

##### Scenario 2: Export transactions as PDF (Happy Path)
```gherkin
Given I am authenticated as a user
And I have transactions from January 1 to March 31, 2026
When I navigate to the export page
And I select date range "2026-01-01" to "2026-03-31"
And I select format "PDF"
And I click "Export"
Then a PDF file is downloaded
And the PDF contains a formatted report with:
  | Section | Content |
  | Summary | Total income, total expenses, net balance |
  | Category Breakdown | Expenses grouped by category with totals |
  | Transaction List | All transactions in the date range |
And the file is named "expense_report_2026-01-01_to_2026-03-31.pdf"
And an analytics event "report_exported" is logged with format "PDF"
```

##### Scenario 3: Validation error for invalid date range (Edge Case)
```gherkin
Given I am authenticated as a user
When I select start date "2026-03-31"
And I select end date "2026-01-01" (end before start)
And I click "Export"
Then I see a validation error "End date must be after start date"
And no file is downloaded
```

##### Scenario 4: Export with no transactions in range (Edge Case)
```gherkin
Given I am authenticated as a user
And I have no transactions between "2026-01-01" and "2026-01-31"
When I export for that date range
Then I receive a file with headers but no transaction rows
And I see a message "No transactions found for the selected period"
```

##### Scenario 5: Authorization enforcement (Security - BOLA Prevention)
```gherkin
Given I am authenticated as user "user_123"
When I request an export via API
Then the export only includes transactions belonging to user "user_123"
And I cannot export data for other users
And the user_id is verified from the JWT token
```

##### Scenario 6: CSV export performance (Performance)
```gherkin
Given I am authenticated as a user
And I have 1000 transactions in the selected date range
When I export as CSV
Then the API responds within 500ms (P95)
And the file is generated successfully
```

##### Scenario 7: PDF export performance (Performance)
```gherkin
Given I am authenticated as a user
And I have 1000 transactions in the selected date range
When I export as PDF
Then the API responds within 2 seconds (P95)
And the file is generated successfully
```

##### Scenario 8: Fallback to CSV on PDF generation failure (Error Handling)
```gherkin
Given I am authenticated as a user
And the PDF generation library fails
When I request a PDF export
Then I see an error message "PDF generation failed. Would you like to download as CSV instead?"
And I can choose to download CSV as a fallback
And an error log is created for the PDF failure
```

##### Scenario 9: Retry logic for export failures (Error Handling)
```gherkin
Given I am authenticated as a user
And the backend API times out on the first request
When I request an export
Then the request is automatically retried once
And if the retry succeeds, the file is downloaded
And if the retry fails, I see an error message "Export failed. Please try again later."
```

##### Scenario 10: Keyboard navigation for export controls (Accessibility)
```gherkin
Given I am authenticated as a user
And I am on the export page
When I navigate using only the keyboard
Then I can access date pickers, format selector, and export button
And I can trigger the export using Enter
And all interactive elements have visible focus indicators
```

---

### PEM-USER-008: Automatic Expense Categorization

**As a** user  
**I want to** have my expenses automatically categorized based on intelligent rules  
**So that** I can save time and effort while maintaining organized financial records

**Priority:** HIGH  
**Estimated Effort:** L  
**Dependencies:** PEM-USER-001

#### Acceptance Criteria

##### Scenario 1: Automatic categorization based on description keywords (Happy Path)
```gherkin
Given I am authenticated as a user
And the system has categorization rules:
  | Keyword | Category |
  | restaurant, lunch, dinner | Food |
  | gas, uber, taxi | Transportation |
  | movie, concert, netflix | Entertainment |
When I add an expense with description "Lunch at restaurant"
Then the system automatically suggests category "Food"
And the suggested category is pre-selected in the form
And I can accept or change the suggestion before saving
```

##### Scenario 2: Manual override of automatic categorization (Happy Path)
```gherkin
Given I am authenticated as a user
And the system suggests category "Food" based on description "Lunch meeting"
When I manually change the category to "Entertainment"
And I save the transaction
Then the transaction is saved with category "Entertainment"
And the automatic suggestion is not enforced
And the user's choice is respected
```

##### Scenario 3: Default to "Other" when no match found (Edge Case)
```gherkin
Given I am authenticated as a user
When I add an expense with description "Random purchase"
And no categorization rule matches the description
Then the system suggests category "Other"
And I can manually select a different category
```

##### Scenario 4: Case-insensitive keyword matching (Edge Case)
```gherkin
Given I am authenticated as a user
When I add an expense with description "RESTAURANT BILL"
Then the system suggests category "Food"
And the matching is case-insensitive
```

##### Scenario 5: Categorization performance (Performance)
```gherkin
Given I am authenticated as a user
When I add an expense with description
Then the categorization suggestion is computed within 50ms
And the suggestion does not delay the form rendering
```

##### Scenario 6: No PII logged during categorization (Security/Privacy)
```gherkin
Given I am authenticated as a user
When the system performs automatic categorization
Then the transaction description is NOT logged in application logs
And only the suggested category is logged (if at all)
And user privacy is maintained
```

---

## Summary

**Total User Stories:** 8  
**Critical Priority:** 3 (PEM-USER-001, PEM-USER-004, PEM-USER-007)  
**High Priority:** 4 (PEM-USER-002, PEM-USER-003, PEM-USER-005, PEM-USER-006, PEM-USER-008)  
**Medium Priority:** 1 (PEM-USER-007)

**Estimated Total Effort:** 2-3 sprints (assuming 2-week sprints)

**Coverage:**
- ✅ Transaction Management (Add, Edit, Delete)
- ✅ Visual Analytics (Charts)
- ✅ Budget Management (Set, Monitor, Alerts)
- ✅ Report Export (CSV, PDF)
- ✅ Automatic Categorization
- ✅ Security (BOLA prevention, authorization)
- ✅ Performance (Response time targets)
- ✅ Accessibility (WCAG 2.1 AA)
- ✅ Error Handling (Graceful degradation, retries)
