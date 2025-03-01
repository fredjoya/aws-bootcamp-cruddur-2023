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
