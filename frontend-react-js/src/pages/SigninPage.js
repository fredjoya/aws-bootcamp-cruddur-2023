import './SigninPage.css';
import React from "react";
import { ReactComponent as Logo } from '../components/svg/logo.svg';
import { Link } from "react-router-dom";
import { Auth } from 'aws-amplify';

export default function SigninPage() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');

  const onsubmit = async (event) => {
    setErrors('');
    event.preventDefault();

    try {
      // Use Auth.signIn to authenticate the user
      const user = await Auth.signIn(email, password);

      // Store the access token in localStorage
      localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken);

      // Redirect to the home page
      window.location.href = "/";
    } catch (error) {
      console.log('Error signing in:', error);

      // Handle specific errors
      if (error.code === 'UserNotConfirmedException') {
        window.location.href = "/confirm";
      } else {
        setErrors(error.message);
      }
    }
  };

  const email_onchange = (event) => {
    setEmail(event.target.value);
  };

  const password_onchange = (event) => {
    setPassword(event.target.value);
  };

  let el_errors;
  if (errors) {
    el_errors = <div className='errors'>{errors}</div>;
  }

  return (
    <article className="signin-article">
      <div className='signin-info'>
        <Logo className='logo' />
      </div>
      <div className='signin-wrapper'>
        <form
          className='signin_form'
          onSubmit={onsubmit}
        >
          <h2>Sign into your Cruddur account</h2>
          <div className='fields'>
            <div className='field text_field username'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange}
              />
            </div>
            <div className='field text_field password'>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={password_onchange}
              />
            </div>
          </div>
          {el_errors}
          <div className='submit'>
            <Link to="/forgot" className="forgot-link">Forgot Password?</Link>
            <button type='submit'>Sign In</button>
          </div>
        </form>
        <div className="dont-have-an-account">
          <span>
            Don't have an account?
          </span>
          <Link to="/signup">Sign up!</Link>
        </div>
      </div>
    </article>
  );
}