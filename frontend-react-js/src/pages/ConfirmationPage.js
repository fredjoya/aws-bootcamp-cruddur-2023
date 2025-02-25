import './ConfirmationPage.css';
import React from "react";
import {ReactComponent as Logo} from '../components/svg/logo.svg';
import { Link } from "react-router-dom";
import { Auth } from 'aws-amplify';

export default function ConfirmationPage() {
  const [email, setEmail] = React.useState('');
  const [code, setCode] = React.useState('');
  const [errors, setErrors] = React.useState('');
  const [codeSent, setCodeSent] = React.useState(false);

  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('');
    
    try {
      await Auth.confirmSignUp(email, code);
      window.location.href = "/signin";
    } catch (error) {
      console.log('Error confirming sign up:', error);
      setErrors(error.message);
    }
  };

  const resendCode = async (event) => {
    event.preventDefault();
    setErrors('');
    
    try {
      await Auth.resendSignUp(email);
      setCodeSent(true);
    } catch (error) {
      console.log('Error resending code:', error);
      setErrors(error.message);
    }
  };

  const email_onchange = (event) => {
    setEmail(event.target.value);
  };

  const code_onchange = (event) => {
    setCode(event.target.value);
  };

  let el_errors;
  if (errors) {
    el_errors = <div className='errors'>{errors}</div>;
  }

  let code_sent;
  if (codeSent) {
    code_sent = <div className='sent'>A new confirmation code has been sent to your email</div>;
  }

  return (
    <article className="confirmation-article">
      <div className="confirmation-info">
        <Logo className="logo" />
      </div>
      <div className="confirmation-wrapper">
        <form className="confirmation_form" onSubmit={onsubmit}>
          <h2>Confirm your Cruddur account</h2>
          <div className="fields">
            <div className="field text_field email">
              <label>Email</label>
              <input type="text" value={email} onChange={email_onchange} />
            </div>
            <div className="field text_field code">
              <label>Confirmation Code</label>
              <input type="text" value={code} onChange={code_onchange} />
            </div>
          </div>
          {el_errors}
          {code_sent}
          <div className="submit">
            <button type="submit">Confirm Account</button>
          </div>
        </form>
        <div className="resend-code">
          <button onClick={resendCode}>Resend Confirmation Code</button>
        </div>
        <div className="signin-link">
          <Link to="/signin">Back to Sign In</Link>
        </div>
      </div>
    </article>
  );
}