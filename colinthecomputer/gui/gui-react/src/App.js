import React, { Component } from 'react';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <Router>
        <div class="m-5 container" style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
            <div class="col text-center">
              <img src="/icons/colin.PNG" alt="colin logo" width="500vh"/>
              <h2>Welcome to Colin The Computer</h2>
                <a href={'/users/'} 
                  role="button" class="btn btn-outline-dark">view users</a>
            </div>
          </div>
      </Router>
    );
  }
}

export default App;
