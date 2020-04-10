import React, { Component } from 'react';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <Router>
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to Colin The Computer</h2>
        </div>
        <p className="App-intro">
          <a href={'users/'} 
            role="button" class="btn btn-outline-dark">view users</a>
        </p>
      </div>
      </Router>
    );
  }
}

export default App;
