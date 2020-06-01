import React, { Component } from "react";
import { Route, Link, BrowserRouter as Router } from "react-router-dom";
import logo from "./logo.svg";
import "./App.css";

class App extends Component {
  render() {
    return (
      <Router>
        <div
          class="m-5 container"
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div class="col text-center">
            <img
              class="ml-5"
              src={`${process.env.PUBLIC_URL}/icons/colin.PNG`}
              alt="colin logo"
              width="500vh"
            />
            <h1
              style={{
                color: "#897159",
                fontWeight: "bold",
                fontFamily: "'Chelsea Market', cursive",
              }}
            >
              Welcome to Colin The Computer
            </h1>
            <h5
              style={{
                fontFamily: "'Chelsea Market', cursive",
              }}
            >
              What's your favorite idea?
            </h5>
            <a href={"/users/"} role="button" class="mt-3 btn btn-outline-dark">
              view users
            </a>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
