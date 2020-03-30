import React, { Component } from 'react';
import Loading from './loading';
import _ from 'lodash';

const API_ROOT = "http://127.0.0.1:8000"

class SnapshotInfo extends Component {
  state = {loaded: null, user_id: null, datetime: null, snapshot_id: null, results: null}

  render() {
    if (!this.state.loaded) {
      return (
        <Loading />
        );
    }

    console.log(this.state)
    return (
      <div class="container" style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
          <Pose user_id={this.state.user_id} snapshot_id={this.state.snapshot_id}/>
          <ColorImage user_id={this.state.user_id} snapshot_id={this.state.snapshot_id}/>
      </div>
      );
  }

  fetch_results = (results) => {
    var fetched_results = {};
    for (var i = 0; i < results.length; i++) {
      fetched_results[results[i]] = this.fetch_result(results[i]);
    }
    return fetched_results;
  }

  componentDidMount = () => {
    // console.log(this.props);
    var user_id = this.props.match.params.user_id;
    var snapshot_id = this.props.match.params.snapshot_id;
    fetch(API_ROOT + '/users/' + user_id + '/snapshots/' + snapshot_id, {
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
      this.state.user_id = user_id;
      this.state.snapshot_id = snapshot_id;
      console.log(data);
      this.setState({loaded: true,
                    user_id: user_id,
                    datetime: data.datetime,
                    snapshot_id: snapshot_id, 
                    results: data.results});
      
    })
    .catch(error => {
      console.log(error); // todo
    });
  }
}


class Pose extends Component {
  state = {loaded: null, translation: null, rotation: null}
  render() {
    if (!this.state.loaded) {
      return (
        <Loading />
        );
    }

    var translation = [];
    var rotation = [];
    console.log(this.state.rotation, Object.keys(this.state.rotation))
    for (let i in Object.keys(this.state.translation)) {
      let key = Object.keys(this.state.translation)[i];
      translation.push(<a key={key} class="my-4"> {key + " = " + this.state.translation[key]} </a>);
    } for (let i in Object.keys(this.state.rotation)) {
      let key = Object.keys(this.state.rotation)[i];
      rotation.push(<a key={key} class="my-4"> {key + " = " + this.state.rotation[key]} </a>);
    }

    console.log('agggggg' + this.state.translation)
    return (
      <div class="jumbotron" style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
        <div class="text-center">
          <h4>Pose</h4>
          <p class="lead">translation</p>
          {translation}
          <p class="lead">rotation</p>
          {rotation}
        </div>
      </div>
      );
  }

  componentDidMount = () => {
    var user_id = this.props.user_id;
    var snapshot_id = this.props.snapshot_id;
    fetch(API_ROOT + '/users/' + user_id + '/snapshots/' + snapshot_id + '/pose', {
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
      this.setState({loaded: true, 
                    translation: data.translation,
                    rotation: data.rotation});
    })
    .catch(error => {
      console.log(error); // todo
    });
  }
}


class ColorImage extends Component {
  state = {loaded: null, path: null}
  render() {
    if (!this.state.loaded) {
      return (
        <Loading />
        );
    }

    return (
      <div class="jumbotron" style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
        <img src={API_ROOT + this.state.path} width="500"/>
      </div>
      );
  }

  componentDidMount = () => {
    var user_id = this.props.user_id;
    var snapshot_id = this.props.snapshot_id;
    fetch(API_ROOT + '/users/' + user_id + '/snapshots/' + snapshot_id + '/color_image', {
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
      this.setState({loaded: true, 
                    path: data.path});
    })
    .catch(error => {
      console.log(error); // todo
    });
  }
}


export default SnapshotInfo;