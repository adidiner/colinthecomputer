import React from "react";
import ReactDOM from "react-dom";
import { Route, Switch, Link, BrowserRouter as Router } from "react-router-dom";
import App from "./App";
import Users from "./components/users";
import UserInfo from "./components/user_info";
import Snapshots from "./components/snapshots";
import SnapshotInfo from "./components/snapshot_info";
import ErrorPage from "./components/error";
import "./index.css";
import "bootstrap/dist/css/bootstrap.css";

const routing = (
  <Router>
    <div>
      <Switch>
        <Route exact path="/" component={App} />
        <Route exact path="/users" component={Users} />
        <Route exact path="/users/:user_id" component={UserInfo} />
        <Route exact path="/users/:user_id/snapshots" component={Snapshots} />
        <Route
          exact
          path="/users/:user_id/snapshots/:snapshot_id"
          render={(props) => (
            <SnapshotInfo key={props.match.params.snapshot_id} {...props} />
          )}
        />
        <Route
          path="*"
          exact={true}
          component={() => (
            <ErrorPage error={{ status: 404, text: "Not Found" }} />
          )}
          status={404}
        />
      </Switch>
    </div>
  </Router>
);

ReactDOM.render(routing, document.getElementById("root"));
