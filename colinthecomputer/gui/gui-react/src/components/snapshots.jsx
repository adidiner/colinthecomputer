import React, { Component } from 'react';
import Loading from './loading';
import _ from 'lodash';

const API_ROOT = "http://127.0.0.1:8000"

class Snapshots extends Component {
  state = {snapshots: null}

  renderDatetime(timestamp) {
    var date = new Date(timestamp);
    return (
      <p>{date.toLocaleTimeString()}</p>
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
    for (var i = 0; i < snapshots.length-6; i += 6) {
      var row = [];
      for (var j = 0; j < Math.min(snapshots.length-i, 6); j++) {
        row.push(
          <div class="btn-group">
            <a role="button" href={'snapshots/' + snapshots[i+j].snapshot_id} class="btn btn-info">
            {this.renderDatetime(snapshots[i+j].datetime)}</a>      
          </div>
        );
      }
      lis.push(<div class="row">{row}</div>);
    }

    return (
      <div /*class="jumbotron jumbotron"*/ style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
        <div class="text-center">
          {lis}
        </div>
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