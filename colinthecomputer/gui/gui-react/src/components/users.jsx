import React, { Component } from 'react';

const API_ROOT = "http://127.0.0.1:8000"

class Users extends Component {
  state = {users: null}
  render() {
    if (!this.state.users) {
      return (
        <div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
            <div class="spinner-grow text-warning" role="status">
              <span class="sr-only">Thinking...</span>
            </div>
            <div class="spinner-grow text-warning" role="status">
              <span class="sr-only">Thinking...</span>
            </div>
            <div class="spinner-grow text-warning" role="status">
              <span class="sr-only">Thinking...</span>
            </div>
          </div>
        );
    }

    return (
      <div>
        <div style={{display: 'flex',  justifyContent:'center'}}>
          <h2>Users</h2>
        </div>
        <div class="list-groups">
          {this.state.users.map(user =>
            (<a href={user.user_id} class="list-group-item list-group-item-action" key={user.user_id}>
              {user.user_id} {user.username}
              </a>))}
        </div>
      </div>
      );
  }

  componentDidMount = () => {
    fetch(API_ROOT + '/users', {
      method: 'GET',
      mode:'cors',
      dataType: 'json'
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      this.setState({users: data});
    });
  }
}
export default Users;