# Decentralized Authentication

In this part of the AWS Cloud Project Bootcamp, the focus was on implementing **decentralized authentication with Cognito**. Here's a breakdown of the steps:


*   **Setting up a Cognito User Pool**:
    *   The initial step involved creating a Cognito user pool, which is used when integrating an application and needing a pool of users.
    *   I navigated the AWS Cognito console, acknowledging its frequent UI updates and emphasizing the importance of programmatic configuration to avoid continuous re-learning of new UIs.
    *   I selected the option to create a **user pool**.
    *   Configured sign-in options, including email and username.
    *   Configured password policies, leaving them at the defaults for this project.
    *   **Disabled Multi-Factor Authentication (MFA)** to avoid incurring costs.
    *   Enabled self-service account recovery with email as the delivery method.
    *   Configured the sign-up experience, enabling self-registration.
    *   Selected Cognito to automatically send messages for verification and confirmation.
    *   Selected 'name' as a required attribute for new users.
    *   Chose to use Cognito's default email service for development, noting the limitations of 50 emails per day.
    *   Named the user pool "crudderuserpool".
    *   Selected the public client app type.
    *   Named the app client "crudder" and disabled the client secret.
*   **Configuring Amplify**:
    *   Installed the AWS Amplify JavaScript library, which is required to use Cognito client-side.
    *   I learned **Amplify is an SDK, a hosting platform, a provisioning service, and a low-code solution**,
    *   Added code to the `app.js` file to configure Amplify.
    *   Environment variables such as region, user pool ID, and client ID.
*   **Conditional Code Changes**:
    *   Modified the `homefeedpage.js` file to conditionally show content based on authentication status.
    *   Implemented a `checkAuth` function to check if a user is authenticated and retrieve user data.
    *   Passed user data to the desktop navigation and sidebar components.
    *   Updated the profile info component to remove the old cookie-based authentication.
*   **Sign-in Page**:
    *   I replaced the cookie authentication with new code.
    *   I changed "username" to "email" in the code.
*   **User Creation**:
    *   I created a user manually in Cognito user pool with email, password and other details.
*   **Troubleshooting**:
    *   Encountered and resolved an error related to missing environment variables.
    *   Identified and corrected a mistake in the app client settings, which caused a "User SRP" error, necessitating the recreation of the user pool.
    *   Addressed an issue where error messages were not displaying correctly on the sign-in page.
    *   I was unable to confirm the user and user was able to get confirmation emails.
 

# Cognito Custom Pages

The following steps were taken to implement user authentication using Cognito Custom Pages:

*   **Investigated and resolved an error** that occurred when a user in a "Force change password" state tried to call a JWT token. This was addressed using an AWS CLI command to bypass the force password change step.
*   **Implemented a sign-up page**, including handling custom attributes such as name and preferred username.
*   **Configured a confirmation page** to allow users to confirm their email addresses after signing up.
*   **Addressed issues related to username and email configurations** in the Cognito user pool, which involved recreating the user pool with the correct settings.
*   **Implemented a password recovery page** to allow users to reset their passwords if they forget them.
*   **Identified the need to protect authenticated requests** on the back end.
*   **Explored the possibility of integrating identity providers** such as Facebook, Google, Amazon, or Apple for user login.
*   **Discussed potential UI improvements**, such as displaying a flash message after email confirmation and enhancing the password reset page.
*   **Demonstrated how to store additional user information** in Cognito, beyond the username and email, and how to retroactively add them.
*   **Showed how to examine the objects returned during the sign-in process** to understand available user attributes and session information.

# Cognito JWT Server-Side Verify

The goal was to implement a back end for Cognito authentication using Flask, focusing on verifying the access token passed from the front end to protect API endpoints. Here’s a summary of the steps taken:

*   **Access Token Handling**: The access token, obtained during front-end sign-in and stored in local storage, needs to be passed along with API calls to the back end. This token is included in the header of the request.

*   **Reading Headers in Flask**: Flask's `request` object is used to view the headers. The authorization header, typically a bearer token, is extracted from the request.

*   **CORS Configuration**: There was an issue with CORS (Cross-Origin Resource Sharing) that needed to be resolved to allow the authorization header. The code was updated to allow the authorization header and expose it.

*   **JWT Decoding and Verification**: The access token (JWT) needs to be decoded to extract information and verify its correctness. Instead of relying on a third-party library, the decision was made to implement a custom solution for token verification.

*   **Cognito Token Verification**: A new library was made called Cognito JWT token. This involves:
    *   Extracting header information.
    *   Verifying the signature.
    *   Decoding the token.
    *   Extracting the claims.
    *   Validating the token against Cognito-generated keys.

*   **Environment Variables**: The Cognito user pool ID and client ID are set as environment variables.

*   **Token Verification Implementation**: Implemented the token verification logic, extracting the access token from the header and verifying it using the Cognito JWT token. The claims are extracted.

*   **Authentication Endpoints**: Implemented logic to differentiate between authenticated and unauthenticated requests. Depending on the authentication status, different data is returned.

*   **Sign-out**: remove the item from local storage.

*   **Edge Cases and Debugging**: Several issues were encountered and resolved:
    *   An incorrect client ID in the Docker Compose file, causing authentication failures, was identified and fixed.
    *   The token expiration was checked.
    *   An issue where the token was not being cleared on sign-out was identified.

# JWT Exploration and Verification Strategies

**Objective**: To explore different approaches to verifying JWTs in an AWS environment, considering trade-offs between security, performance, and cost.

**Key Considerations and Options Explored:**

*   **JWT Verification with Cognito:**
    *   The initial approach involved using a third-party library for JWT verification.
    *   The use of `boto3` to call Cognito IPD (Identity Provider) and the `get_user` function was considered. However, this was deemed unsuitable because it involves hitting the Cognito API, which negates the benefit of JWTs (self-contained verification). The `get_user` function retrieves user attributes and metadata, which may not be necessary for simple verification.
*   **AWS-provided JWT Verification:**
    *   The AWS JWT Verify library (Node.js) was examined, which is recommended for API Gateway, AppSync, Lambda authorizers, CloudFront Lambda Edge, or Node.js apps running on ECS Fargate.
    *   A Python equivalent was sought, and community-developed libraries were found.
    *   The importance of auditing community libraries for quality and security was emphasized. AWS-provided libraries are generally preferred due to official support.
*   **Alternative Architectures for JWT Verification:** Several architectural patterns were considered for implementing JWT verification:
    *   **Middleware:** Implementing custom middleware within the Flask application to handle JWT verification. This approach keeps the verification logic within the application but requires the middleware to be written in the same language as the server (Flask/Python).
    *   **Sidecar Container:** Using a separate container (sidecar) running a Node.js application with the AWS JWT Verify library. The Flask app would pass requests to the sidecar for JWT verification. This allows using different languages but adds complexity and resource overhead, especially in ECS EC2 environments where capacity planning is crucial.
    *   **API Gateway with Lambda Authorizer:** Utilizing AWS API Gateway with a Lambda authorizer function to handle JWT verification. API Gateway can directly authorize JWTs or use a Lambda function. The trade-offs include potential cost implications (depending on API Gateway usage) and the possibility of API Gateway returning 401 errors, which might not be desired.
*   **JWT Structure and Claims:**
    *   JWTs have a specific structure and contain encoded data (claims).
    *   Standard claims include audience (aud), issuer (iss), subject, expiration time, and more.
    *   The audience claim identifies the intended recipients of the JWT, such as a Cognito user pool.

**Trade-offs and Decisions:**

*   The key trade-off is between tightly coupled (code within the application) and decoupled (external services) solutions.
*   Factors to consider include:
    *   **Maintainability:** Smaller, self-written code may be easier to maintain.
    *   **Security:** Community libraries should be carefully audited.
    *   **Performance:** Avoiding unnecessary API calls (like hitting Cognito for verification) is crucial.
    *   **Cost:** API Gateway can be expensive at scale.
    *   **Complexity:** Introducing additional containers (sidecar) or services (API Gateway) increases architectural complexity.

**Considerations for Future Implementation:**

*   Explore API Gateway with Lambda authorizers, keeping in mind the potential for 401 errors and cost implications.
*   Investigate the amplify refresh token to ensure tokens are refreshed.

# Improving UI Contrast and Implementing CSS Variables for Theming

In this part of the AWS cloud project bootcamp, the focus was on improving the UI contrast and implementing CSS variables for theming. The goal was to make the UI easier to see, especially on monitors where the initial design appeared unclear.

Here's a breakdown of the steps taken:

*   **Initial Assessment:** The existing UI was evaluated, noting the difficulty in distinguishing between different areas due to poor contrast.
*   **CSS Adjustments:**
    *   The background colour was modified using the inspector tool to find a more suitable colour.
    *   The colour was changed by dragging the colour picker to a more suitable color.
    *   The specific code for the colour was found in the index.css file.
    *   The border bottom colour of elements was adjusted to improve visibility.
    *   The colour was changed by dragging the colour picker to a more suitable colour.
    *   The code for the border bottom color was found in the activity item CSS.
*   **CSS Variables for Theming:**
    *   CSS variables were introduced to manage colours more efficiently and enable theming.
    *   Variables were defined in the root element within the index.css file.
    *   Existing colour values were replaced with references to these CSS variables.
    *   This approach allows for easier modification of the colour scheme across the application.
*   **Addressing Contrast Issues:**
    *   Contrast issues around specific elements, such as the search field, were identified and addressed.
    *   New CSS variables were created for field borders and backgrounds.
    *   Adjustments were made to ensure consistency in UI elements across different pages, such as the sign-in page.
*   **Code Maintenance Considerations**:
    *   A decision to use CSS instead of SAS was made, in light of long term maintainability.
    *   It was determined that using a simpler and primitive code, such as CSS, is better for maintenance long term.
*   **Commit and Sync:** The changes were committed with the message "Improved UI changes and theme CSS variables" and then synced.

The overall goal was to improve the UI's visibility and maintainability by adjusting colours, introducing CSS variables for theming, and ensuring consistency across different components and pages.

# Topics -- Securing Amazon RDS Postgres Database

Here are some of the topics covered in this part of the bootcamp:
*   **Creating an Amazon RDS Postgres database** securely, including a walkthrough of the Amazon console.
*   **Connecting to the database** and troubleshooting common connection errors.
*   **Database types in the cloud**:
    *   Relational databases (e.g., MySQL, SQL Server, Postgres). These have tables with rows that have connections. SQL queries can retrieve information.
    *   Non-relational databases (e.g., DynamoDB). These are more decoupled, without strong relationships between columns and rows.
*   **Amazon RDS database engines**, such as SQL Server, Postgres, Oracle, MariaDB, and Aurora. Aurora is Amazon's version of Postgres and MySQL.
*   **Why companies use Amazon RDS**: to store information like customer and credit card data.
*   **Security best practices** for Amazon RDS Postgres.
    *   Ensuring the database is in the correct region.
    *   Configuring inbound rules to restrict connections to trusted IPs.
    *   Setting up organization Service Control Policies (SCP) to prevent RDS instance deletion.
    *   Enabling deletion protection.
    *   Enforcing encryption on RDS.
    *   Using CloudTrail to audit database activities.
    *   Enabling Amazon GuardDuty to detect malicious behaviour.
    *   Limiting users who can create or connect to RDS instances.
    *   Considering different authentication types, such as IAM user or Kerberos.
*   **Troubleshooting connection errors**, which often involve checking security group rules and public accessibility settings.
*   **Deleting an Amazon RDS Postgres database** when it is no longer needed.




