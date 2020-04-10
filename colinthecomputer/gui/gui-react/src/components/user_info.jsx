import React, { Component } from 'react';
import Loading from './loading'

const API_ROOT = "http://127.0.0.1:8000"

class UserInfo extends Component {
  state = {user_info: null}

  renderGender(gender) {
    switch(gender) {
      case 'm':
        return (
          <span class="badge badge-pill badge-info">male</span>
          );
      case 'f':
        return (
          <span class="badge badge-pill badge-info">female</span>
          );
      case 'o':
        return (
          <div style={{display: 'flex',  justifyContent:'center'}}>
            <span class="badge badge-pill badge-info">gender: other</span>
          </div>
          );
    // todo <span class="bagde badge-pill badge-light">gender</span>
    }
  }

  renderBirthday(timestamp) {
    var date = new Date(timestamp * 1000);
    var age = new Date(new Date() - date).getFullYear() - 1970;
    return (
      <p>{"born " + date.toDateString() + " (age " + age + " years)" }</p>
      );
  }

  render() {
    if (!this.state.user_info) {
      return (
        <Loading />
        );
    }

    var user_info = this.state.user_info;
    return (
      <div style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
      <div class='jumbotron' style={{display: 'flex',  justifyContent:'center', alignItems:'center', height:'80vh'}}>  
        <div class='col text-center'>
          <h2>{user_info.username}</h2>
          <h4>{"user #" + user_info.user_id}</h4>
          {this.renderGender(user_info.gender)}
          {this.renderBirthday(user_info.birthday)}
          <a href={user_info.user_id + '/snapshots'} 
            role="button" class="btn btn-outline-dark">view snapshots</a>
        </div>
      </div>
      </div>
      );
  }

  componentDidMount = () => {
    // console.log(this.props);
    var id = this.props.match.params.user_id;
    fetch(API_ROOT + '/users/' + id, {
      method: 'GET',
      mode:'cors',
      dataType: 'json'
    })
    .then(response => {
      if (!response.ok) {
        console.log(response);
        throw Error(response.statusText);
      }
      return response;
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      this.setState({user_info: data});
    })
    .catch(error => {
      console.log(error); // todo
    });
  }
}

export default UserInfo;