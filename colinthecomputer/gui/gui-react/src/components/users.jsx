import React, { Component } from 'react';
import Loading from './loading'


class Users extends Component {
  state = {users: null}
  render() {
    console.log(window.api_root)
    if (!this.state.users) {
      return (
        <Loading />
        );
    }

    return (
      <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <a class="navbar-brand" href="/">
            <img src="/icons/colin.PNG" width="40px" class="d-inline-block align-top" alt=""/>
          </a>
        </nav>
        <div class='jumbotron' style={{display: 'flex', height: '100vh'}}>
          <div class="col text-center">
            <h2>Users</h2>
            <div class="list-groups">
              {this.state.users.map(user =>
                (<a href={`/users/${user.user_id}`} class="list-group-item list-group-item-action" key={user.user_id}>
                  <img src="/icons/user.PNG" alt="" width="45px"/>
                  {" "} {user.user_id} {user.username}
                  </a>))}
            </div>
          </div>
        </div>
      </div>
      );
  }

  componentDidMount = () => {
    fetch(window.api_root + '/users', {
      method: 'GET',
      mode:'cors',
      dataType: 'json'
    })
    .then(response => response.json())
    .then(data => {
      this.setState({users: data});
    });
  }
}
export default Users;