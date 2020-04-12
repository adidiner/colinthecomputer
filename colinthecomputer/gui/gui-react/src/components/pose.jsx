import React, { Component } from 'react';
import Loading from './loading';

const API_ROOT = "http://127.0.0.1:8000"


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
      translation.push(<a key={key}> {key + " = " + this.state.translation[key].toFixed(3)} </a>);
    } for (let i in Object.keys(this.state.rotation)) {
      let key = Object.keys(this.state.rotation)[i];
      rotation.push(<a key={key}> {key + " = " + this.state.rotation[key].toFixed(3)} </a>);
    }

    console.log('agggggg' + this.state.translation)
    return (
      <div class="jumbotron" style={{display: 'flex',  justifyContent:'center', alignItems:'center', width:'60vh', height: '40vh'}}>
        <div class="text-center">
          <h5>Pose</h5>
          <h6 class="mb-0">translation</h6>
          <p class="mb-2"><small> {translation} </small></p>
          <h6 class="mb-0">rotation</h6>
          <small> {rotation} </small>
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


export default Pose;