import React, { Component } from 'react';
import Loading from './loading'

const API_ROOT = "http://127.0.0.1:8000"

class Snapshots extends Component {
  state = {snapshots: null}

  render() {
    if (!this.state.snapshots) {
      return (
        <Loading />
        );
    }

    var snapshots = this.state.snapshots;
    var lis = [];
    for (var i = 0; i < snapshots.length-3; i += 3) {
      var row = [];
      for (var j = 0; j < Math.min(snapshots.length-i, 3); j++) {
        row.push(
          <div class="col">
            <a role="button" class="btn btn-info">{snapshots[i+j].snapshot_id}</a>      
          </div>
        );
      }
      lis.push(<div class="row">{row}</div>);
    }

    return (
      <div class='jumbotron' style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
        {lis}
      </div>
      );
  }

  componentDidMount = () => {
    // console.log(this.props);
    var user_id = this.props.match.params.user_id;
    fetch(API_ROOT + '/users/' + user_id + '/snapshots', {
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
      this.setState({snapshots: data});
    })
    .catch(error => {
      console.log(error); // todo
    });
  }
}

export default Snapshots;