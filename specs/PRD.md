# Product Requirements Document (PRD)
## Expense Tracker – Personal Expense Management

## 1. Product Overview
Expense Tracker is a personal finance application that allows users to record, categorize, visualize, and control their income and expenses.  
The product focuses on simplicity, clarity, and actionable insights.

## 2. Goals
- Help users understand their spending habits
- Enable budget control per category
- Provide visual insights through monthly charts
- Allow export of financial data for external use

## 3. Target Users
- Individuals managing personal finances
- Freelancers
- Students
- Non-expert financial users

---

## Feature Spec — Personal Expense Management

### 1. Feature Name
**Personal Expense Management**

This feature enables users to track their financial transactions, gain insights into spending patterns, and maintain budget control without requiring financial expertise. It covers income/expense recording, automatic categorization, visual analytics, budget management, and report export. The feature protects sensitive financial data while enabling users to make informed financial decisions.

---

### 2. Core Entities / Roles / Actors

#### 2.1 Actors
- **Individual User (`USER`)**: Can create, view, edit, and delete their own transactions; set budgets; view analytics; export reports. Cannot access other users' data.

---

### 3. High-Level Rules and Permissions

#### 3.1 Access Levels
- **Public**: No access to any expense tracking features (authentication required)
- **Authenticated (`USER`)**: 
  - Can manage own transactions (create, read, update, delete)
  - Can view own analytics and charts
  - Can set and monitor own budgets
  - Can export own financial reports (CSV, PDF)
  - Cannot access other users' financial data (BOLA prevention enforced)

---

### 4. Requirements and Constraints

#### 4.1 Security / Compliance / Quality Requirements
- **Authentication**: JWT-based authentication MUST be enforced for all endpoints
- **Authorization**: All transaction, budget, and report endpoints MUST verify user ownership via `user_id` claim from JWT (BOLA prevention)
- **Data Protection**: 
  - Transaction amounts and descriptions MUST NOT be logged in application logs
  - HTTPS/TLS 1.2+ MUST be enforced for all API communication
  - Database encryption MUST be enabled for data at rest
- **GDPR Compliance**: Users MUST be able to export all their data and request account deletion
- **Audit Logging**: Transaction creation/modification events MUST be logged with user_id and timestamp (90-day retention)
- **Performance**: 
  - Transaction creation: P95 < 200ms
  - Chart data retrieval: P95 < 300ms
  - Report export (CSV): P95 < 500ms
- **Accessibility**: WCAG 2.1 Level AA compliance MUST be achieved for all UI components
- **Data Integrity**: Database indexes MUST be created on `(user_id, date)` and `(user_id, category_id)` for query efficiency

---

## 4. Functional Requirements (Detailed)

### 4.1 Income and Expense Tracking
- Users can add income records
- Users can add expense records
- Each record includes:
  - Amount (required)
  - Date (required)
  - Category (required)
  - Optional description

### 4.2 Automatic Categorization
- Expenses are automatically categorized
- Default categories:
  - Food
  - Transportation
  - Entertainment
  - Utilities
  - Health
  - Other
- Users can manually change the assigned category

### 4.3 Monthly Expense Visualization
- The system displays monthly expense summaries
- Charts supported:
  - Pie chart by category
  - Bar chart by month
- Charts update automatically when data changes

### 4.4 Budget Management
- Users can define a monthly budget per category
- The system tracks spending against each budget
- Visual indicators when:
  - 80% of the budget is reached
  - Budget is exceeded

### 4.5 Report Export
- Users can export reports in:
  - CSV format
  - PDF format
- Reports can be filtered by date range
- Reports include:
  - Income summary
  - Expense summary
  - Category totals

## 5. User Flows

### 5.1 Add Expense Flow
1. User selects "Add Expense"
2. User enters expense details
3. System auto-assigns category
4. User confirms or edits category
5. Expense is saved and reflected in analytics

### 5.2 Budget Monitoring Flow
1. User defines a category budget
2. User adds expenses
3. System updates remaining budget
4. Warnings appear when limits are approached

## 6. Non-Functional Requirements
- Responsive UI (mobile and desktop)
- Persistent data storage
- Fast loading and chart rendering
- Secure handling of user financial data

## 7. Out of Scope (for MVP)
- Bank integrations
- Multi-currency support
- Cloud synchronization
