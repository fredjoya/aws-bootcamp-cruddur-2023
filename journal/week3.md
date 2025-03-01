# Week 3 — Decentralized Authentication

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
 

# Week 3 — Cognito Custom Pages

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
*   **Addressed an issue where the username was not pre-filled** on the confirmation page and acknowledged the need for better React skills to resolve it.

# Week 3 — Congito JWT Server-Side Verify

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

