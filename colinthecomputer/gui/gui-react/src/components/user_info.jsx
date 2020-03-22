import React, { Component } from 'react';

const API_ROOT = "http://127.0.0.1:8000"

class UserInfo extends Component {
  state = {user_info: null}
  render() {
    if (!this.state.user_info) {
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

    var user_info = this.state.user_info;
    return (
      <div>
        <div style={{display: 'flex',  justifyContent:'center'}}>
          <h2>{user_info.username}</h2>
        </div>
        <span class="badge badge-pill badge-info">{user_info.gender}</span>
      </div>
      );
  }

  componentDidMount = () => {
    console.log(this.props)
    var id = this.props.match.params.id;
    fetch(API_ROOT + '/users/' + id, {
      method: 'GET',
      mode:'cors',
      dataType: 'json'
    })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      this.setState({user_info: data});
    });
  }
}
export default UserInfo;