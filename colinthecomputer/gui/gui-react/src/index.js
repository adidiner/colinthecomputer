import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import App from './App';
import Users from './components/users';
import UserInfo from './components/user_info';
import Snapshots from './components/snapshots'
import SnapshotInfo from './components/snapshot_info'
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
      <Route exact path="/users/:user_id" component={UserInfo} />
      <Route exact path="/users/:user_id/snapshots" component={Snapshots} />
      <Route exact path="/users/:user_id/snapshots/:snapshot_id" render={(props) => (
  		<SnapshotInfo key={props.match.params.snapshot_id} {...props} />)}/>
    </div>
  </Router>
)

ReactDOM.render(
  routing,
  document.getElementById('root')
);
