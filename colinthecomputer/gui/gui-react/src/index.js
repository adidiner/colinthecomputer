import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import App from './App';
import Users from './components/users';
import UserInfo from './components/user_info'
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';

const element = <h1>hey yall</h1>;

/*ReactDOM.render(
  <Users />,
  document.getElementById('root')
);*/

const routing = (
  <Router>
    <div>
      <Route exact path="/" component={App} />
      <Route exact path="/users" component={Users} />
      <Route path="/users/:id" component={UserInfo} />
    </div>
  </Router>
)

ReactDOM.render(
  routing,
  document.getElementById('root')
);
