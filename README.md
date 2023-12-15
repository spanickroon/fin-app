# User Guide

## For the user

### Authentication
Users log in using their Google Authenticator. If they don't have an account, they can register. Upon registration, a QR code is sent to the specified email. Users need to scan this QR code with the Google Authenticator app to generate an OTP code, which they must enter during login.

### Payments via QR Code
Users can navigate to the main page, where the first hyperlink leads them to a page with categories of utility payments. After selecting a specific subcategory, users can generate a QR code for payment via PayPal. For payments requiring meter readings, users must input previous and current readings. Payment history is accessible in the corresponding section.

### Loans
Users can apply for a loan only after verifying their documents. To do so, users must upload a photo of the last page of their passport in the "Documents" section. After successful upload, they can specify the desired loan amount in the "Loans" section.

### Logging Out
After completing tasks, it is recommended for users to log out. To log out, use the "Log Out" button in the top right corner of the main page header.

## For Moderators (Administrative Panel)
### Payments
When creating a payment, a moderator selects a subcategory and, if necessary, activates the "is_prev_amount" flag. This flag adds an additional field to the payment for the previous meter reading value. This is relevant for categories such as gas, electricity, etc., where determining the amount requires knowledge of the consumed units over a specific period (usually a month).

### Accepting Loans
Moderators can view and approve loan requests.

## General Information
The administrative panel supports two languages - Russian and English. At the time of writing this guide, the application (templates) only supports the Russian language.