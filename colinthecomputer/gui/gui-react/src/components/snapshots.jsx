import React, { Component } from 'react';
import Loading from './loading';
import {Link} from "react-router-dom";
import _ from 'lodash';


class Snapshots extends Component {
  state = {snapshots: null}

  renderDatetime(timestamp) {
    var date = new Date(timestamp);
    return (
      <p>{`${date.toLocaleTimeString()}`}</p>
      );
  }

  render() {
    if (!this.state.snapshots) {
      return (
        <Loading />
        );
    }

    var snapshots = _.sortBy(this.state.snapshots, ['datetime']);
    var lis = [];
    for (var i = 0; i < snapshots.length; i++) {
      lis.push(
        <div>
          <div class="jumbotron m-1" style={{display: 'flex', justifyContent:'center', alignItems:'center', height: "36vh", width: "36vh"}}>
            <div class="col text-center">
              <img src="/icons/snapshot.PNG" alt="" width="40px"/>
              <Link style={{color: "green", fontSize:"14px"}} to={{
                pathname: `/users/${this.state.user_id}/snapshots/${snapshots[i].snapshot_id}`,
                state: {
                  snapshots: snapshots,
                  index: `${i}`
                }
              }}>
              {`\nsnapshot #${i+1}: `}
              {this.renderDatetime(snapshots[i].datetime)}
              </Link>
            </div>
          </div>
        </div>
        );
    }
    
    return (
      <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <a class="navbar-brand" href="/">
            <img src="/icons/colin.PNG" width="40px" class="d-inline-block align-top" alt=""/>
          </a>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
              <a class="nav-item nav-link" href={`/users/${this.state.user_id}/`}>
                <img src="/arrows/back.PNG" width="40px" class="d-inline-block align-top" alt=""/>
              </a>
            </div>
          </div>
        </nav>
        <div class="mx-3" style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
          <div class="col text-center">
            <div class="row text-center">
              {lis}
            </div>
          </div>
        </div>
      </div>
      );
  }

  componentDidMount = () => {
    // console.log(this.props);
    var user_id = this.props.match.params.user_id;
    fetch(window.api_root + '/users/' + user_id + '/snapshots', {
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
      this.setState({user_id: user_id,
                     snapshots: data});
    })
    .catch(error => {
      console.log(error); // todo
    });
  }
}

export default Snapshots;